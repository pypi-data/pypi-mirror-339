"""
Common operations on databases.
"""
from __future__ import annotations

import logging
import os
import re
import socket
from collections import abc
from datetime import date, datetime, time, tzinfo
from decimal import Decimal
from enum import Enum, Flag
from io import IOBase
from pathlib import Path
from secrets import token_hex
import sys
from threading import current_thread
from time import time_ns
from typing import Any, Generator, Generic, Iterable, Mapping, Sequence, Tuple, TypeVar, overload
from urllib.parse import ParseResult, parse_qs, quote, unquote, urlparse

from zut import (TupleRow, Header, Literal, Protocol, TabularDumper, Secret, get_secret, build_url,
                 convert, examine_csv_file, files, get_default_csv_delimiter,
                 get_default_decimal_separator, get_logger, get_tzkey,
                 hide_url_password,
                 now_naive_utc, parse_tz, slugify, tabular_dumper, slugify_snake)

try:
    from django.http import Http404 as _BaseNotFoundError
except ModuleNotFoundError:
    _BaseNotFoundError = Exception

try:
    from tabulate import tabulate
except ModuleNotFoundError:
    tabulate = None


#region Protocol objects (for type generics)

class Connection(Protocol):
    def close(self) -> None:
        ...

    def commit(self) -> None:
        ...

    def cursor(self) -> Cursor:
        ...


class Cursor(Protocol):
    def __enter__(self) -> Cursor:
        ...

    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None) -> None:
        ...

    def close(self) -> None:
        ...
    
    def execute(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None) -> None:
        ...

    def nextset(self) -> bool:
        ...

    @property
    def connection(self) -> Connection:
        ...

    @property
    def rowcount(self) -> int:
        ...

    @property
    def description(self) -> tuple[tuple[str, Any, int, int, int, int, bool]]:
        ...

#endregion

if sys.version_info < (3, 13): # TypeVar's default argument introduced in Python 3.13
    T_Connection = TypeVar('T_Connection', bound=Connection)
    T_Cursor = TypeVar('T_Cursor', bound=Cursor)
else:
    T_Connection = TypeVar('T_Connection', bound=Connection, default=Connection)
    T_Cursor = TypeVar('T_Cursor', bound=Cursor, default=Cursor)


