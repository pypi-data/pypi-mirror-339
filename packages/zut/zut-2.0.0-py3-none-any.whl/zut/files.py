"""
File and directory operations, compatible with both the local file system and Samba/Windows shares.
"""
from __future__ import annotations

from getpass import getuser
import ntpath
import os
import shutil
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from tempfile import mktemp
from typing import Callable

from zut import (SudoNotAvailable, get_logger, get_secret, is_sudo_available,
                 parse_tz, run_process, skip_utf8_bom)

try:
    # package `smbprotocol`: required if not Windows, or if non default credentials
    import smbclient
    import smbclient.path as smbclient_path
    import smbclient.shutil as smbclient_shutil
except ModuleNotFoundError:
    smbclient = None
    smbclient_path = None
    smbclient_shutil = None

_open = open
_smb_credentials_configured = None
_smb_port = 445

_logger = get_logger(__name__)


def configure_smb_credentials(user: str = None, password: str = None, host: str = None, port: int = None, *, once = False):
    global _smb_credentials_configured, _smb_port

    if once and _smb_credentials_configured is not None:
        return
    
    if not user:
        user = os.environ.get('SMB_USER')
        
    if not password:
        password = get_secret('SMB_PASSWORD')
        
    if not host:
        host = os.environ.get('SMB_HOST')
        
    if not port:
        port = os.environ.get('SMB_PORT')
        if port:
            port = int(port)
    _smb_port = port if port else 445

    if user or password or host or port:
        if not smbclient:
            raise ValueError(f"Package `smbprotocol` is required to specify smb credentials")
        if host or port:
            smbclient.register_session(server=host, port=port, username=user, password=password)
        else:
            smbclient.ClientConfig(username=user, password=password)
        _smb_credentials_configured = True
    else:
        _smb_credentials_configured = False


def can_use_network_paths():
    if sys.platform == 'win32' and not _smb_credentials_configured:
        return True  # Python is natively compatible with Samba shares on Windows

    return smbclient is not None


def _standardize(path: str|Path) -> tuple[str,bool]:
    """
    Return (path, use_native).
    """
    if not path:
        return path, True
    
    if isinstance(path, Path):
        path = str(path)

    path = os.path.expanduser(path)
    
    if not (path.startswith("\\\\") or path.startswith("//")):
        return path, True  # not a network path
        
    if sys.platform == 'win32' and not _smb_credentials_configured:
        return path, True  # Python is natively compatible with Samba shares on Windows

    return path, False


def dirname(path: str|Path):
    path, use_native = _standardize(path)
    
    if use_native:
        return os.path.dirname(path)
    
    return ntpath.dirname(path)


def basename(path: str|Path):
    path, use_native = _standardize(path)

    if use_native:
        return os.path.basename(path)

    return ntpath.basename(path)


def join(*paths: str|Path):
    remaining_paths = []
    method = 'os'
    for path in paths:
        path = os.path.expanduser(path)
        if isinstance(path, str) and (path.startswith("//") or '://' in path):
            remaining_paths = [path]
            method = 'custom'
        elif isinstance(path, str) and (path.startswith('\\\\')):
            remaining_paths = [path]
            method = 'nt'
        else:
            remaining_paths.append(path)

    if method == 'os':
        return os.path.join(*remaining_paths)
    elif method == 'nt':
        return ntpath.join(*remaining_paths)
    else:
        return '/'.join(remaining_paths)


def indir(path: str|os.PathLike, dir: str|os.PathLike|None = None, **kwargs):
    """
    Return the given path from within the given directory if any, relative to the current directory.
    """
    if not isinstance(path, str):
        if isinstance(path, os.PathLike):
            path = str(path)
        else:
            raise TypeError(f"Argument 'path' must be a string or PathLike object, not {type(path).__name__}")

    if dir is not None and not isinstance(dir, str):
        if isinstance(dir, os.PathLike):
            dir = str(dir)
        else:
            raise TypeError(f"Argument 'dir' must be a string or PathLike object, not {type(dir).__name__}")

    if not path.startswith(('./', '.\\')):
        if dir:
            path = join(dir, path)

    if kwargs:
        path = path.format(**kwargs)

    try:
        rel_path = os.path.relpath(path)
        if rel_path.startswith(('../', '..\\')):
            return path
        return rel_path
    except ValueError:
        return path