class Db(Generic[T_Connection, T_Cursor]):
    """
    Base class for database adapters.
    """

    #region Init

    # DB engine specifics
    scheme: str
    default_port: int
    default_schema: str|None = 'public'
    only_positional_params = False
    split_multi_statement_files = False
    table_in_path = True
    identifier_quotechar_begin = '"'
    identifier_quotechar_end = '"'
    sql_placeholder = '%s'
    sql_named_placeholder = '%%(%s)s'
    bool_sql_basetype = 'boolean'
    int_sql_basetype = 'bigint'
    float_sql_basetype = 'double precision'
    decimal_sql_basetype = 'numeric'
    datetime_sql_basetype = 'timestamp with time zone'
    date_sql_basetype = 'date'
    str_sql_basetype = 'text'
    str_precised_sql_basetype = 'character varying'
    accept_aware_datetime = True
    truncate_with_delete = False
    can_cascade_truncate = True
    identity_definition_sql = 'GENERATED ALWAYS AS IDENTITY'
    procedure_caller = 'CALL'
    procedure_params_parenthesis = True
    function_requires_schema = False
    can_add_several_columns = False
    temp_schema = 'pg_temp'
    missing_dependency: str = None
    
    # Global configurable
    autocommit = True
    use_http404 = False
    """ Use Django's HTTP 404 exception instead of NotFoundError (if Django is available). """

    def __init__(self, origin: T_Connection|str|ParseResult|dict|None = None, *, name: str = None, user: str = None, password: str|Secret = None, host: str = None, port: str = None, encrypt: bool|None = None, password_required: bool = False, autocommit: bool = None, tz: tzinfo|str|None = None, migrations_dir: str|os.PathLike = None, table: str|None = None, schema: str|None = None):
        """
        Create a new Db instance.
        - `origin`: an existing connection object (or Django wrapper), the URL for the new connection to be created by the Db instance, or the key to build a connection object (name of DB, or prefix of environment variable names).
        - `autocommit`: commit transactions automatically (applies only for connections created by the Db instance).
        - `tz`: naive datetimes in results are made aware in the given timezone.
        """
        if self.missing_dependency:
            raise ValueError(f"Cannot use {type(self).__name__} (missing {self.missing_dependency} dependency)")
                
        self.table: str = table
        """ A specific table associated to this instance. Used for example as default table for `dumper`. """

        self.schema: str = schema
        """ A specific schema associated to this instance. Used for example as default table for `dumper`. """

        logger_name = f"{__name__}.{self.__class__.__qualname__}"
        
        if origin is None:
            origin = getattr(self.__class__, 'origin', None)

        if origin is None:
            origin = {
                'name': name or getattr(self.__class__, 'name', None),
                'user': user or getattr(self.__class__, 'user', None),
                'password': password or getattr(self.__class__, 'password', None),
                'host': host or getattr(self.__class__, 'host', None),
                'port': port or getattr(self.__class__, 'port', None),
                'encrypt': encrypt if encrypt is not None else getattr(self.__class__, 'encrypt', None),
            }
            if not origin['name']:
                raise TypeError(f"Argument 'name' must be given when 'origin' is none.")
        
        elif (isinstance(origin, str) and not ':' in origin): # origin is a key: either the name of the DB, or the prefix of environment variable names
            logger_name += f'.{origin}'
            env_prefix = slugify(origin, separator='_').upper()     
            origin = {
                'name': os.environ.get(f'{env_prefix}_DB_NAME') or name or getattr(self.__class__, 'name', None) or origin,
                'user': os.environ.get(f'{env_prefix}_DB_USER') or user or getattr(self.__class__, 'user', None),
                'password': get_secret(f'{env_prefix}_DB_PASSWORD') or password or getattr(self.__class__, 'password', None),
                'host': os.environ.get(f'{env_prefix}_DB_HOST') or host or getattr(self.__class__, 'host', None),
                'port': os.environ.get(f'{env_prefix}_DB_PORT') or port or getattr(self.__class__, 'port', None),
                'encrypt': os.environ.get(f'{env_prefix}_DB_ENCRYPT') if os.environ.get(f'{env_prefix}_DB_ENCRYPT') is not None else (encrypt if encrypt is not None else getattr(self.__class__, 'encrypt', None)),
            }
        
        else:            
            if name is not None:
                raise TypeError(f"Argument 'name' cannot be set when 'origin' is not a string.")
            if user is not None:
                raise TypeError(f"Argument 'user' cannot be set when 'origin' is not a string.")
            if password is not None:
                raise TypeError(f"Argument 'password' cannot be set when 'origin' is not a string.")
            if host is not None:
                raise TypeError(f"Argument 'host' cannot be set when 'origin' is not a string.")
            if port is not None:
                raise TypeError(f"Argument 'port' cannot be set when 'origin' is not a string.")
            if encrypt is not None:
                raise TypeError(f"Argument 'encrypt' cannot be set when 'origin' is not a string.")
        
        # Actual interpretation of 'origin'
        self._connection_url: str
        self._connection_encrypt: bool|None = None
        self._connection_url_secret: Secret|None = None
        if isinstance(origin, dict):
            self._owns_connection = True
            self._connection: T_Connection = None

            if 'NAME' in origin: # uppercase (as used by django)
                password = origin.get('PASSWORD', None)
                if isinstance(password, Secret):
                    self._connection_url_secret = password
                    password = None
                self._connection_encrypt = origin.get('ENCRYPT')
                
                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = origin.get('HOST', None),
                    port = origin.get('PORT', None),
                    username = origin.get('USER', None),
                    password = password,
                    path = origin.get('NAME', None),
                )
                if not self.table:
                    self.table = origin.get('TABLE', None)
                if not self.schema:
                    self.schema = origin.get('SCHEMA', None)

            else: # lowercase (as used by some drivers' connection kwargs)                
                password = origin.get('password', None)
                if isinstance(password, Secret):
                    self._connection_url_secret = password
                    password = None
                self._connection_encrypt = origin.get('encrypt')

                self._connection_url = build_url(
                    scheme = self.scheme,
                    hostname = origin.get('host', None),
                    port = origin.get('port', None),
                    username = origin.get('user', None),
                    password = password,
                    path = origin.get('name', origin.get('dbname', None)),
                )
                if not self.table:
                    self.table = origin.get('table', None)
                if not self.schema:
                    self.schema = origin.get('schema', None)

        elif (isinstance(origin, str) and ':' in origin) or isinstance(origin, ParseResult): # URL
            self._owns_connection = True
            self._connection: T_Connection = None

            r = origin if isinstance(origin, ParseResult) else urlparse(origin)
            if r.fragment:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected fragment: {r.fragment}")
            if r.params:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected params: {r.params}")
            
            query = parse_qs(r.query)
            query_schema = query.pop('schema', [None])[-1]
            if query_schema and self.schema is None:
                self.schema = query_schema
            query_table = query.pop('table', [None])[-1]                
            if query_table and self.table is None:
                self.table = query_table
            if query:
                raise ValueError(f"Invalid {self.__class__.__name__}: unexpected query data: {query}")
            
            scheme = r.scheme
            r = self._verify_scheme(r)
            if not r:
                raise ValueError(f"Invalid {self.__class__.__name__}: invalid scheme: {scheme}")

            if not self.table and self.table_in_path:
                table_match = re.match(r'^/?(?P<name>[^/@\:]+)/((?P<schema>[^/@\:\.]+)\.)?(?P<table>[^/@\:\.]+)$', r.path)
            else:
                table_match = None

            if table_match:
                if self.table is None:
                    self.table = table_match['table']
                if self.schema is None:
                    self.schema = table_match['schema'] if table_match['schema'] else None
            
                r = r._replace(path=table_match['name'])
                self._connection_url = r.geturl()            
            else:
                self._connection_url = r.geturl()
            self._connection_url_secret = None

        elif type(origin).__name__ in {'Connection', 'ConnectionProxy'} or hasattr(origin, 'cursor'):
            self._connection = origin
            self._connection_url: str = None
            self._owns_connection = False

            if password_required:
                raise TypeError(f"Argument 'password_required' cannot be set when 'origin' is connection object.")
            if autocommit is not None:
                raise TypeError(f"Argument 'autocommit' cannot be set when 'origin' is connection object.")
            if migrations_dir is not None:
                raise TypeError(f"Argument 'migrations_dir' cannot be set when 'origin' is connection object.")        
        else:
            raise TypeError(f"Invalid type for argument 'origin': {type(origin).__name__}")


        self.password_required = password_required
        if isinstance(tz, str):
            tz = tz if tz == 'localtime' else parse_tz(tz)
        self.tz = tz
        
        self._autocommit = autocommit or getattr(self.__class__, 'autocommit', None)
        self._migrations_dir = migrations_dir or getattr(self.__class__, 'migrations_dir', None)
        self._is_port_opened = None
        
        self._logger = get_logger(logger_name)
    

    @classmethod
    def get_sqlutils_path(cls):
        path = Path(__file__).resolve().parent.joinpath('sqlutils', f"{cls.scheme}.sql")
        if not path.exists():
            return None
        return path
    
    
    def _verify_scheme(self, r: ParseResult) -> ParseResult|None:
        if r.scheme == self.scheme:
            return r
        else:
            return None


    def get_url(self, *, hide_password = False):
        if self._connection_url:
            url = self._connection_url
        else:
            url = self._get_url_from_connection()

        if hide_password:
            url = hide_url_password(url, always_password=self._connection_url_secret)
        elif self._connection_url_secret:
            r = urlparse(url)
            r.password = self._connection_url_secret.value
            url = r.geturl()
            self._connection_url_secret = None
            self._connection_url = url

        if self.table:
            if self.table_in_path:
                url += f"/"
                if self.schema:
                    url += quote(self.schema)
                    url += '.'
                url += quote(self.table)
            else:
                url += f"?table={quote(self.table)}"
                if self.schema:
                    url += f"&schema={quote(self.schema)}"

        return url


    def _get_url_from_connection(self):
        raise NotImplementedError()
    

    def get_db_name(self):
        url = self.get_url(hide_password=True)
        r = urlparse(url)
        return unquote(r.path).lstrip('/')


    @property
    def is_port_opened(self):
        if self._is_port_opened is None:
            r = urlparse(self.get_url(hide_password=True))
            host = r.hostname or '127.0.0.1'
            port = r.port if r.port is not None else self.default_port
        
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug("Check host %s, port %s (from thread %s)", host, port, current_thread().name)

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((host, port))
                if result == 0:
                    self._logger.debug("Host %s, port %s: connected", host, port)
                    self._is_port_opened = True
                else:
                    self._logger.debug("Host %s, port %s: NOT connected", host, port)
                    self._is_port_opened = False
                sock.close()
            except Exception as err:
                raise ValueError(f"Cannot check host {host}, port {port}: {err}")
        
        return self._is_port_opened
    
    #endregion
    

    #region Connections, cursors and transactions

    def __enter__(self):
        return self


    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        self.close()


    def close(self):
        if self._connection is None or not self._owns_connection:
            return
        
        if self._logger.isEnabledFor(logging.DEBUG):
            self._logger.debug("Close %s (%s) connection to %s", type(self).__name__, type(self._connection).__module__ + '.' + type(self._connection).__qualname__, hide_url_password(self._connection_url, always_password=self._connection_url_secret))
        self._connection.close()
        self._connection = None


    @property
    def connection(self) -> T_Connection:
        if self._connection is None:
            if self._connection_url_secret:
                r = urlparse(self._connection_url)
                r.password = self._connection_url_secret.value
                self._connection_url_secret = None
                self._connection_url = r.geturl()

            elif self.password_required:
                password = urlparse(self._connection_url).password
                if not password:
                    raise ValueError("Cannot create %s connection to %s: password not provided" % (type(self).__name__, hide_url_password(self._connection_url)))
                
            if self._logger.isEnabledFor(logging.DEBUG):
                self._logger.debug(f"Create %s connection to %s", type(self).__name__, hide_url_password(self._connection_url))
            self._connection = self._create_connection()

            if self._migrations_dir:
                self.migrate(self._migrations_dir)
        return self._connection
    

    def get_autocommit(self):
        if not self._connection:
            return self._autocommit
        else:
            return self._connection.autocommit


    def _create_connection(self) -> T_Connection:
        raise NotImplementedError()
    
        
    def transaction(self):    
        try:
            from django.db import transaction
            from django.utils.connection import ConnectionProxy
            if isinstance(self._connection, ConnectionProxy):
                return transaction.atomic()
        except ModuleNotFoundError:
            pass
        return self._create_transaction()
        

    def _create_transaction(self):
        raise NotImplementedError()

    
    @overload
    def cursor(self, query: str = None, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source: str|None = None, result: Literal[False] = ...) -> CursorContext[T_Connection, T_Cursor]:
        """ Create a cursor, execute the given SQL statement if any, and return a context manager that gives the cursor object when entered (must be entered and exited properly using `with`). """
        ...

    @overload
    def cursor(self, query: str = None, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source: str|None = None, result: Literal[True]) -> ResultContext[T_Connection, T_Cursor]:
        """ Create a cursor, execute the given SQL statement if any, and return a result context manager (must be entered and exited properly using `with`). """
        ...
    
    def cursor(self, query: str = None, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source: str|None = None, result = False):
        if query:
            if limit is not None or offset is not None:
                query, _ = self.get_paginated_and_total_query(query, limit=limit, offset=offset)
            if isinstance(params, abc.Mapping) and self.only_positional_params:
                query, params = self.to_positional_params(query, params)
        return (ResultContext if result else CursorContext)(self, query, params, warn_results=warn_results, messages_source=messages_source)
    

    def _register_cursor_messages_handler(self, cursor: T_Cursor, messages_source: str|None):
        """
        Register a messages handler for the cursor. Must be a context manager.
        """
        pass
    
    
    def _log_cursor_messages(self, cursor: T_Cursor, messages_source: str|None):
        """
        Log messages produced during execution of a cursor. Use this if messages cannot be handled through `_register_cursor_messages_handler`.
        """
        pass

    _log_cursor_messages._do_nothing = True


    def _get_cursor_lastrowid(self, cursor: T_Cursor):
        raise NotImplementedError()

    #endregion


    #region Execute
    
    @overload
    def execute(self, query: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source = None, result: Literal[False] = ...) -> int:
        """ Execute a SQL statement, return the number of affected rows or -1 if none (cursor is entered and exited automatically). """
        ...

    @overload
    def execute(self, query: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source = None, result: Literal[True]) -> ResultContext[T_Connection, T_Cursor]:
        """ Execute a SQL statement, return the result context (must be entered and exited properly using `with`). """
        ...
    
    def execute(self, query: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source = None, result = False):
        the_result = self.cursor(query, params, limit=limit, offset=offset, warn_results=warn_results, messages_source=messages_source, result=True)
        if result:
            return the_result
        else:
            with the_result:
                return the_result.rowcount


    @overload
    def execute_file(self, file: str|os.PathLike, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source = None, encoding = 'utf-8', result: Literal[False] = ...) -> int:
        """ Execute a SQL file (possibly multi statement), return the total number of affected rows or -1 if none (cursor is entered and exited automatically). """
        ...

    @overload
    def execute_file(self, file: str|os.PathLike, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source = None, encoding = 'utf-8', result: Literal[True]) -> ResultContext[T_Connection, T_Cursor]:
        """ Execute a SQL file (possibly multi statement), return the result context (must be entered and exited properly using `with`). """
        ...
    
    def execute_file(self, file: str|os.PathLike, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source = None, encoding = 'utf-8', result = False, **file_kwargs):
        file_content = files.read_text(file, encoding=encoding)
        if file_kwargs:
            file_content = file_content.format(**{key: '' if value is None else value for key, value in file_kwargs.items()})
        
        a_result = None
        previous_rowcount = 0
        if self.split_multi_statement_files and ';' in file_content:
            # Split queries
            import sqlparse  # not at the top because the enduser might not need this feature
            queries = sqlparse.split(file_content, encoding)
            
            # Execute all queries
            query_count = len(queries)
    
            for index, query in enumerate(queries):
                if a_result is not None:
                    with a_result:
                        if not result:
                            rowcount = a_result.rowcount
                            if rowcount != -1:
                                previous_rowcount += rowcount
                
                query_num = index + 1
                if self._logger.isEnabledFor(logging.DEBUG):
                    query_start = re.sub(r"\s+", " ", query).strip()[0:100] + "…"
                    self._logger.debug("Execute query %d/%d: %s ...", query_num, query_count, query_start)
                if not messages_source:
                    messages_source = os.path.basename(file) + f' (query {query_num}/{query_count})'

                a_result = self.execute(query, params, limit=limit, offset=offset, warn_results=True if query_num < query_count else warn_results, messages_source=messages_source, result=True)
        else:
            if not messages_source:
                messages_source = os.path.basename(file)
            a_result = self.execute(file_content, params, limit=limit, offset=offset, warn_results=warn_results, messages_source=messages_source, result=True)
            
        # Handle last result
        if result:
            return a_result
        else:
            with a_result:
                rowcount = a_result.rowcount
                return previous_rowcount + (rowcount if rowcount != -1 else 0)
    

    def execute_function(self, name: str|tuple, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, warn_results: int|bool = False, messages_source = None, result = False, caller='SELECT', params_parenthesis=True):
        schema, name = self.split_name(name)
        
        query = f"{caller} "
        if not schema and self.function_requires_schema:
            schema = self.default_schema
        if schema:    
            query += f"{self.escape_identifier(schema)}."
        query += f"{self.escape_identifier(name)} "

        if params_parenthesis:
            query += "("
                
        if isinstance(params, abc.Mapping):
            list_params = []
            first = True
            for key, value in enumerate(params):
                if not key:
                    raise ValueError(f"Parameter cannot be empty")
                elif not re.match(r'^[\w\d0-9_]+$', key): # for safety
                    raise ValueError(f"Parameter contains invalid characters: {key}")
                
                if first:
                    first = False
                else:
                    query += ','

                query += f'{key}={self.sql_placeholder}'
                list_params.append(value)
            params = list_params
        elif params:
            query += ','.join([self.sql_placeholder] * len(params))
    
        if params_parenthesis:
            query += ")"

        if not messages_source:
            messages_source = (f'{schema}.' if schema else '') + name

        return self.execute(query, params, limit=limit, offset=offset, warn_results=warn_results, messages_source=messages_source, result=result)
    

    def execute_procedure(self, name: str|tuple, params: list|tuple|dict = None, *, limit: int = None, offset: int = None, warn_results: int|bool = 10, messages_source = None, result = False):
        return self.execute_function(name, params, limit=limit, offset=offset, warn_results=warn_results, messages_source=messages_source, result=result, caller=self.procedure_caller, params_parenthesis=self.procedure_params_parenthesis)


    #endregion


    #region Query helpers

    @classmethod
    def escape_identifier(cls, value: str|Header) -> str:
        if isinstance(value, Header):
            value = value.name
        elif not isinstance(value, str):
            raise TypeError(f"Invalid identifier: {value} ({type(value)})")
        return f"{cls.identifier_quotechar_begin}{value.replace(cls.identifier_quotechar_end, cls.identifier_quotechar_end+cls.identifier_quotechar_end)}{cls.identifier_quotechar_end}"
    

    @classmethod
    def escape_literal(cls, value) -> str:
        if value is None:
            return "null"
        else:
            return f"'" + str(value).replace("'", "''") + "'"
    

    def split_name(self, name: str|tuple|type = None) -> tuple[str|None,str]:
        if name is None:
            if not self.table:
                raise ValueError("No table given")
            schema = self.schema
            name = self.table        
        elif isinstance(name, tuple):
            schema, name = name
        elif isinstance(name, str):
            try:
                pos = name.index('.')
                schema = name[0:pos]
                name = name[pos+1:]
            except ValueError:
                schema = None
                name = name
        else:
            meta = getattr(name, '_meta', None) # Django model
            if meta:
                schema = None
                name: str = meta.db_table
            else:
                raise TypeError(f'name: {type(name).__name__}')
                    
        if schema == 'temp':
            if self.temp_schema == '#':
                schema = None
                name = f'#{name}'
            else:
                schema = self.temp_schema
        elif schema == '#' and self.temp_schema == '#': # sqlserver
            schema = None
            name = f'#{name}'

        return (schema, name)


    def to_supported_value(self, value: Any):
        """ Convert a value to types supported by the underlying connection. """        
        if isinstance(value, (Enum,Flag)):
            return value.value
        elif isinstance(value, (datetime,time)):
            if value.tzinfo:
                if self.accept_aware_datetime:
                    return value
                elif self.tz:
                    value = make_naive(value, self.tz)
                else:
                    raise ValueError(f"Cannot store tz-aware datetimes with {type(self).__name__} without providing `tz` argument")
            return value
        else:
            return value
    
    def to_positional_params(self, query: str, params: dict) -> tuple[str, Sequence[Any]]:
        from sqlparams import \
            SQLParams  # not at the top because the enduser might not need this feature

        if not hasattr(self.__class__, '_params_formatter'):
            self.__class__._params_formatter = SQLParams('named', 'qmark')
        query, params = self.__class__._params_formatter.format(query, params)

        return query, params
    

    def get_paginated_and_total_query(self, query: str, *, limit: int|None, offset: int|None) -> tuple[str,str]:        
        if limit is not None:
            if isinstance(limit, str) and re.match(r"^[0-9]+$", limit):
                limit = int(limit)
            elif not isinstance(limit, int):
                raise TypeError(f"Invalid type for limit: {type(limit).__name__} (expected int)")
            
        if offset is not None:
            if isinstance(offset, str) and re.match(r"^[0-9]+$", offset):
                offset = int(offset)
            elif not isinstance(offset, int):
                raise TypeError(f"Invalid type for offset: {type(limit).__name__} (expected int)")
        
        beforepart, selectpart, orderpart = self._split_select_query(query)

        paginated_query = beforepart
        total_query = beforepart
        
        paginated_query += self._paginate_splited_select_query(selectpart, orderpart, limit=limit, offset=offset)
        total_query += f"SELECT COUNT(*) FROM ({selectpart}) s"

        return paginated_query, total_query
    

    def _split_select_query(self, query: str):
        import sqlparse  # not at the top because the enduser might not need this feature

        # Parse SQL to remove token before the SELECT keyword
        # example: WITH (CTE) tokens
        statements = sqlparse.parse(query)
        if len(statements) != 1:
            raise sqlparse.exceptions.SQLParseError(f"Query contains {len(statements)} statements")

        # Get first DML keyword
        dml_keyword = None
        dml_keyword_index = None
        order_by_index = None
        for i, token in enumerate(statements[0].tokens):
            if token.ttype == sqlparse.tokens.DML:
                if dml_keyword is None:
                    dml_keyword = str(token).upper()
                    dml_keyword_index = i
            elif token.ttype == sqlparse.tokens.Keyword:
                if order_by_index is None:
                    keyword = str(token).upper()
                    if keyword == "ORDER BY":
                        order_by_index = i

        # Check if the DML keyword is SELECT
        if not dml_keyword:
            raise sqlparse.exceptions.SQLParseError(f"Not a SELECT query (no DML keyword found)")
        if dml_keyword != 'SELECT':
            raise sqlparse.exceptions.SQLParseError(f"Not a SELECT query (first DML keyword is {dml_keyword})")

        # Get part before SELECT (example: WITH)
        if dml_keyword_index > 0:
            tokens = statements[0].tokens[:dml_keyword_index]
            beforepart = ''.join(str(token) for token in tokens)
        else:
            beforepart = ''
    
        # Determine actual SELECT query
        if order_by_index is not None:
            tokens = statements[0].tokens[dml_keyword_index:order_by_index]
            selectpart = ''.join(str(token) for token in tokens)
            tokens = statements[0].tokens[order_by_index:]
            orderpart = ''.join(str(token) for token in tokens)
        else:
            tokens = statements[0].tokens[dml_keyword_index:]
            selectpart = ''.join(str(token) for token in tokens)
            orderpart = ''

        return beforepart, selectpart, orderpart
    

    def _paginate_splited_select_query(self, selectpart: str, orderpart: str, *, limit: int|None, offset: int|None) -> str:
        result = f"{selectpart} {orderpart}"
        if limit is not None:
            result += f" LIMIT {limit}"
        if offset is not None:
            result += f" OFFSET {offset}"
        return result
    

    def _get_select_table_query(self, table: str|tuple = None, *, schema_only = False) -> str:
        """
        Build a query on the given table.

        If `schema_only` is given, no row will be returned (this is used to get information on the table).
        Otherwise, all rows will be returned.

        The return type of this function depends on the database engine.
        It is passed directly to the cursor's execute function for this engine.
        """
        schema, table = self.split_name(table)
        
        query = f'SELECT * FROM'
        if schema:
            query += f' {self.escape_identifier(schema)}.'
        query += f'{self.escape_identifier(table)}'
        if schema_only:
            query += ' WHERE 1 = 0'

        return query   
    
    #endregion
    

    #region Result shortcuts

    def get_row(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None) -> TupleRow:        
        """Retrieve the first row from the query. Raise NotFoundError if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_row()
        

    def single_row(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None) -> TupleRow:        
        """Retrieve the result row from the query. Raise NotFoundError if there is no row or SeveralFound if there are more than one row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.single_row()
        
    
    def first_row(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None) -> TupleRow|None:
        """Retrieve the first row from the query. Return None if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.first_row()


    def get_vals(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_vals()


    def get_val(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_val()


    def single_val(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row or SeveralFound if there are more than one row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.single_val()


    def first_val(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None):
        """A convenience function for returning the first column of the first row from the query. Raise None if there is no row."""
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.first_val()
   

    def iter_dicts(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, limit: int = None, offset: int = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            yield from result.iter_dicts()
   

    def get_dicts(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, limit: int = None, offset: int = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_dicts()
   

    def paginate_dicts(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int, offset: int = 0):
        paginated_sql, total_query = self.get_paginated_and_total_query(sql, limit=limit, offset=offset)
        rows = self.get_dicts(paginated_sql, params)
        total = self.get_val(total_query, params)
        return {"rows": rows, "total": total}
    

    def get_dict(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.get_dict()
    

    def single_dict(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.single_dict()
    

    def first_dict(self, sql: str, params: Sequence[Any]|Mapping[str,Any]|None = None, *, limit: int = None, offset: int = None):
        with self.cursor(sql, params, limit=limit, offset=offset, result=True) as result:
            return result.first_dict()

    #endregion


    #region Inspect

    def schema_exists(self, schema: str = None) -> bool:        
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")
        raise NotImplementedError()


    def table_exists(self, table: str|tuple = None) -> bool:
        raise NotImplementedError()
    

    def get_columns(self, table_or_cursor: str|tuple|T_Cursor = None) -> tuple[str]:
        if table_or_cursor is None or isinstance(table_or_cursor, (str,tuple)):
            # table_or_cursor is assumed to be a table name (use self.table if None) 
            query = self._get_select_table_query(table_or_cursor, schema_only=True)
            with self.cursor() as cursor:
                cursor.execute(query)
                return self.get_columns(cursor)
        else:
            # table_or_cursor is assumed to be a cursor
            if not table_or_cursor.description:
                raise ValueError("No results in last executed query (no cursor description available)")
            return tuple(info[0] for info in table_or_cursor.description)


    def get_headers(self, object: str|tuple|T_Cursor = None, minimal = False) -> list[Header]:
        """
        Get the headers for the given table, cursor, or Django model.

        The following Header attributes are set (when possible):
        - `name`: set to the name of the table or cursor columns, or of the Django model columns.
        - `not_null`: indicate whether the column has a 'not null' constraint.
        
        If `minimal`, perform minimal queries, to get at least the type.
        """
        if object is None or isinstance(object, (str,tuple)): # `object` is assumed to be a table name (use `self.table` if `object` is `None`)
            return self._get_headers_from_table(object, minimal=minimal)

        elif isinstance(object, type): # `object` is assumed to be a Django model
            return self._get_headers_from_model(object, minimal=minimal)

        else: # `object` is assumed to be a cursor
            if not object.description:
                raise ValueError("No results in last executed query (no cursor description available)")
            return self._get_headers_from_cursor_description(object.description)
        

    def _get_headers_from_table(self, table: str|tuple|None = None, *, minimal = False):
        schema, table = self.split_name(table)

        headers: list[Header] = []
        for data in self._get_headers_data_from_table((schema, table), minimal=minimal):
            data.pop('ordinal', None)
            
            _type = None
            if 'type_identifier' in data:
                type_identifier = data.pop('type_identifier')
                _type = self._get_type_from_identifier(type_identifier)
                data['type'] = _type

            if 'unique' in data:
                unique = data['unique']
                
                if isinstance(unique, str):
                    unique = unique.split(';')
                    for i in range(len(unique)):
                        unique[i] = unique[i].split(',')

                if isinstance(unique, list):
                    if len(unique) == 1 and unique[0] == [data['name']]:
                        unique = True
                
                data['unique'] = unique

            if 'default' in data:
                default = data['default']
                if isinstance(default, str):
                    if default == '(getdate())' or default == 'now()':
                        default = Header.DEFAULT_NOW
                    else:
                        m = re.match(r"^\((.+)\)$", default) # sqlserver-specific
                        if m:
                            default = m[1]
                            m = re.match(r"^\((.+)\)$", default) # second level (e.g. for integer value)
                            if m:
                                default = m[1]
                        m = re.match(r"^'(.+)'(?:::[a-z0-9 ]+)?$", default) # note: `::type` is postgresql-specific
                        if m:
                            default = re.sub(r"''", "'", m[1]) # remove quotes

                if default != Header.DEFAULT_NOW and _type is not None:
                    default = convert(default, _type)
                
                data['default'] = default

            for key in ['not_null', 'primary_key', 'unique', 'identity']:
                if key in data and isinstance(data[key], int):
                    if data[key] == 0:
                        data[key] = False
                    elif data[key] == 1:
                        data[key] = True
                    else:
                        raise ValueError(f"Invalid integer value for \"{key}\": \"{data[key]}\" in {data}")
            
            header = Header(**data)
            headers.append(header)
        
        return headers
    

    def _get_headers_data_from_table(self, table, *, minimal: bool) -> Iterable[dict[str,Any]]:
        raise NotImplementedError()
    

    def _get_headers_from_model(self, model, *, minimal = False) -> Iterable[Header]:
        from django.db import models

        field: models.Field
       
        headers: dict[str,Header] = {}

        for field in model._meta.fields:
            header = Header(field.attname)

            _type = _get_django_field_python_type(field)
            if _type:
                header.type = _type
                if isinstance(field, models.DecimalField):
                    header.precision = field.max_digits
                    header.scale = field.decimal_places
                elif isinstance(field, models.CharField):
                    header.precision = field.max_length

            header.not_null = not field.null

            if field.primary_key:
                header.primary_key = True
            if field.unique:
                header.unique = True

            headers[header.name] = header

        if not minimal:
            unique_keys = _get_django_model_unique_keys(model)
            for key in unique_keys:
                if len(key) == 1:
                    header = headers[key[0]]
                    header.unique = True
                else:
                    for field in key:
                        header = headers[field]
                        if not headers[field].unique:
                            header.unique = [key]
                        elif not headers[field].unique is True:
                            header.unique.append(key)

        return headers.values()


    def _get_headers_from_cursor_description(self, cursor_description) -> list[Header]:
        headers = []

        for name, type_identifier, display_size, internal_size, precision, scale, nullable in cursor_description:
            actual_type = self._get_type_from_identifier(type_identifier)
            if actual_type == str and precision is None and display_size is not None: # for postgresql
                precision = display_size

            if isinstance(nullable, int):
                if nullable == 1:
                    nullable = True
                elif nullable == 0:
                    nullable = False
               
            header = Header(name, type=actual_type, precision=precision, scale=scale, not_null=not nullable if isinstance(nullable, bool) else None)
            headers.append(header)
        
        return headers
    
    
    def _get_type_from_identifier(self, type_identifier: type|str|int) -> type|None:
        if isinstance(type_identifier, type):
            return type_identifier
        raise NotImplementedError()
    

    def get_sql_type(self, _type: type|Header, precision: int|None = None, scale: int|None = None, *, key: bool|None = None) -> str:
        if isinstance(_type, Header):
            header = _type
            if header.sql_type:
                return header.sql_type
            
            _type = header.type
            if precision is None:
                precision = header.precision
            if scale is None:
                scale = header.scale
            if key is None:
                key = True if header.unique else False
            if _type is None:
                if header.default is not None:
                    if header.default == header.DEFAULT_NOW:
                        _type = datetime
                    else:
                        _type = type(header.default)
                else:
                    _type = str
        elif not isinstance(_type, type):
            raise TypeError(f"_type: {type(_type)}")
        
        if issubclass(_type, bool):
            sql_basetype = self.bool_sql_basetype
        elif issubclass(_type, int):
            sql_basetype = self.int_sql_basetype
        elif issubclass(_type, float):
            sql_basetype = self.float_sql_basetype
        elif issubclass(_type, Decimal):
            if self.decimal_sql_basetype == 'text':
                sql_basetype = self.decimal_sql_basetype
            else:
                if precision is None:
                    raise ValueError("Precision must be set for decimal values")
                if scale is None:
                    raise ValueError("Scale must be set for decimal values")
                sql_basetype = self.decimal_sql_basetype
        elif issubclass(_type, datetime):
            sql_basetype = self.datetime_sql_basetype
        elif issubclass(_type, date):
            sql_basetype = self.date_sql_basetype
        else: # use str
            if precision is not None:
                sql_basetype = self.str_precised_sql_basetype
            elif key:
                sql_basetype = self.str_precised_sql_basetype
                precision = 255 # type for key limited to 255 characters (max length for a 1-bit length VARCHAR on MariaDB)
            else:
                sql_basetype = self.str_sql_basetype

        sql_type = sql_basetype
        if precision is not None or scale is not None:
            sql_type += '('
            if precision is not None:
                sql_type += str(precision)                
            if scale is not None:
                if precision is not None:
                    sql_type += ','
                sql_type += str(scale)
            sql_type += ')'

        return sql_type


    def get_sql_column_definition(self, column: Header|str, *, ignore_decimal = False, ignore_not_null = False):
        if not isinstance(column, Header):
            column = Header(column)

        if ignore_decimal and column.type and issubclass(column.type, (float,Decimal)):
            sql_type = 'varchar(100)'
        else:
            sql_type = self.get_sql_type(column)
            
        if column.primary_key or column.identity:
            not_null = True
        elif ignore_not_null:
            not_null = False
        else:
            not_null = column.not_null
        
        sql = f"{self.escape_identifier(column.name)} {sql_type} {'NOT NULL' if not_null else 'NULL'}"

        if column.default is not None:
            sql += f" DEFAULT {self.get_sql_escaped_default(column.default)}"

        return sql
    

    def get_sql_escaped_default(self, default):
        if default is None:
            return 'null'
        elif default == Header.DEFAULT_NOW:
            return 'CURRENT_TIMESTAMP'
        elif isinstance(default, str) and default.startswith('sql:'):
            return default[len('sql:'):]
        else:
            return self.escape_literal(default)
    
    #endregion


    #region DDL
    
    def drop_table(self, table: str|tuple = None, *, if_exists = False, loglevel = logging.DEBUG):
        schema, table = self.split_name(table)
        
        query = "DROP TABLE "
        if if_exists:
            query += "IF EXISTS "
        if schema:    
            query += f"{self.escape_identifier(schema)}."
        query += f"{self.escape_identifier(table)}"

        self._logger.log(loglevel, "Drop table %s%s", f'{schema}.' if schema else '', table)
        self.execute(query)


    def clear_table(self, table: str|tuple|type = None, *, scope: str|None = None, truncate: bool|Literal['cascade'] = False, if_exists = False, loglevel = logging.DEBUG):
        schema, table = self.split_name(table)

        if if_exists:
            if not self.table_exists((schema, table)):
                return
        
        if scope or not truncate or self.truncate_with_delete:
            query = "DELETE FROM "
        else:
            query = "TRUNCATE "
               
        if schema:    
            query += f"{self.escape_identifier(schema)}."
        query += f"{self.escape_identifier(table)}"

        if scope:
            query += " WHERE scope = %s"
            params = [scope]
        else:
            if truncate == 'cascade':
                if self.truncate_with_delete:
                    raise ValueError("Cannot clear with truncate")
                query += " CASCADE"
            params = []
        
        self._logger.log(loglevel, "Clear table %s%s", f'{schema}.' if schema else '', table)
        self.execute(query, params)


    def create_table(self, table: str|tuple, columns: Iterable[str|Header], *, ignore_decimal = False, ignore_not_null = False, if_not_exists = False, loglevel = logging.DEBUG):
        """
        Create a table from a list of columns.

        NOTE: This method does not intend to manage all cases, but only those usefull for zut library internals.
        """
        schema, table = self.split_name(table)
        
        columns = [Header(column) if not isinstance(column, Header) else column for column in columns]

        sql = "CREATE "
        if schema in {self.temp_schema, 'temp'}:
            sql += "TEMPORARY "
        sql += "TABLE "
        if if_not_exists:
            sql += "IF NOT EXISTS "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += f"{self.escape_identifier(table)}("

        primary_key: tuple[str] = tuple(sorted(column.name for column in columns if column.primary_key))

        unique_keys: list[tuple[str]] = []    
        for column in columns:
            if column.unique:
                if column.unique is True:
                    key = (column.name,)
                    if not key in unique_keys and key != primary_key:
                        unique_keys.append(key)
                else:
                    for key in column.unique:
                        if not key in unique_keys and key != primary_key:
                            unique_keys.append(key)

        for i, column in enumerate(columns):
            sql += (',' if i > 0 else '') + self.get_sql_column_definition(column, ignore_decimal=ignore_decimal, ignore_not_null=ignore_not_null)
            if len(primary_key) == 1 and primary_key[0] == column.name:
                sql += " PRIMARY KEY"
            if column.identity:
                sql += f" {self.identity_definition_sql}"

        # Multi primary keys ?
        if len(primary_key) > 1:
            sql += ",PRIMARY KEY("
            for i, column in enumerate(primary_key):
                sql += ("," if i > 0 else "") + f"{self.escape_identifier(column)}"
            sql += ")" # end PRIMARY KEY

        # Unique together ?
        for unique_key in unique_keys:
            sql += ",UNIQUE("
            for i, key in enumerate(unique_key):
                sql += ("," if i > 0 else "") + f"{self.escape_identifier(key)}"
            sql += ")" # end UNIQUE
        
        sql += ")" # end CREATE TABLE

        self._logger.log(loglevel, "Create table %s%s", f'{schema}.' if schema else '', table)
        self.execute(sql)


    def append_column(self, table: str|tuple, columns: list[str|Header], *, ignore_decimal = False, ignore_not_null = False, loglevel = logging.DEBUG):
        """
        Add column(s) to a table.

        NOTE: This method does not intend to manage all cases, but only those usefull for zut library internals.
        """
        if len(columns) > 1 and not self.can_add_several_columns:
            for column in columns:
                self.append_column(table, [column], ignore_decimal=ignore_decimal, ignore_not_null=ignore_not_null, loglevel=loglevel)
            return

        schema, table = self.split_name(table)
        
        sql = "ALTER TABLE "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += self.escape_identifier(table)
        sql += f" ADD "
        for i, column in enumerate(columns):
            if isinstance(column, Header):
                if column.primary_key:
                    raise NotImplementedError(f"Cannot append primary key column: {column.name}")
                if column.unique:
                    raise NotImplementedError(f"Cannot append unique column: {column.name}")
                if column.identity:
                    raise NotImplementedError(f"Cannot append identity column: {column.name}")
            sql += (',' if i > 0 else '') + self.get_sql_column_definition(column, ignore_decimal=ignore_decimal, ignore_not_null=ignore_not_null)

        self._logger.log(loglevel, "Append column%s %s to table %s%s", ('s' if len(columns) > 1 else '', ', '.join(str(column) for column in columns)), f'{schema}.' if schema else '', table)        
        self.execute(sql)


    def alter_column_default(self, table: tuple|str|type, columns: Iterable[Header]|dict[str,Any], *, loglevel = logging.DEBUG):
        schema, table = self.split_name(table)

        if isinstance(columns, dict):
            columns = [Header(name, default=default) for name, default in columns.items()]

        columns_sql = ''
        columns_names: list[str] = []
        only_reset = True
        for column in columns:
            columns_sql = (", " if columns_sql else "") + f"ALTER COLUMN {self.escape_identifier(column.name)} "
            if column.default is None:
                columns_sql += "DROP DEFAULT"
            else:
                columns_sql += f"SET DEFAULT {self.get_sql_escaped_default(column)}"
                only_reset = False
            columns_names.append(f'"{column.name}"')

        if not columns_sql:
            return
    
        sql = "ALTER TABLE "
        if schema:
            sql += f"{self.escape_identifier(schema)}."
        sql += f"{self.escape_identifier(table)} {columns_sql}"

        self._logger.log(loglevel, "%s default for column%s %s of table %s%s", 'Reset' if only_reset else 'Alter', 's' if len(columns_names) > 1 else '', ', '.join(columns_names), f'{schema}.' if schema else '', table)
        self.execute(sql)
    

    def get_temp_table_name(self, basename: str):
        while True:
            name = f"{slugify(basename, separator='_')[:40]}_tmp_{token_hex(4)}"
            if not self.table_exists((self.temp_schema, name)):
                return name
   

    def drop_schema(self, schema: str = None, *, if_exists = False, loglevel = logging.DEBUG):
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")
        
        if not schema:
            schema = self.schema or self.default_schema
            if not schema:
                raise ValueError("No schema defined for this Db")
        
        query = "DROP SCHEMA "
        if if_exists:
            query += "IF EXISTS "
        query += f"{self.escape_identifier(schema)}"
        
        self._logger.log(loglevel, "Drop schema %s", schema)
        self.execute(query)
    

    def create_schema(self, schema: str = None, *, if_not_exists = False, loglevel = logging.DEBUG):
        if self.default_schema is None:
            raise ValueError("This Db does not support schemas")

        if not schema:
            schema = self.schema or self.default_schema
            if not schema:
                raise ValueError("No schema defined for this Db")
        
        query = "CREATE SCHEMA "
        if if_not_exists:
            if self.scheme == 'sqlserver':
                if self.schema_exists(schema):
                    return
            else:
                query += "IF NOT EXISTS "
        query += f"{self.escape_identifier(schema)}"
        
        self._logger.log(loglevel, "Create schema %s", schema)
        self.execute(query)

    # endregion


    #region Non-Django migrations

    def migrate(self, dir: str|os.PathLike, **file_kwargs):        
        last_name = self.get_last_migration_name()

        if last_name is None:
            sql_utils = self.get_sqlutils_path()
            if sql_utils:
                self._logger.info("Deploy SQL utils ...")
                self.execute_file(sql_utils)

            self._logger.info("Create migration table ...")
            self.execute(f"CREATE TABLE migration(id {self.int_sql_basetype} NOT NULL PRIMARY KEY {self.identity_definition_sql}, name {self.get_sql_type(str, key=True)} NOT NULL UNIQUE, deployed_utc {self.datetime_sql_basetype} NOT NULL)")
            last_name = ''
        
        for path in sorted((dir if isinstance(dir, Path) else Path(dir)).glob('*.sql')):
            if path.stem == '' or path.stem.startswith('~') or path.stem.endswith('~'):
                continue # skip
            if path.stem > last_name:
                self._apply_migration(path, **file_kwargs)

        self.connection.commit()


    def _apply_migration(self, path: Path, **file_kwargs):
        self._logger.info("Apply migration %s ...", path.stem)

        self.execute_file(path, **file_kwargs)
        self.execute(f"INSERT INTO migration (name, deployed_utc) VALUES({self.sql_placeholder}, {self.sql_placeholder})", [path.stem, self.to_supported_value(now_naive_utc())])


    def get_last_migration_name(self) -> str|None:
        if not self.table_exists("migration"):
            return None
        
        try:
            return self.get_val("SELECT name FROM migration ORDER BY name DESC", limit=1)
        except NotFoundError:
            return ''

    #endregion


    #region Check if available
                
    def is_available(self, *, migration: tuple[str,str]|str = None):
        if migration:
            if isinstance(migration, tuple):
                migration_app, migration_name = migration
            else:
                pos = migration.index(':')
                migration_app = migration[:pos]
                migration_name = migration[pos+1:]
        
        try:
            with self.cursor():
                if migration:
                    from django.db.migrations.recorder import MigrationRecorder
                    recorder = MigrationRecorder(self.connection)
                    recorded_migrations = recorder.applied_migrations()
                    for an_app, a_name in recorded_migrations.keys():
                        if an_app == migration_app and a_name == migration_name:
                            return True
                    return False
                else:
                    return True
        except:
            return False
        
    #endregion


    #region Load (copy and merge)

    def load_from_csv(self,
                    csv_files: Path|str|IOBase|list[Path|str|IOBase],
                    table: str|tuple|type = None,
                    *,
                    headers: list[Header|str]|None = None,
                    optional: str|Sequence[str]|Literal['*',True]|None = None,
                    snake_case: bool|None = None,
                    merge: Literal['append','truncate','create','recreate','auto','auto|append','auto|truncate']|tuple[Header|str]|list[Header|str] = 'auto',
                    create_model: str|tuple|type|list[Header] = None,
                    create_pk: bool|str = None,
                    create_additional: dict[str|Any]|list[Header] = None,
                    mark_missing: bool|str = None,
                    consts: dict[str|Any] = None,
                    insert_consts: dict[str|Any] = None,
                    foreign_keys: list[FK] = None,
                    # CSV format
                    encoding = 'utf-8',
                    delimiter: str = None,
                    decimal_separator: str = None,
                    quotechar = '"',
                    nullval: str = None,
                    no_headers: bool = None,
                    # Title and file helpers (similar to zut.load_tabular())                            
                    title: str|bool = False,
                    src_name: str|bool|None = None,
                    dir: str|Path|Literal[False]|None = None,
                    **kwargs) -> int:
        """
        Load CSV file(s) to a table. The table will be created if it does not already exist.
        
        - `headers`: list of CSV headers to use. If not provided, headers will be determined from the first line of the first input CSV file.
        
        - `optional`: optional headers will be discared if they do not exist in the destination.

        - `merge`:
            - If `append`, data will simply be appended.
            - If `truncate`, destination table will be created if it does not already exist, or truncated if it already exists.
            - If `create`, destination table will be created if it does not already exist. Data will simply be appended.
            - If `recreate`, destination table will be droped if exist, and (re)created.
            - If a tuple (or list), reconciliate using the given header names as keys.
            - If `auto` or `auto|append` (default):
                - [`id`] if header `id` is present in the CSV headers;
                - or the first unique key found in `create_model` if given;
                - or the first unique key in the destination table;
                - or (if there is no unique key): `append`.
            - If `auto|truncate`, same as `auto` but if no key is found, truncate destination table before.

        - `create_pk`: if a non-empty string or True (means `id`), destination table will be created (if necessary) with
        an auto-generated primary key named as the value of `create_pk`, if it is not already in CSV headers.

        - `create_model`: can be a Django model, the name (or tuple) of a table, or a list of columns. If set, destination
        table will be created (if necessaray) with SQL types and unique keys matching `create_model` columns.

        - `create_additional`: can be a dictionnary (column name: default value) or a list of columns. If set, destination
        table will be created (if necessary) with these columns (in addition to those provided by `create_model` if any).

        - `consts`: set constant values when a row is inserted or updated (during a merge). If the colunm name (key of the
        dictionnary) ends with '?', there will first be a check that the column exist and the constant will be ignored
        if the column does not exist.

        - `insert_consts`: same as `consts` but only set when a row is inserted.
        """

        # Prepare csv_files and table parameters
        target_model = None
        if not table:
            if not self.table:
                raise ValueError("No table given")
            schema, table = self.split_name(table)
        elif isinstance(table, (str,tuple)):
            schema, table = self.split_name(table)
        elif isinstance(table, type): # Django model
            target_model = table
            schema = self.default_schema
            table = table._meta.db_table
        else:
            raise TypeError(f"table: {table}")

        if isinstance(csv_files, (Path,str,IOBase)):
            csv_files = [csv_files]
        if not csv_files:
            raise ValueError("csv_files cannot be empty")
        for i in range(len(csv_files)):
            if not isinstance(csv_files[i], IOBase):
                if dir is not False:
                    csv_files[i] = files.indir(csv_files[i], dir, title=title, **kwargs)
                if not files.exists(csv_files[i]):
                    raise FileNotFoundError(f"Input CSV file does not exist: {csv_files[i]}")
                
        if title:
            if src_name is None or src_name is True:
                if len(csv_files) == 1:
                    src = csv_files[0]
                    if isinstance(src, IOBase):
                        src_name = getattr(src, 'name', f'<{type(src).__name__}>')
                    else:
                        src_name = src
            self._logger.info(f"Load{f' {title}' if title and not title is True else ''}{f' from {src_name}' if src_name else ''} …")
        
        # Determine merge param
        if merge is None or (isinstance(merge, str) and merge in {'auto', 'auto|append', 'auto|truncate'}):
            merge = self.get_load_auto_key(target_model or (schema, table), headers=headers or csv_files[0], convert_to_available=not target_model, default='truncate' if 'truncate' in merge else 'append', snake_case=snake_case, encoding=encoding, delimiter=delimiter, quotechar=quotechar)
        elif isinstance(merge, (list,tuple)):
            merge = tuple(column.name if isinstance(column, Header) else column for column in merge)            
            for i, column in enumerate(merge):
                if not isinstance(column, str):
                    raise TypeError(f"merge[{i}]: {type(column).__name__}")
        elif isinstance(merge, str):
            if not merge in {'append', 'truncate', 'create', 'recreate'}:
                raise ValueError(f"Invalid merge value: {merge}")
        else:
            raise TypeError(f"merge: {type(merge).__name__}")
        
        # Determine CSV parameters and headers
        if not delimiter:
            if isinstance(merge, self._LoadCacheMixin):
                delimiter = merge._delimiter

        if not delimiter or (not headers and not no_headers):
            examined_columns, examined_delimiter, _ = examine_csv_file(csv_files[0], encoding=encoding, delimiter=delimiter, quotechar=quotechar, force_delimiter=False)
            if not delimiter:
                delimiter = examined_delimiter or get_default_decimal_separator()
            if not headers and not no_headers:
                headers = examined_columns

        if not decimal_separator:
            decimal_separator = get_default_decimal_separator(csv_delimiter=delimiter)

        if not headers and isinstance(merge, self._LoadCacheMixin):
            headers = merge._headers

        if headers:
            headers = [header if isinstance(header, Header) else Header(header) for header in headers]

        if optional:
            if optional == '*':
                optional = True
            elif isinstance(optional, str):
                optional = [str]

        columns: dict[str,str] = {}
        for header in headers:
            columns[header.name] = slugify_snake(header.name) if snake_case else header.name

        has_optional_headers = False
        
        # Add foreign keys from Django model
        if target_model and foreign_keys is None:
            foreign_keys = self._get_load_foreign_keys(columns.values(), target_model)

        foreign_keys_by_source_column_name: dict[str,FK] = {}
        if foreign_keys:
            for foreign_key in foreign_keys:
                for column in foreign_key.source_columns:
                    foreign_keys_by_source_column_name[column] = foreign_key

        # Start transaction with database
        total_rowcount = 0
        with self.transaction():
            # Determine if we must (re)create the destination table
            if isinstance(merge, self._LoadCacheMixin) and merge._model_table_exists is not None and merge._model == (schema, table):
                table_existed = merge._model_table_exists
            else:
                table_existed = self.table_exists((schema, table))

            if table_existed:
                if merge == 'recreate':
                    self._logger.debug(f"Drop table {f'{schema}.' if schema else ''}{table}") 
                    self.drop_table((schema, table))                        
                    must_create = True
                else:
                    must_create = False
            else:
                must_create = True

            # Create the destination table
            if must_create:
                if not headers:
                    raise ValueError(f"Cannot create table without headers")

                # (adapt headers to `create_model`)
                if create_model:
                    if isinstance(create_model, str):
                        create_model = self.split_name(create_model)
                    
                    if isinstance(merge, self._LoadCacheMixin) and merge._model_columns_by_name is not None and merge._model == create_model:
                        model_columns_by_name = merge._model_columns_by_name
                    else:
                        model_columns_by_name = self._get_load_model_columns_by_name(create_model)

                    for column in headers:
                        model_column = model_columns_by_name.get(column.name)
                        if model_column:
                            if model_column.identity:
                                raise ValueError("Cannot load an identity column")
                            column.merge(model_column)
                
                # (ensure a unique key is created for the merge key)
                if isinstance(merge, tuple):
                    for column in headers:
                        if column.name in merge:
                            if not column.unique:
                                column.unique = [merge]
                            elif isinstance(column.unique, list):
                                if not merge in column.unique:
                                    column.unique.append(merge)

                destination_columns_by_name: dict[str,Header] = {}
                for header in headers:
                    foreign_key = foreign_keys_by_source_column_name.get(header.name)
                    if foreign_key:
                        if foreign_key.destination_column not in destination_columns_by_name:
                            column = Header(foreign_key.destination_column)
                            column.type = foreign_key.related_pk_type if foreign_key.related_pk_type else int
                            destination_columns_by_name[header.name] = column
                    else:
                        destination_columns_by_name[header.name] = header

                if create_additional:
                    if isinstance(create_additional, dict):
                        create_additional: list[Header] = [Header(name, default=default, not_null=default is not None) for (name, default) in create_additional.items()]
                    else:
                        for i in range(len(create_additional)):
                            if not isinstance(create_additional[i], Header):
                                create_additional[i] = Header(create_additional)

                    for column in create_additional:
                        if not column.name in destination_columns_by_name:
                            destination_columns_by_name[column.name] = column

                if create_pk:
                    if not isinstance(create_pk, str):
                        create_pk = 'id'
                    pk_found = False

                    for column in headers:
                        if column.primary_key or column.name == create_pk:
                            pk_found = True
                            column.primary_key = True

                    if not pk_found:
                        pk_column = Header(create_pk, primary_key=True, identity=True, sql_type='bigint')
                        destination_columns_by_name = {pk_column.name: pk_column, **destination_columns_by_name}
                        
                self._logger.debug(f"Create destination table {f'{schema}.' if schema else ''}{table}")
                if schema:
                    self.create_schema(schema, if_not_exists=True)
                self.create_table((schema, table), destination_columns_by_name.values())

            # Update headers with types from existing destination table
            else:
                if isinstance(merge, self._LoadCacheMixin) and merge._model_columns_by_name is not None and merge._model == (schema, table):
                    destination_columns_by_name = merge._model_columns_by_name
                else:
                    destination_columns_by_name = {column.name: column for column in self.get_headers((schema, table), minimal=True)}

                # (select headers that are in destination table or foreign keys, if optional is set)
                columns = {}
                for header in headers:
                    column = destination_columns_by_name.get(header.name)
                    if column:
                        header.merge(column)
                        columns[header.name] = slugify_snake(header.name) if snake_case else header.name
                    else:
                        foreign_key = foreign_keys_by_source_column_name.get(header.name)
                        if foreign_key:
                            if foreign_key.related_pk_type:
                                header.type = foreign_key.related_pk_type
                            columns[header.name] = slugify_snake(header.name) if snake_case else header.name
                        elif optional and (optional is True or header.name in optional):
                            has_optional_headers = True
                        else:
                            columns[header.name] = slugify_snake(header.name) if snake_case else header.name
                
            # Remove optional consts if necessary
            def remove_optional_consts(consts: dict[str,Any]):
                if any(name.endswith('?') for name in consts.keys()):
                    new_consts = {}
                    for name, value in consts.items():
                        is_optional = name.endswith('?')
                        actual_name = name[:-1] if is_optional else name
                        if not is_optional or actual_name in destination_columns_by_name:
                            new_consts[actual_name] = value
                    return new_consts
                else:
                    return consts

            if consts:
                consts = remove_optional_consts(consts)
                    
            if insert_consts:
                insert_consts = remove_optional_consts(insert_consts)

            # Determine if we must perform conversions at load time
            conversions: dict[str,Header] = {}
            if headers:
                for header in headers:
                    if header.type:
                        dst_column_name = slugify_snake(header.name) if snake_case else header.name
                        if issubclass(header.type, (float,Decimal)) :
                            if decimal_separator != '.':
                                conversions[dst_column_name] = header
                        elif issubclass(header.type, datetime):
                            if self.tz:
                                conversions[dst_column_name] = header
                        elif issubclass(header.type, list):
                            conversions[dst_column_name] = header
                
            # Truncate destination table
            if merge == 'truncate':
                if table_existed:
                    if self._logger.isEnabledFor(logging.DEBUG):
                        self._logger.debug(f"Truncate table {f'{schema}.' if schema else ''}{table}") 
                    self.clear_table((schema, table), truncate=True)
            
            # Prepare temporary table if we're reconciliating
            if (isinstance(merge, tuple) and table_existed) or has_optional_headers or conversions or consts or insert_consts or foreign_keys:
                temp_table = self.get_temp_table_name(table)
                self.drop_table(temp_table, if_exists=True)                    
                self._logger.debug(f"Create {temp_table}")                                
                if not headers:
                    raise ValueError(f"Cannot create table without headers")
                self.create_table(temp_table, [Header(header.name, sql_type=self.str_sql_basetype if header.name in conversions else header.sql_type) for header in headers])
            else:
                temp_table = None # load directly to destination table
                
            # Perform actual copy of CSV files
            for csv_file in csv_files:                        
                if temp_table: # copy to temporary table if we're reconciliating
                    self._logger.debug(f"Load {temp_table} from csv file {csv_file}")
                    total_rowcount += self.copy_from_csv(csv_file, temp_table, headers, encoding=encoding, delimiter=delimiter, quotechar=quotechar, nullval=nullval, no_headers=no_headers)
                else:
                    self._logger.debug(f"Load table {f'{schema}.' if schema else ''}{table} from csv file {csv_file}")
                    total_rowcount += self.copy_from_csv(csv_file, (schema, table), headers, encoding=encoding, delimiter=delimiter, quotechar=quotechar, nullval=nullval, no_headers=no_headers)

            # Merge from temporary table to destination table if we're reconciliating
            if temp_table:
                if self._logger.isEnabledFor(logging.DEBUG):
                    msg = f"Merge {temp_table} to {f'{schema}.' if schema else ''}{table}"
                    if isinstance(merge, tuple):
                        msg += f" using key {', '.join(merge)}"
                    self._logger.debug(msg)
                
                self.merge_table(temp_table, (schema, table),
                                 columns=columns,
                                 key=merge if isinstance(merge, tuple) else None,
                                 mark_missing=mark_missing,
                                 consts=consts,
                                 insert_consts=insert_consts,
                                 foreign_keys=foreign_keys,
                                 conversions=conversions)
                
                self._logger.debug("Drop %s", temp_table)
                self.drop_table(temp_table)

        if title:
            self._logger.info(f"{total_rowcount:,}{f' {title}' if title and not title is True else ''} rows imported{f' from {src_name}' if src_name else ''}")
        
        return total_rowcount


    def copy_from_csv(self,
                    csv_file: Path|str|IOBase,
                    table: str|tuple = None,
                    headers: list[Header|str] = None,
                    *,
                    buffer_size = 65536,
                    # CSV format
                    encoding = 'utf-8',
                    delimiter: str = None,
                    quotechar = '"',
                    nullval: str = None,
                    no_headers: bool = None) -> int:
        
        raise NotImplementedError() 


    def merge_table(self,
                    src_table: str|tuple,
                    dst_table: str|tuple|None = None,
                    columns: Sequence[Header|str]|Mapping[Header|str,Header|str] = None,
                    *,
                    key: str|tuple[str]|None = None,
                    mark_missing: bool|str|None = None,
                    consts: dict[str|Any]|None = None,
                    insert_consts: dict[str|Any]|None= None,
                    foreign_keys: list[FK]|None = None,
                    conversions: dict[str,str|type|Header] = {}):
        
        # Prepare table arguments
        src_schema, src_table = self.split_name(src_table)

        if not dst_table:
            if not self.table:
                raise ValueError("No table given")
            dst_table = self.table
        dst_schema, dst_table = self.split_name(dst_table)

        # Prepare columns argument
        if columns:
            if isinstance(columns, abc.Mapping):
                columns = {src_column if isinstance(src_column, Header) else src_column: dst_column if isinstance(dst_column, Header) else dst_column for src_column, dst_column in columns.items()}
            else:
                columns = {column.name if isinstance(column, Header) else column: column.name if isinstance(column, Header) else column for column in columns}
        else:
            columns = {column: column for column in self.get_columns((src_schema, src_table))}

        foreign_keys_column_names = set()
        if foreign_keys:
            for foreing_key in foreign_keys:
                for column in foreing_key.source_columns:
                    foreign_keys_column_names.add(column)
        
        # Prepare SQL parts
        key_sql = ""
        if key:
            if isinstance(key, str):
                key = [key]
            for key_column in key:
                key_sql += (", " if key_sql else "") + self.escape_identifier(key_column)

        from_sql = (f"{self.escape_identifier(src_schema)}." if src_schema else "") + f"{self.escape_identifier(src_table)} s"

        insert_sql = ""
        select_sql = ""
        join_sql = ""
        set_sql = ""
        foreign_key_check_sqls: list[str] = []
        naive_tzkey = None

        def append_standard_column(src_column: str, dst_column: str):
            nonlocal insert_sql, select_sql, set_sql, naive_tzkey

            conversion_fmt = '{value}'
            conversion = conversions.get(src_column)
            if conversion:
                if isinstance(conversion, Header):
                    conversion = self.get_sql_type(conversion)
                elif isinstance(conversion, type):
                    if issubclass(conversion, Decimal):
                        conversion = self.float_sql_basetype # we cannot use decimal because we don't know precision and scale
                    else:
                        conversion = self.get_sql_type(conversion)
                elif not isinstance(conversion, str):
                    raise TypeError(f"conversions[{src_column}]: {conversion}")
                
                if '{value}' in conversion:
                    conversion_fmt = conversion
                else:                
                    conversion = conversion.lower()
                    if conversion.endswith('[]'): # array
                        conversion_fmt = "CAST(string_to_array({value}, '|') AS "+conversion+")"
                    elif conversion.startswith(('float','double','real','decimal','numeric')):
                        conversion_fmt = "CAST(replace(replace({value}, ',', '.'), ' ', '') AS "+conversion+")"
                    elif conversion == 'timestamptz':
                        if not naive_tzkey:
                            if not self.tz:
                                raise ValueError("Cannot convert to timestamptz when tz not set")
                            naive_tzkey = get_tzkey(self.tz)
                        conversion_fmt = "CAST(CASE WHEN {value} SIMILAR TO '%[0-9][0-9]:[0-9][0-9]' AND SUBSTRING({value}, length({value})-5, 1) IN ('-', '+') THEN {value}::timestamptz ELSE {value}::timestamp AT TIME ZONE "+self.escape_literal(naive_tzkey)+" END AS "+conversion+")"
                    else:
                        conversion_fmt = "CAST({value} AS "+conversion+")"

            escaped_src_column_name = self.escape_identifier(src_column)
            escaped_dst_column_name = self.escape_identifier(dst_column)

            insert_sql += (", " if insert_sql else "")       
            select_sql += (", " if select_sql else "")
            insert_sql += escaped_dst_column_name
            select_sql += conversion_fmt.format(value=f"s.{escaped_src_column_name}")

            if key and not dst_column in key:
                set_sql += (", " if set_sql else "") + f"{escaped_dst_column_name} = excluded.{escaped_dst_column_name}"

        def append_consts(consts: dict[str,Any], *, insert_only = False):
            nonlocal insert_sql, select_sql, set_sql

            if not consts:
                return
            
            for column_name, value in consts.items():
                escaped_column_name = self.escape_identifier(column_name)
                if value == Header.DEFAULT_NOW:
                    escaped_literal = 'CURRENT_TIMESTAMP'
                elif isinstance(value, str) and value.startswith('sql:'):
                    escaped_literal = value[len('sql:'):]
                else:
                    escaped_literal = self.escape_literal(value)

                insert_sql += (", " if insert_sql else "") + escaped_column_name
                select_sql += (", " if select_sql else "") + escaped_literal
                if not insert_only:
                    set_sql += (", " if set_sql else "") + f"{escaped_column_name} = excluded.{escaped_column_name}"

        def append_foreign_key(foreign_key: FK, alias: str):
            nonlocal insert_sql, select_sql, join_sql, set_sql, foreign_key_check_sqls

            escaped_destination_column_name = self.escape_identifier(foreign_key.destination_column)
            insert_sql += (", " if insert_sql else "") + escaped_destination_column_name
            select_sql += (", " if select_sql else "") + f"{alias}.{self.escape_identifier(foreign_key.related_pk)}"            
            if key and not foreign_key.destination_column in key:
                set_sql += (", " if set_sql else "") + f"{escaped_destination_column_name} = excluded.{escaped_destination_column_name}"

            my_join_sql = f"LEFT OUTER JOIN {self.escape_identifier(foreign_key.related_schema or self.default_schema)}.{self.escape_identifier(foreign_key.related_table)} {alias} ON "
            for i, source_column in enumerate(foreign_key.source_columns):
                foreign_column = foreign_key.related_columns[i]
                my_join_sql += (" AND " if i > 0 else "") + f"{alias}.{self.escape_identifier(foreign_column)} = s.{self.escape_identifier(source_column)}"
                
            join_sql += ("\n" if join_sql else "") + my_join_sql

            # Build check SQL
            columns_sql = ""
            columns_notnull_sql = ""
            for i, source_column in enumerate(foreign_key.source_columns):
                foreign_column = foreign_key.related_columns[i]
                columns_sql += (", " if i > 0 else "") + f"s.{self.escape_identifier(source_column)}"
                columns_notnull_sql += (" OR " if i > 0 else "") + f"s.{self.escape_identifier(source_column)} IS NOT NULL"
                
            check_sql = f"SELECT {columns_sql}"
            check_sql += f"\nFROM {from_sql}"
            check_sql += f"\n{my_join_sql}"
            check_sql += f"\nWHERE ({columns_notnull_sql})"
            check_sql += f"\nAND {alias}.{self.escape_identifier(foreign_key.related_pk)} IS NULL"
            check_sql += f"\nGROUP BY {columns_sql}"

            foreign_key_check_sqls.append(check_sql)

        for src_column, dst_column in columns.items():
            if not dst_column in foreign_keys_column_names:
                append_standard_column(src_column, dst_column)

        append_consts(consts)
        append_consts(insert_consts, insert_only=True)

        if foreign_keys:
            for i, foreign_key in enumerate(foreign_keys):
                append_foreign_key(foreign_key, f"fk{i+1}")

        # Assemble SQL statement
        merge_sql = "INSERT INTO "
        if dst_schema:    
            merge_sql += f"{self.escape_identifier(dst_schema)}."
        merge_sql += f"{self.escape_identifier(dst_table)}"
        merge_sql += f" ({insert_sql})"
        merge_sql += f"\nSELECT {select_sql}"
        merge_sql += f"\nFROM {from_sql}"
        if join_sql:
            merge_sql += f"\n{join_sql}"
        if key:
            merge_sql += f"\nON CONFLICT ({key_sql})"
            merge_sql += f"\nDO UPDATE SET {set_sql}"

        if mark_missing:
            if mark_missing is True:
                mark_missing = 'missing'

            pk_columns = [header.name for header in self.get_headers((dst_schema, dst_table)) if header.primary_key]
            if not pk_columns:
                raise ValueError(f"Cannot use `mark_missing` option: no pk found in {dst_table}")
            
            outer_sql  = f"WITH upserted AS ("
            outer_sql += f"\n{merge_sql}"
            outer_sql += f"\nRETURNING {','.join(self.escape_identifier(c) for c in pk_columns)}"
            outer_sql += f"\n)"
            outer_sql += f"\nUPDATE "
            if dst_schema:    
                outer_sql += f"{self.escape_identifier(dst_schema)}."
            outer_sql += f"{self.escape_identifier(dst_table)} t"
            outer_sql += f"\nSET {self.escape_identifier(mark_missing)} = true"
            outer_sql += f"\nFROM "
            if dst_schema:    
                outer_sql += f"{self.escape_identifier(dst_schema)}."
            outer_sql += f"{self.escape_identifier(dst_table)} s"
            outer_sql += f"\nLEFT OUTER JOIN upserted u ON " + ' AND '.join(f"u.{self.escape_identifier(c)} = s.{self.escape_identifier(c)}" for c in pk_columns)
            outer_sql += f"\nWHERE (" + ' AND '.join(f"t.{self.escape_identifier(c)} = s.{self.escape_identifier(c)}" for c in pk_columns) + f")"
            outer_sql += f"\nAND (u.{self.escape_identifier(pk_columns[0])} IS NULL)"

            merge_sql = outer_sql

        # Execute SQL statements
        with self.transaction():
            # Foreign key checks
            fk_missing = []
            for check_sql in foreign_key_check_sqls:
                result = self.execute(check_sql, result=True)
                if result:
                    tab = result.tabulate()
                    self._logger.error(f"{result.rowcount} foreign key{'s' if result.rowcount > 1 else ''} not found for {result.columns}" + f"\n{tab[0:1000]}{'…' if len(tab) > 1000 else ''}")
                    fk_missing.append(result.columns[1] if len(result.columns) == 1 else result.columns)

            if fk_missing:
                raise ValueError(f"Foreign key missing for {', '.join(str(missing) for missing in fk_missing)}")
            
            # Merge statement
            self.execute(merge_sql)


    def get_load_auto_key(self,
                          model: str|tuple|type|list[Header],
                          *,
                          headers: list[str|Header]|str|Path = None, # headers or CSV file
                          convert_to_available = False,
                          default: str = 'append',
                          snake_case = False,
                          # For determining headers from `headers` if this is a file
                          encoding = 'utf-8',
                          delimiter: str = None,
                          quotechar = '"') -> tuple[str]|str:

        delimiter: str|None = None
        model = self.split_name(model) if isinstance(model, str) else model
        model_table_exists: bool = None
        model_columns_by_name: dict[str,Header] = None

        if headers:
            if isinstance(headers, (str,Path)):
                csv_file = headers
                header_names, delimiter, _ = examine_csv_file(csv_file, encoding=encoding, delimiter=delimiter, quotechar=quotechar, force_delimiter=False)
                if header_names:
                    actual_headers = [Header(name) for name in header_names]
                if not delimiter:
                    delimiter = get_default_csv_delimiter()
            else:
                actual_headers = [header if isinstance(header, Header) else Header(header) for header in headers]
        else:
            actual_headers = None

        if actual_headers and any(header.name == 'id' for header in actual_headers):
            key = ('id',)
        elif model:
            if isinstance(model, (str,tuple)): # This is actually a table                
                model_table_exists = self.table_exists(model)
            
            if model_table_exists is False:
                key = None
            else:
                model_columns_by_name = self._get_load_model_columns_by_name(model)
                key = self._select_load_auto_key(model_columns_by_name.values(), available=actual_headers, convert_to_available=convert_to_available, snake_case=snake_case)
        elif actual_headers:
            key = self._select_load_auto_key(actual_headers, snake_case=snake_case)
        else:
            key = None

        cache = self._TupleWithLoadCache(key) if key else self._StrWithLoadCache(default)
        cache._headers = actual_headers
        cache._delimiter = delimiter
        cache._model = model
        cache._model_table_exists = model_table_exists
        cache._model_columns_by_name = model_columns_by_name
        return cache


    def _get_load_model_columns_by_name(self, model: str|tuple|type|list[Header]) -> dict[str,Header]:
        """
        - `model`: can be a Django model, the name (or tuple) of a table, or a list of columns.
        """
        if isinstance(model, list):
            by_name = {}
            for column in model:
                if not isinstance(column, Header):
                    column = Header(column)
                by_name[column.name] = column
            return by_name
        else:
            return {header.name: header for header in self.get_headers(model, minimal=False)}


    def _select_load_auto_key(self, target: Iterable[Header], available: Iterable[Header|str]|None = None, *, convert_to_available = False, snake_case = False) -> tuple[str]|None:
        actual_available: list[str] = []
        if available:
            for a in available:
                name = a.name if isinstance(a, Header) else a
                if snake_case:
                    name = slugify_snake(name)
                actual_available.append(name)
        

        def convert_to_available_columns(model_key: tuple[str]):
            if not available:
                return model_key
            
            converted_key = []

            for model_column_name in model_key:
                if model_column_name in actual_available:
                    converted_key.append(model_column_name)
                elif model_column_name.endswith('_id'):
                    base = model_column_name[:-len('_id')]
                    if base in actual_available:
                        converted_key.append(base)
                    else:
                        found = False
                        for name in actual_available:
                            if name.startswith(f'{base}_'):
                                found = True
                                converted_key.append(name)
                        if not found:
                            return None
                else:
                    return None
            
            return tuple(converted_key)

        for header in target:
            if header.name == 'id':
                continue

            if header.unique:
                if header.unique is True:
                    keys = [(header.name,)]
                elif header.unique:
                    keys = header.unique

                for key in keys:
                    converted_key = convert_to_available_columns(key)
                    if converted_key:
                        return converted_key if convert_to_available else key
        
        return None
    

    def _get_load_foreign_keys(self, columns: Iterable[str], target_model: type):
        from django.db.models import Field, ForeignKey

        results: list[FK] = []

        field: Field
        for field in target_model._meta.fields:
            if isinstance(field, ForeignKey):
                prefix = f"{field.name}_"
                source_columns = [column for column in columns if column.startswith(prefix)]
                if source_columns:
                    results.append(FK(source_columns, field.related_model,
                                              related_pk=field.related_model._meta.pk.attname,
                                              related_pk_type=_get_django_field_python_type(field.related_model._meta.pk),
                                              destination_column=field.attname))

        return results


    class _LoadCacheMixin:
        def __init__(self, *args, **kwargs):
            self._headers: list[Header]|None = None
            self._delimiter: str|None = None
            self._model: tuple|type|list[Header]|None = None
            self._model_table_exists: bool = None
            self._model_columns_by_name: dict[str,Header] = None

    class _TupleWithLoadCache(Tuple[str], _LoadCacheMixin):
        pass

    class _StrWithLoadCache(str, _LoadCacheMixin):
        pass

    #endregion


    #region Dump

    def dumper(self,               
               # DB-specific options
               table: str|tuple = None, *,
               add_autoincrement_pk: bool|str = False,
               batch: int|None = None,
               # Common TabularDumper options
               headers: Iterable[Header|Any]|None = None,
               append = False,
               archivate: bool|str|Path|None = None,
               title: str|bool|None = None,
               dst_name: str|bool = True,
               dir: str|Path|Literal[False]|None = None,
               delay: bool = False,
               defaults: dict[str,Any] = None,
               optional: str|Sequence[str]|Literal['*',True]|None = None,
               add_columns: bool|Literal['warn'] = False,
               no_tz: tzinfo|str|bool|None = None,
               # Destination mask values
               **kwargs) -> DbDumper[T_Connection, T_Cursor]:
        
        if no_tz is None:
            no_tz = self.tz

        extended_kwargs = {
                'headers': headers,
                'append': append,
                'archivate': archivate,
                'title': title,
                'dst_name': dst_name,
                'dir': dir,
                'delay': delay,
                'defaults': defaults,
                'optional': optional,
                'add_columns': add_columns,
                'no_tz': no_tz,
                **kwargs
            }

        return DbDumper(self,
                        table=table,
                        add_autoincrement_pk=add_autoincrement_pk,
                        batch_size=batch,
                        **extended_kwargs)
    
    #endregion


class CursorContext(Generic[T_Connection, T_Cursor]):
    def __init__(self, db: Db[T_Connection, T_Cursor], sql: str = None, params: Sequence[Any]|Mapping[str,Any]|None = None, *, warn_results: int|bool = False, messages_source: str|None = None):
        self.db = db
        self._warn_results = warn_results
        self._messages_source = messages_source
        self._messages_handler = None
        
        cursor = db.connection.cursor()
        self.cursor = cursor if self.db.scheme == 'sqlite' else cursor.__enter__() # sqlite cursors are not context managers

        self._messages_handler = self.db._register_cursor_messages_handler(cursor, self._messages_source)
        if self._messages_handler:
            self._messages_handler.__enter__()

        if sql:
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)

    def __enter__(self) -> T_Cursor:
        return self.cursor
    
    def __exit__(self, exc_type = None, exc_value = None, exc_traceback = None):
        if self._messages_handler:
            self._messages_handler.__exit__(exc_type, exc_value, exc_traceback)

        no_cursor_messages = getattr(self.db._log_cursor_messages, '_do_nothing', None)
        if no_cursor_messages and not self._warn_results:
            self.cursor.close()
            return

        while True: # traverse all result sets
            self.db._log_cursor_messages(self.cursor, self._messages_source)

            if self._warn_results:
                if self.cursor.description:
                    rows = []
                    there_are_more = False
                    for i, row in enumerate(iter(self.cursor)):
                        if self._warn_results is True or i < self._warn_results:
                            rows.append(row)
                        else:
                            there_are_more = True
                            break

                    if rows:
                        columns = [c[0] for c in self.cursor.description]
                        warn_text = "Unexpected result set:\n" 
                        
                        if tabulate:
                            warn_text += tabulate(rows, columns)
                        else:
                            warn_text += '\t'.join(columns)
                            for row in rows:
                                warn_text += '\n' + '\t'.join(str(val) for val in row)
                        
                        if there_are_more:
                            warn_text += "\n…"
                        logger = logging.getLogger(f"{self.db._logger.name}:{self._messages_source}") if self._messages_source else self.db._logger
                        logger.warning(warn_text)

            if self.db.scheme == 'sqlite' or not self.cursor.nextset():
                break

        self.cursor.close()


class ResultContext(CursorContext[T_Connection, T_Cursor]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._row_iterator = None
        self._row_iteration_stopped = False
        self._iterated_rows: list[TupleRow] = []

    def __enter__(self):
        return self

    @property
    def headers(self):
        try:
            return self._headers
        except:
            pass
        self._headers = self.db._get_headers_from_cursor_description(self.cursor.description)
        return self._headers

    @property
    def columns(self) -> tuple[str]:
        try:
            return self._columns
        except:
            pass
        self._columns = tuple(c[0] for c in self.cursor.description)
        return self._columns

    def __iter__(self):       
        return ResultIterator(self)
        
    def __bool__(self):
        try:
            next(iter(self))
            return True
        except StopIteration:
            return False

    def _next_row_values(self):
        if self._row_iterator is None:
            self._row_iterator = iter(self.cursor)
        
        if self._row_iteration_stopped:
            raise StopIteration()
    
        try:
            values = next(self._row_iterator)
        except StopIteration:
            self._input_rows_iterator_stopped = True
            raise

        return values

    def _format_row(self, values) -> TupleRow:
        transformed = None

        if self.db.tz:
            for i, value in enumerate(values):
                if isinstance(value, (datetime,time)):
                    if not value.tzinfo:
                        if transformed is None:
                            transformed = [value for value in values] if isinstance(values, tuple) else values
                        transformed[i] = value.replace(tzinfo=self.db.tz)

        row = TupleRow(transformed if transformed is not None else values)
        row.provider = self
        return row
    
    @property
    def rowcount(self) -> int:
        """ Return row count or -1 if none. """
        return self.cursor.rowcount
    
    @property
    def lastrowid(self):
        return self.db._get_cursor_lastrowid(self.cursor)
    
    def iter_rows(self) -> Generator[TupleRow,Any,None]:
        for row in iter(self):
            yield row
    
    def get_rows(self):
        return [row for row in self.iter_rows()]

    def get_row(self):
        iterator = iter(self)
        try:
            return next(iterator)
        except StopIteration:
            raise NotFoundError()

    def single_row(self):
        iterator = iter(self)
        try:
            result = next(iterator)
        except StopIteration:
            raise NotFoundError()
        
        try:
            next(iterator)
        except StopIteration:
            return result
        
        raise SeveralFoundError()

    def first_row(self):
        try:
            return self.get_row()
        except NotFoundError:
            return None
    
    def iter_dicts(self) -> Generator[dict[str,Any],Any,None]:
        for row in iter(self):
            yield {column: row[i] for i, column in enumerate(self.columns)}
    
    def get_dicts(self):
        return [data for data in self.iter_dicts()]

    def get_dict(self):
        iterator = self.iter_dicts()
        try:
            return next(iterator)
        except StopIteration:
            raise NotFoundError()

    def single_dict(self):
        iterator = self.iter_dicts()
        try:
            result = next(iterator)
        except StopIteration:
            raise NotFoundError()
        
        try:
            next(iterator)
        except StopIteration:
            return result
        
        raise SeveralFoundError()

    def first_dict(self):
        try:
            return self.first_dict()
        except NotFoundError:
            return None

    def get_vals(self):
        """A convenience function for returning the first column of each row from the query."""
        return [row[0] for row in iter(self)]

    def get_val(self):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row."""
        return self.get_row()[0]

    def single_val(self):
        """A convenience function for returning the first column of the first row from the query. Raise NotFoundError if there is no row or SeveralFound if there are more than one row."""
        return self.single_row()[0]

    def first_val(self):
        """A convenience function for returning the first column of the first row from the query. Raise None if there is no row."""
        row = self.get_row()
        if row is None:
            return None
        return row[0]
    
    def tabulate(self):
        if tabulate:
            return tabulate(self.get_rows(), self.columns)
        else:
            text = '\t'.join(self.columns)
            for row in self.get_rows():
                text += '\n' + '\t'.join(str(val) for val in row)
            return text
    
    def print_tabulate(self, *, file = sys.stdout):
        file.write(self.tabulate())

    def to_dumper(self, dumper: TabularDumper|IOBase|str|Path, close=True, **kwargs):
        """
        Send results to the given tabular dumper.
        
        If dumper is `tab`, `csv`, a stream or a str/path, create the appropriate Tab/CSV/Excel dumper.
        
        Return a tuple containing the list of columns and the number of exported rows.
        """
        if isinstance(dumper, TabularDumper):
            if dumper.headers is not None:
                if [header.name for header in dumper.headers] != self.columns:
                    raise ValueError("Invalid headers in given dumper")
            else:
                dumper.headers = self.headers
        else:
            dumper = tabular_dumper(dumper, headers=self.headers, **kwargs)

        try:
            for row in iter(self):
                dumper.dump(row)        
            return self.columns, dumper.count
        finally:
            if close:
                dumper.close()


class ResultIterator(Generic[T_Connection, T_Cursor]):
    def __init__(self, context: ResultContext[T_Connection, T_Cursor]):
        self.context = context
        self.next_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.next_index < len(self.context._iterated_rows):
            row = self.context._iterated_rows[self.next_index]
        else:
            values = self.context._next_row_values()
            row = self.context._format_row(values)
            self.context._iterated_rows.append(row)
        
        self.next_index += 1
        return row


class FK:
    def __init__(self, source_columns: str|Iterable[str], related_table: str|tuple[str|None,str]|type, *, related_columns: str|Iterable[str] = None, related_pk: str = 'id', related_pk_type: type|None = None, destination_column: str = None):
        if isinstance(source_columns, str):
            self.source_columns = (source_columns,)
        else:
            self.source_columns = tuple(column for column in source_columns)

        if isinstance(related_table, tuple):
            self.related_schema, self.related_table = related_table
        elif isinstance(related_table, str):
            self.related_schema = None
            self.related_table = related_table
        elif isinstance(related_table, type):
            self.related_schema = None
            self.related_table = related_table._meta.db_table
        else:
            raise TypeError(f"related_table: {related_table}")
        
        source_prefix = self._find_source_prefix()

        if related_columns:
            if isinstance(related_columns, str):
                self.related_columns = (related_columns,)
            else:
                self.related_columns = tuple(column for column in related_columns)
            if len(self.related_columns) != len(self.source_columns):
                raise ValueError(f"{len(related_columns)} foreign_columns for {len(source_columns)} columns")
        else:
            self.related_columns = tuple(column[len(source_prefix):] for column in self.source_columns)            

        self.related_pk = related_pk
        self.related_pk_type = related_pk_type

        if destination_column:
            self.destination_column = destination_column
        elif source_prefix:
            self.destination_column = f'{source_prefix}{self.related_pk}'
        else:
            self.destination_column = f'{self.related_table}{self.related_pk}'


    def __repr__(self):
        return f"FK({', '.join(self.source_columns)}) -> {self.destination_column}: {f'{self.related_schema}.' if self.related_schema else ''}{self.related_table}({', '.join(self.related_columns)}) -> {self.related_pk}" + (f" ({self.related_pk_type.__name__})" if self.related_pk_type else "")


    def _find_source_prefix(self):        
        size = len(self.source_columns)

        # if size is 0, return empty string 
        if (size == 0):
            raise ValueError("Source columns cannot be empty")

        if (size == 1):
            foreign_table_prefix = f"{self.related_table}_"
            if self.source_columns[0].startswith(foreign_table_prefix): # e.g. source_column 'cluster_name', foreign table 'cluster'
                return foreign_table_prefix
            
            pos = self.related_table.rfind('_')
            if pos > 0:
                part_prefix = f"{self.related_table[pos+1:]}_"
                if self.source_columns[0].startswith(part_prefix): # e.g. source_column 'cluster_name', foreign table 'vmware_cluster':
                    return part_prefix

            return ''

        # sort the array of strings 
        values = sorted(self.source_columns)
        
        # find the minimum length from first and last string 
        end = min(len(values[0]), len(values[size - 1]))

        # find the common prefix between  the first and last string 
        i = 0
        while (i < end and values[0][i] == values[size - 1][i]):
            i += 1

        prefix = values[0][0: i]
        return prefix