def splitext(path: str|Path):
    path, use_native = _standardize(path)

    if use_native:
        return os.path.splitext(path)
    
    return ntpath.splitext(path)


def exists(path: str|Path):
    path, use_native = _standardize(path)

    if use_native:
        return os.path.exists(path)

    if not smbclient:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient_path.exists(path, port=_smb_port)


def stat(path: str|Path):
    path, use_native = _standardize(path)

    if use_native:
        return os.stat(path)
    
    if not smbclient:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient.stat(path, port=_smb_port)


def mtime(path: str|Path|zipfile.Path):
    if isinstance(path, zipfile.Path):
        y, m, d, hour, min, sec = path.root.getinfo(path.at).date_time
        # Inside zip files, dates and times are stored in local time in 16 bits, not UTC (Coordinated Universal Time/Temps Universel Coordonné) as is conventional, using an ancient MS DOS format.
        # Bit 0 is the least signifiant bit. The format is little-endian. There was not room in 16 bit to accurately represent time even to the second, so the seconds field contains the seconds divided by two, giving accuracy only to the even second.
        return datetime(y, m, d, hour, min, sec, tzinfo=parse_tz('localtime'))
    else:
        st = os.stat(path)
        return datetime.fromtimestamp(st.st_mtime).astimezone()


def makedirs(path: str|Path, exist_ok: bool = False):
    path, use_native = _standardize(path)

    if use_native:
        return os.makedirs(path, exist_ok=exist_ok)

    if not smbclient:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient.makedirs(path, exist_ok=exist_ok, port=_smb_port)


def remove(path: str|Path, missing_ok: bool = False):
    path, use_native = _standardize(path)

    if missing_ok:
        if not exists(path):
            return

    if use_native:
        os.remove(path)
        return

    if not smbclient:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    smbclient.remove(path, port=_smb_port)


def rmtree(path: str|Path, ignore_errors=False, onerror=None, missing_ok: bool = False):
    path, use_native = _standardize(path)

    if missing_ok:
        if not exists(path):
            return

    if use_native:
        shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror)
        return
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    smbclient_shutil.rmtree(path, ignore_errors=ignore_errors, onerror=onerror, port=_smb_port)


def open(path: str|Path, mode="r", buffering: int = -1, encoding: str = None, errors: str = None, newline: str = None, mkdir: bool = False, **kwargs):
    if mkdir:
        dir_path = dirname(path)
        if dir_path:
            makedirs(dir_path, exist_ok=True)

    path, use_native = _standardize(path)

    if use_native:
        return _open(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, **kwargs)

    if not smbclient:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient.open_file(path, mode=mode, buffering=buffering, encoding=encoding, errors=errors, newline=newline, port=_smb_port, **kwargs)


def read_bytes(path: str|Path) -> bytes:
    """
    Open the file in bytes mode, read it, and close the file.
    """
    with open(path, mode='rb') as f:
        return f.read()


def read_text(path: str|Path, encoding: str = None, errors: str = None, newline: str = None, sudo = False) -> str:
    """
    Open the file in text mode, read it, and close the file.
    """
    if sudo and not os.access(path, os.R_OK):
        if not is_sudo_available():
            raise SudoNotAvailable()
        
        try:
            tmp = mktemp()
            run_process(['cp', path, tmp], check=True, sudo=True)
            run_process(['chown', getuser(), tmp], check=True, sudo=True)
            with _open(tmp, 'r', encoding=encoding, errors=errors, newline=newline) as fp:
                return fp.read()
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    else:
        with open(path, mode='r', encoding=encoding, errors=errors, newline=newline) as f:        
            skip_utf8_bom(f, encoding)
            return f.read()