class DbDumper(TabularDumper[Db[T_Connection, T_Cursor]]):
    """ 
    Line-per-line INSERT commands (to be used when `InsertSqlDumper` is not available).
    """
    def __init__(self, origin: Db[T_Connection, T_Cursor]|T_Connection|ParseResult|dict,
                 table: str|tuple|None = None,
                 *,
                 add_autoincrement_pk: bool|str = False,
                 batch_size: int|None = None,
                 **kwargs):
        
        if isinstance(origin, Db):
            dst = origin
            self._close_dst = False
        else:
            dst = get_db(origin, autocommit=False)
            self._close_dst = True
        
        if table:
            self._schema, self._table = dst.split_name(table)
        elif dst.table:
            self._schema, self._table = dst.schema, dst.table
        else:
            raise ValueError("Table name not provided")

        dst_name = kwargs.pop('dst_name', None)
        if not dst_name:
            dst_name = f"{self._schema + '.' if self._schema else ''}{self._table}"

        super().__init__(dst, dst_name=dst_name, **kwargs)

        self._add_autoincrement_pk = 'id' if add_autoincrement_pk is True else add_autoincrement_pk
        self._insert_sql_headers: list[Header] = []
        self._insert_sql_single: str = None
        self._insert_sql_batch: str = None
        if self.dst.scheme == 'sqlite':
            self._max_params = 999
        elif self.dst.scheme == 'sqlserver':
            self._max_params = 2100
        else:
            self._max_params = 65535 # postgresql limit
        self.batch_size = batch_size

        self._cursor = None
        self._batch_rows = []
        self._executed_batch_count = 0

        self._insert_schema = self._schema
        self._insert_table = self._table

    @property
    def cursor(self):
        """
        Reused cursor (only for inserting data).
        """
        if self._cursor is None:
            self._cursor = self.dst.connection.cursor()
        return self._cursor

    def close(self, *final_queries):
        """
        Export remaining rows, execute optional final SQL queries, and then close the dumper.
        """
        super().close()

        self.flush(*final_queries)

        if self._cursor is not None:
            self._cursor.close()
            self._cursor = None       

        if not self.dst.get_autocommit():
            self.dst.connection.commit()

        if self._close_dst:
            self.dst.close()

    def _build_insert_sqls(self, additional_headers: list[Header]):
        self._insert_sql_headers += additional_headers

        into_sql = f""
        if self._insert_schema:
            into_sql += f"{self.dst.escape_identifier(self._insert_schema)}."
        into_sql += self.dst.escape_identifier(self._insert_table)

        into_sql += "("
        values_sql = "("
        need_comma = False
        for header in self._insert_sql_headers:
            if need_comma:
                into_sql += ","
                values_sql += ","
            else:
                need_comma = True
            into_sql += f"{self.dst.escape_identifier(header.name)}"
            values_sql += self.dst.sql_placeholder
        into_sql += ")"
        values_sql += ")"

        max_batch = int(self._max_params / len(self._insert_sql_headers))
        if self.batch_size is None or max_batch < self.batch_size:
            self.batch_size = max_batch

        self._insert_sql_single = f"INSERT INTO {into_sql} VALUES {values_sql}"
        self._insert_sql_batch = f"INSERT INTO {into_sql} VALUES "
        for i in range(self.batch_size):
            self._insert_sql_batch += (',' if i > 0 else '') + values_sql

    def open(self) -> list[Header]|None:
        # Called at first exported row, before headers are analyzed.
        # Return list of existing headers if table exists, None if not.
        if self.dst.table_exists((self._schema, self._table)):
            if not self.append:
                self.dst.clear_table((self._schema, self._table))
            
            headers = [header for header in self.dst.get_headers((self._schema, self._table)) if not header.identity]
            self._build_insert_sqls(headers)
            return headers
        else:
            return None
    
    def export_headers(self, headers: list[Header]):
        # Called at first exported row, if there are no pre-existing headers (= table does not exist) => create table
        columns = [header for header in headers]
        
        if self._add_autoincrement_pk and not any(header.name == self._add_autoincrement_pk for header in headers):
            columns.insert(0, Header(name=self._add_autoincrement_pk, type=int, primary_key=True, identity=True))

        self.dst.create_table((self._schema, self._table), columns)

        self._build_insert_sqls(headers)

    def new_headers(self, headers: list[Header]) -> bool|None:
        self.dst.append_column((self._schema, self._table), headers, ignore_not_null=True)
        self._build_insert_sqls(headers)
        return True

    def _ensure_opened(self):
        if not self.headers:
            raise ValueError(f"Cannot dump to db without headers")
        super()._ensure_opened()

    def _convert_value(self, value: Any):
        value = super()._convert_value(value)
        value = self.dst.to_supported_value(value)
        return value

    def export(self, row: list):
        self._batch_rows.append(row)
        if len(self._batch_rows) >= self.batch_size:
            self._export_batch()

    def _export_batch(self):
        kwargs = {}
        if self.dst.scheme == 'postgresql':
            kwargs['prepare'] = True
            
        inlined_row = []
        while len(self._batch_rows) / self.batch_size >= 1:
            for row in self._batch_rows[:self.batch_size]:
                inlined_row += row
                
            if self._logger.isEnabledFor(logging.DEBUG):
                t0 = time_ns()
                if self._executed_batch_count == 0:
                    self._d_total = 0
            
            self.cursor.execute(self._insert_sql_batch, inlined_row, **kwargs)
            self._executed_batch_count += 1

            if self._logger.isEnabledFor(logging.DEBUG):
                t = time_ns()
                d = t - t0
                self._d_total += d
                self._logger.debug(f"Batch {self._executed_batch_count}: {self.batch_size:,} rows inserted in {d/1e6:,.1f} ms (avg: {self._d_total/1e3/(self._executed_batch_count * self.batch_size):,.1f} ms/krow, inst: {d/1e3/self.batch_size:,.1f} ms/krow)")
            
            self._batch_rows = self._batch_rows[self.batch_size:]

    def flush(self, *final_queries):
        """
        Export remaining rows, and then execute optional final SQL queries.
        """
        super().flush()

        kwargs = {}
        if self.dst.scheme == 'postgresql':
            kwargs['prepare'] = True
        
        self._ensure_opened()
        self._export_batch()

        if self._batch_rows:
            if self._logger.isEnabledFor(logging.DEBUG):
                t0 = time_ns()

            for row in self._batch_rows:
                while len(row) < len(self._insert_sql_headers):
                    row.append(None)
                self.cursor.execute(self._insert_sql_single, row, **kwargs)
                            
            if self._logger.isEnabledFor(logging.DEBUG):
                d = time_ns() - t0
                self._logger.debug(f"Remaining: {len(self._batch_rows):,} rows inserted one by one in {d/1e6:,.1f} ms ({d/1e3/(len(self._batch_rows)):,.1f} ms/krow)")

            self._batch_rows.clear()

        for final_query in final_queries:
            self.dst.execute(final_query)