def write_bytes(path: str|Path, data):
    """
    Open the file in bytes mode, write to it, and close the file.
    """
    with open(path, mode='wb') as f:
        return f.write(data)


def write_text(path: str|Path, data: str, encoding: str = None, errors: str = None, newline: str = None, sudo = False):
    """
    Open the file in text mode, write to it, and close the file.
    """
    if sudo:
        if not is_sudo_available():
            raise SudoNotAvailable()

        try:
            tmp = mktemp()
            with _open(tmp, mode='w', encoding=encoding, errors=errors, newline=newline) as fp:
                fp.write(data)
            run_process(['cp', tmp, path], check=True, sudo=True)
        finally:
            os.unlink(tmp)
    else:
        with open(path, mode='w', encoding=encoding, errors=errors, newline=newline) as f:
            return f.write(data)


def copy(src: str|Path, dst: str|Path, follow_symlinks=True):
    """
    Copy file data and file data and file's permission mode (which on Windows is only the read-only flag).
    Other metadata like file's creation and modification times, are not preserved.

    The destination may be a directory (in this case, the file will be copied into `dst` directory using
    the base filename from `src`).

    If `follow_symlinks` is `False`, `dst` will be created as a symbolic link if `src` is a symbolic link.
    If `follow_symlinks` is `True`, `dst` will be a copy of the file `src` refers to.
    """
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)
    
    if src_native and dst_native:
        return shutil.copy(src, dst, follow_symlinks=follow_symlinks)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient_shutil.copy(src, dst, follow_symlinks=follow_symlinks, port=_smb_port)


def copy2(src: str|Path, dst: str|Path, follow_symlinks=True):
    """
    Identical to `copy()` except that `copy2()` also attempts to preserve the file metadata.

    `copy2()` uses `copystat()` to copy the file metadata. Please see `copystat()` for more information about how and what
    metadata it copies to the `dst` file.

    If `follow_symlinks` is `False`, `dst` will be created as a symbolic link if `src` is a symbolic link.
    If `follow_symlinks` is `True`, `dst` will be a copy of the file `src` refers to.
    """
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)
    
    if src_native and dst_native:
        return shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient_shutil.copy2(src, dst, follow_symlinks=follow_symlinks, port=_smb_port)


def copyfile(src: str|Path, dst: str|Path, follow_symlinks=True):
    """
    Copy the contents (no metadata) in the most efficient way possible.

    If `follow_symlinks` is `False`, `dst` will be created as a symbolic link if `src` is a symbolic link.
    If `follow_symlinks` is `True`, `dst` will be a copy of the file `src` refers to.
    """
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)
    
    if src_native and dst_native:
        return shutil.copyfile(src, dst, follow_symlinks=follow_symlinks)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient_shutil.copyfile(src, dst, follow_symlinks=follow_symlinks, port=_smb_port)


def copystat(src: str|Path, dst: str|Path, follow_symlinks=True):
    """
    Copy the read-only attribute, last access time, and last modification time from `src` to `dst`.
    The file contents, owner, and group are unaffected.

    If `follow_symlinks` is `False` and `src` and `dst` both refer to symbolic links, the attributes will be read and written
    on the symbolic links themselves (rather than the files the symbolic links refer to).
    """
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)
    
    if src_native and dst_native:
        return shutil.copystat(src, dst, follow_symlinks=follow_symlinks)
    
    if not smbclient_shutil:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient_shutil.copystat(src, dst, follow_symlinks=follow_symlinks, port=_smb_port)


def copymode(src: str|Path, dst: str|Path, follow_symlinks=True):
    """
    Copy the permission bits from `src` to `dst`.
    The file contents, owner, and group are unaffected.
    
    Due to the limitations of Windows, this function only sets/unsets `dst` FILE_ATTRIBUTE_READ_ONLY flag based on what `src` attribute is set to.

    If `follow_symlinks` is `False` and `src` and `dst` both refer to symbolic links, the attributes will be read and written
    on the symbolic links themselves (rather than the files the symbolic links refer to).
    """
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)

    if src_native and dst_native:
        return shutil.copymode(src, dst, follow_symlinks=follow_symlinks)

    if not smbclient_shutil:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient_shutil.copymode(src, dst, follow_symlinks=follow_symlinks, port=_smb_port)