class NotFoundError(_BaseNotFoundError): # Status code 404
    def __init__(self, message: str = None):
        super().__init__(message if message else "Not found")


class SeveralFoundError(Exception): # Status code 409 ("Conflict")
    def __init__(self, message: str = None):
        super().__init__(message if message else "Several found")


def _get_django_field_python_type(field) -> type|None:
    from django.db import models
    from django.contrib.postgresql.field import ArrayField

    if isinstance(field, models.BooleanField):
        return bool
    elif isinstance(field, models.IntegerField):
        return int
    elif isinstance(field, models.FloatField):
        return float
    elif isinstance(field, models.DecimalField):
        return Decimal
    elif isinstance(field, models.DateTimeField):
        return datetime
    elif isinstance(field, models.DateField):
        return date
    elif isinstance(field, models.CharField):
        return str
    elif isinstance(field, models.TextField):
        return str
    elif isinstance(field, ArrayField):
        return list
    else:
        return None # we don't want to make false assumptions (e.g. we would probably want 'str' in the context of a load table and 'int' for a foreign key field)


def _get_django_model_unique_keys(model) -> list[tuple[str]]:
    """
    Report django model unique keys, based on attnames (column names).
    """
    from django.db import models

    field_orders: dict[str,int] = {}
    attnames_by_name: dict[str,str] = {}

    class Unique:
        def __init__(self, fields: list[str]|tuple[str]|str):
            if isinstance(fields, str):
                self.fields = [fields]
            elif isinstance(fields, (list,tuple)):
                self.fields: list[str] = []
                for i, name in enumerate(fields):
                    if isinstance(name, str):
                        if not name in field_orders:
                            name = attnames_by_name[name]
                        self.fields.append(name)
                    else:
                        raise TypeError(f"fields[{i}]: {type(name).__name__}")  
            else:
                raise TypeError(f"fields: {type(fields).__name__}")            
            
            self.min_field_order = min(field_orders[field] for field in self.fields)

        def append(self, field: str):
            self.fields.append(field)
            if field_orders[field] < self.min_field_order:
                self.min_field_order = field_orders[field]

    primary_key: Unique = None
    other_keys: list[Unique] = []

    for i, field in enumerate(model._meta.fields):
        field_orders[field.attname] = i
        attnames_by_name[field.name] = field.attname
        
        if field.primary_key:
            if not primary_key:
                primary_key = Unique(field.attname)
            else:
                primary_key.append(field.attname)
        elif field.unique:
            other_keys.append(Unique(field.attname))

    for names in model._meta.unique_together:
        other_keys.append(Unique(names))

    for constraint in model._meta.constraints:
        if isinstance(constraint, models.UniqueConstraint):
            other_keys.append(Unique(constraint.fields))

    results = []
    
    if primary_key:
        results.append(tuple(primary_key.fields))

    for key in sorted(other_keys, key=lambda key: key.min_field_order):
        results.append(tuple(key.fields))

    return results