def copytree(src: str|Path, dst: str|Path, symlinks: bool = False, ignore: Callable[[str, list[str]],list[str]] = None, ignore_dangling_symlinks: bool = False, dirs_exist_ok: bool = False):
    """
    Recursively copy a directory tree rooted at `src` to a directory named `dst` and return the destination directory.

    Permissions and times of directories are copied with `copystat()`, individual files are copied using `copy2()`.

    If `symlinks` is true, symbolic links in the source tree result in symbolic links in the destination tree;
    if it is false, the contents of the files pointed to by symbolic links are copied. If the file pointed by the symlink doesn't
    exist, an exception will be added. You can set `ignore_dangling_symlinks` to true if you want to silence this exception.
    Notice that this has no effect on platforms that don't support `os.symlink`.

    If `dirs_exist_ok` is false (the default) and `dst` already exists, an error is raised. If `dirs_exist_ok` is true, the copying
    operation will continue if it encounters existing directories, and files within the `dst` tree will be overwritten by corresponding files from the
    `src` tree.

    If `ignore` is given, it must be a callable of the form `ignore(src, names) -> ignored_names`.
    It will be called recursively and will receive as its arguments the directory being visited (`src`) and a list of its content (`names`).
    It must return a subset of the items of `names` that must be ignored in the copy process.
    """
    src, src_native = _standardize(src)
    dst, dst_native = _standardize(dst)

    if src_native and dst_native:
        return shutil.copytree(src, dst, symlinks=symlinks, ignore=ignore, ignore_dangling_symlinks=ignore_dangling_symlinks, dirs_exist_ok=dirs_exist_ok)

    if not smbclient_shutil:
        raise ModuleNotFoundError(f'Missing package `smbprotocol`')
    return smbclient_shutil.copytree(src, dst, symlinks=symlinks, ignore=ignore, ignore_dangling_symlinks=ignore_dangling_symlinks, dirs_exist_ok=dirs_exist_ok, port=_smb_port)


def archivate(path: str|Path, archive_dir: bool|str|Path|None = None, *, missing_ok: bool = False, keep: bool = False) -> str:
    """
    Archivate `path` to `archive_dir` directory, ensuring unique archive name.
    - `archive_dir`: By default (if None), use the same directory as the origin path. If relative, it is relative to the directory of the original path.
    - `missing_ok`: If True, do not throw an exception if the original file does not exist.
    - `keep`: If True, the original file is not removed after archiving.
    """
    if archive_dir is False:
        return
    
    if isinstance(path, Path):
        path = str(path)

    if missing_ok:
        if not path or not exists(path):
            return

    if isinstance(archive_dir, Path):
        archive_dir = str(archive_dir)
    
    if not exists(path):
        return FileNotFoundError(f'Path does not exist: {path}')
    
    if archive_dir is None or archive_dir is True:
        archive_dir = dirname(path)
    else:
        if not os.path.isabs(archive_dir):
            archive_dir = join(dirname(path), archive_dir)
        if not exists(archive_dir):
            makedirs(archive_dir)
   
    bname = basename(path)
    stem, ext = splitext(bname)
    archive = join(archive_dir, stem + ext)
    if exists(archive):            
        st = stat(path)
        mtime = datetime.fromtimestamp(st.st_mtime)
        mainpart = join(archive_dir, stem + f"_{mtime.strftime('%Y%m%d')}")
        
        i = 1
        while True:
            archive = mainpart + (f"-{i}" if i > 1 else '') + ext
            if not exists(archive):
                break
            i += 1

    _logger.debug(f"Archivate %s to %s", path, archive)
    copy2(path, archive)
    if not keep:
        remove(path)
    return archive