def _get_connection_from_wrapper(db):    
    if type(db).__module__.startswith(('django.db.backends.', 'django.utils.connection')):
        return db.connection
    elif type(db).__module__.startswith(('psycopg_pool.pool',)):
        return db.connection()
    elif type(db).__module__.startswith(('psycopg2.pool',)):
        return db.getconn()
    else:
        return db


def get_db(origin, *, autocommit=True) -> Db:
    """
    Create a new Db instance (if origin is not already one).
    - `autocommit`: commit transactions automatically (applies only for connections created by the Db instance).
    """
    from zut.db.mariadb import MariaDb
    from zut.db.postgresql import PostgreSqlDb
    from zut.db.postgresqlold import PostgreSqlOldDb
    from zut.db.sqlite import SqliteDb
    from zut.db.sqlserver import SqlServerDb

    if isinstance(origin, str):
        db_cls = get_db_class(origin)
        if db_cls is None:
            raise ValueError(f"Invalid db url: {origin}")
        return db_cls(origin, autocommit=autocommit)
    
    elif isinstance(origin, dict) and 'ENGINE' in origin: # Django
        engine = origin['ENGINE']
        if engine in {"django.db.backends.postgresql", "django.contrib.gis.db.backends.postgis"}:
            if not PostgreSqlDb.missing_dependency:
                return PostgreSqlDb(origin, autocommit=autocommit)
            elif not PostgreSqlOldDb.missing_dependency:
                return PostgreSqlOldDb(origin, autocommit=autocommit)
            else:
                raise ValueError(f"PostgreSql and PostgreSqlOld not available (psycopg missing)")
        elif engine in {"django.db.backends.mysql", "django.contrib.gis.db.backends.mysql"}:
            return MariaDb(origin, autocommit=autocommit)
        elif engine in {"django.db.backends.sqlite3", "django.db.backends.spatialite"}:
            return SqliteDb(origin, autocommit=autocommit)
        elif engine in {"mssql"}:
            return SqlServerDb(origin, autocommit=autocommit)
        else:
            raise ValueError(f"Invalid db: unsupported django db engine: {engine}")
        
    elif isinstance(origin, Db):
        return origin
    
    else:
        db_cls = get_db_class(origin)
        if db_cls is None:
            raise ValueError(f"Invalid db: unsupported origin type: {type(origin)}")
        return db_cls(origin)
    

def get_db_class(origin: Connection|ParseResult|str) -> type[Db]|None:
    from zut.db.mariadb import MariaDb
    from zut.db.postgresql import PostgreSqlDb
    from zut.db.postgresqlold import PostgreSqlOldDb
    from zut.db.sqlite import SqliteDb
    from zut.db.sqlserver import SqlServerDb

    if isinstance(origin, str):
        origin = urlparse(origin)

    if isinstance(origin, ParseResult):
        if origin.scheme in {'postgresql', 'postgres', 'pg'}:
            if not PostgreSqlDb.missing_dependency:
                db_cls = PostgreSqlDb
            elif not PostgreSqlOldDb.missing_dependency:
                db_cls = PostgreSqlOldDb
            else:
                raise ValueError(f"PostgreSql and PostgreSqlOld not available (psycopg missing)")
        elif origin.scheme in {'mariadb', 'mysql'}:
            db_cls = MariaDb
        elif origin.scheme in {'sqlite', 'sqlite3'}:
            db_cls = SqliteDb
        elif origin.scheme in {'sqlserver', 'sqlservers', 'mssql', 'mssqls'}:
            db_cls = SqlServerDb
        else:
            return None
    else: # origin is assumed to be a connection object
        origin = _get_connection_from_wrapper(origin)

        type_fullname: str = type(origin).__module__ + '.' + type(origin).__qualname__
        if type_fullname == 'psycopg2.extension.connection':
            db_cls = PostgreSqlOldDb
        elif type_fullname == 'psycopg.Connection':
            db_cls = PostgreSqlDb
        elif type_fullname == 'MySQLdb.connections.Connection':
            db_cls = MariaDb
        elif type_fullname == 'sqlite3.Connection':
            db_cls = SqliteDb
        elif type_fullname == 'pyodbc.Connection':
            db_cls = SqlServerDb
        else:
            return None
    
    if db_cls.missing_dependency:
        raise ValueError(f"Cannot use db {db_cls} (missing {db_cls.missing_dependency} dependency)")
    
    return db_cls
