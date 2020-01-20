# Ω*
#               ■          ■■■■■  
#               ■         ■■   ■■ 
#               ■        ■■     ■ 
#               ■        ■■       
#     ■■■■■     ■        ■■■      
#    ■■   ■■    ■         ■■■     
#   ■■     ■■   ■          ■■■■   
#   ■■     ■■   ■            ■■■■ 
#   ■■■■■■■■■   ■              ■■■
#   ■■          ■               ■■
#   ■■          ■               ■■
#   ■■     ■    ■        ■■     ■■
#    ■■   ■■    ■   ■■■  ■■■   ■■ 
#     ■■■■■     ■   ■■■    ■■■■■


"""
Moca Config Module
モカシステム設定モジュール
茉客系统设定模块

[MocaConfig]

Copyright (c) 2020.1.17 [el.ideal-ideas]

This software is released under the MIT License. see LICENSE.txt.

https://www.el-ideal-ideas.com
"""


# -- Imports --------------------------------------------------------------------------

from typing import Any, Union, List, Tuple, Optional
from moca_core import EL_S, N, MocaFileError, MocaUsageError
from pathlib import Path
from json import load, dump, JSONDecodeError
from threading import Thread
from time import sleep
from datetime import datetime
from random import choice, randint
from string import ascii_letters, digits
from uuid import uuid1, uuid4
from multiprocessing import current_process, cpu_count
from sanic import Sanic
from sanic.response import redirect, text, json
from sanic_openapi import doc, swagger_blueprint
from sanic.exceptions import Forbidden, InvalidUsage
from ssl import SSLContext, create_default_context, Purpose
from docopt import docopt
from os import _exit

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------


VERSION = '1.0.12'

__USAGE = """
    Usage:
        moca_config
        moca_config help
        moca_config PATH [-p|--port <PORT>] [-n|--name <NAME>] [-t|--token <TOKEN>] [-w|--workers <WORKERS>] 
                         [-c|--certfile <CERT_PATH>] [-k|--keyfile <KEY_PATH>] [-i|--interval <RELOAD_INTERVAL>] 
                         [mochi]
        
    MocaConfig Module
    
    Arguments:
        PATH:            the path of config file.
        PORT:            the port number of config server.
        NAME:            the name of config instance.
        TOKEN:           the access token of config server.
        CERT_PATH:       the certificate file path(for ssl connection).
        KEY_PATH:        the private key file path(for ssl connection).
        RELOAD_INTERVAL: the reload interval of config server.
        WORKERS:         the number of workers.
        
    Options:
        help:                              show the help.
        -p | --port <PORT>:                config server port number.
        -n | --name <NAME>:                config name.
        -t | --token <TOKEN>:              the access token of config server.
        -c | --certfile <CERT_PATH>:       the path of the certificate file.
        -k | --keyfile <KEY_PATH>:         the path of the private key file.
        -i | --interval <RELOAD_INTERVAL>: the reload interval of config server.
        -w | --workers <WORKERS>:          the number of workers.
        mochi:                             もっちもっちにゃんにゃん
"""

__HELP = """
EN: This command can run a standalone config server.
JA: このコマンドは独立動作する設定サーバーを立ち上げることができます。
ZH: 本命令可以启动一个能独立运行的设定服务器。
"""

server_headers = {
    'X-Served-By': 'Sanic: Moca-System(Python): Y',
    'Access-Control-Allow-Origin': '*',
    'Detail': 'This system is create by el.ideal-ideas, For more info,'
              ' please check www.el-ideal-ideas.com, or Twitter : @support_el_s',
}

# -------------------------------------------------------------------------- Variables --

# -- Main Class --------------------------------------------------------------------------


class MocaConfig(object):
    """
    This is the config module developed by el.ideal-ideas for Moca System.
    This config module is json based.
    All config data in the json file, will be loaded into memory, and can be used from MocaConfig class.
    MocaConfig class will reload the json file in 5(default value) seconds.
    If the json file was changed. the new config value will overwrite the old config value that in memory.
    -------
    これはモカシステムのためにel.ideal-ideasによって開発された設定モジュールである。
    この設定モジュールはJSON形式を採用しています。
    JSONファイル内のすべての設定情報はメモリ内にロードされ、そしてMocaConfigクラスを経由して取得できます。
    MocaConfigクラスはデフォルト設定では5秒ごとJSONファイルをリロードします。
    JSONファイルに変更があった場合、その変更はメモリ内の設定情報にも反映されます。
    -------
    这是el.ideal-ideas为茉客系统开发的设定模块。
    这个设定模块采用了JSON格式。
    JSON文件内的所有设定信息会被保存到内存里，您可以通过MocaConfig类来获取各种设定信息。
    MocaConfig类会每5（初期值）秒重新读取一次JSON文件。
    如果JSON文件被改写，内存内的设定信息也会和JSON文件同步。

    Attributes
    ----------
    path: Path
        the config file path

    reload_interval: float
        the reload interval

    __config_cache: dict
        config cache

    __status: int
        the status of config module, 0 is correct
    """

    __INIT_MSG = {
        "__MocaConfig": "Welcome to MocaConfig, the config module is now available.",
        "__MocaConfig_version": VERSION
    }

    __instance_list: dict = {}

    # status code
    CORRECT = 0
    DECODE_ERROR = 1
    FILE_NOT_FOUND = 2
    PERMISSION_ERROR = 3
    OS_ERROR = 4
    UNKNOWN_ERROR = 5

    # el command
    NOW: str = '[el]#moca_now#'  # current time
    NOW_DATE: str = '[el]#moca_now_date#'  # current date
    RANDOM_STRING: str = '[el]#moca_random_string<length>#'  # random string
    RANDOM_INTEGER: str = '[el]#moca_random_integer#'  # random integer
    RANDOM_INTEGER_LIST: str = '[el]#moca_random_integer_list<length>#'  # random integer list
    RANDOM_INTEGERS: str = '[el]#moca_random_integers<length>#'  # random integer list
    UUID1: str = '[el]#moca_uuid1#'  # uuid1 string
    UUID1_HEX: str = '[el]#moca_uuid1_hex#'  # uuid1 hex
    UUID4: str = '[el]#moca_uuid4#'  # uuid4 string
    UUID4_HEX: str = '[el]#moca_uuid4_hex#'  # uuid4 hex
    PROCESS_ID: str = '[el]#moca_process_id#'  # process id
    PROCESS_NAME: str = '[el]#moca_process_name#'  # process name
    CPU_COUNT: str = '[el]#moca_cpu_count#'  # cpu count
    GET_ALL_CONFIG: str = '[el]#moca_get_all_config#'  # get all config

    def __init__(self,
                 name: str,
                 filepath: Union[Path, str],
                 filename: str = '',
                 reload_interval: float = 5.0):
        """
        The initializer of MocaConfig class.
        :param name: the name of this instance
        :param filepath: the path of json config file.
        :param filename: the name of json config file.
        :param reload_interval: the interval to reload config file. if the value is -1, never reload config file

        Raise
        -----
            TypeError: if the arguments type is incorrect.
            MocaFileError: if can't find, open or create config file.
        """
        # set config file path
        path: Path
        if isinstance(filepath, Path):  # check filepath parameter
            path = filepath
        elif isinstance(filepath, str):
            path = Path(filepath)
        else:
            raise TypeError('Argument type error, '
                            'Expected filepath: Union[Path, str], '
                            f'But received filepath: {type(filepath)}')
        if isinstance(filename, str):  # check filename parameter
            if filename != '':  # if filename is not empty string, join it.
                path = path.joinpath(filename)
        else:
            raise TypeError('Argument type error, '
                            'Expected filename: str, '
                            f'But received filename: {type(filename)}')
        self.path: Path = path
        # check config file
        if not path.is_file():  # if file is not exist, create it
            if not path.parent.is_dir():
                path.parent.mkdir(parents=True)
            try:
                with open(str(path), mode='w', encoding='utf-8') as config_file:
                    dump(MocaConfig.__INIT_MSG,
                         config_file,
                         ensure_ascii=False,
                         indent=4,
                         sort_keys=False,
                         separators=(',', ': '))
            except (FileNotFoundError, PermissionError, OSError, Exception) as error:
                raise MocaFileError(f"Can't create config file.{N}"
                                    f"Details: {N}"
                                    f"{error}")
        else:
            try:
                with open(str(path), mode='r', encoding='utf-8') as _:
                    pass
            except (FileNotFoundError, PermissionError, OSError, Exception) as error:
                raise MocaFileError(f"Can't open config file.{N}"
                                    f"Details: {N}"
                                    f"{error}")
        # set reload interval
        if isinstance(reload_interval, float) or isinstance(reload_interval, int):
            self.reload_interval: float = float(reload_interval)
        else:
            TypeError('Argument type error, '
                      'Expected reload_interval: float, '
                      f'But received reload_interval: {type(reload_interval)}')
        # initialize cache variable
        self.__config_cache: dict = {}
        # set current status
        self.__status: int = MocaConfig.CORRECT
        # load config file
        self.reload_config()
        # start reload-config-loop on other thread
        loop_thread = Thread(target=self.__reload_config_loop)
        loop_thread.start()
        # add self to instance list
        MocaConfig.__instance_list[name] = self

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def status(self):
        """Return the self.status"""
        return self.__status

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def reload_config(self) -> None:
        """Reload json config file."""
        try:
            with open(str(self.path), mode='r', encoding='utf-8') as config_file:
                self.__config_cache = load(config_file)
            self.__status = MocaConfig.CORRECT
        except JSONDecodeError:
            self.__status = MocaConfig.DECODE_ERROR
        except FileNotFoundError:
            self.__status = MocaConfig.FILE_NOT_FOUND
        except PermissionError:
            self.__status = MocaConfig.PERMISSION_ERROR
        except OSError:
            self.__status = MocaConfig.OS_ERROR
        except Exception:
            self.__status = MocaConfig.UNKNOWN_ERROR

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def random_string(length: int) -> str:
        """Return a random string."""
        characters = ascii_letters + digits
        return ''.join([choice(characters) for _ in range(length)])

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def random_integers(length: int) -> str:
        """Return random integers as string"""
        return ''.join([str(randint(0, 9)) for _ in range(length)])

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def random_integer_list(length: int) -> List[int]:
        """Return random integer list"""
        return [randint(0, 9) for _ in range(length)]

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def __reload_config_loop(self) -> None:
        """the reload-config-loop."""
        while True:
            if self.reload_interval == -1:
                sleep(5)
            elif self.reload_interval <= 0:
                sleep(5)
                self.reload_config()
            else:
                sleep(self.reload_interval)
                self.reload_config()

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get_config_size(self) -> int:
        """Return config cache size"""
        return len(self.__config_cache)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get_all_config(self) -> dict:
        """Return all config"""
        return self.__config_cache

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get_all_config_key(self) -> tuple:
        """Return all key in self.__config_cache."""
        return tuple(self.__config_cache.keys())

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @classmethod
    def el_command_parser(cls,
                          command: str) -> Tuple[bool, Any]:
        """
        Parse the command.
        :param command: target string.
        :return: (status, response)
                 status: detected el-command, or not.
                 response: el-command response, if can't detect el-command, the response will be None.
        """
        if command == cls.NOW:
            return True, datetime.now()
        elif command == cls.NOW_DATE:
            return True, datetime.now().date()
        elif command.startswith('[el]#moca_random_string<') and command.endswith('>#'):
            try:
                return True, cls.random_string(int(command[24:-2]))
            except (TypeError, ValueError, Exception):
                return False, None
        elif command == cls.RANDOM_INTEGER:
            return True, randint(0, 9)
        elif command.startswith('[el]#moca_random_integer_list<') and command.endswith('>#'):
            try:
                return True, cls.random_integer_list(int(command[30:-2]))
            except (TypeError, ValueError, Exception):
                return False, None
        elif command.startswith('[el]#moca_random_integers<') and command.endswith('>#'):
            try:
                return True, cls.random_integers(int(command[26:-2]))
            except (TypeError, ValueError, Exception):
                return False, None
        elif command == cls.UUID1:
            return True, str(uuid1())
        elif command == cls.UUID1_HEX:
            return True, uuid1().hex
        elif command == cls.UUID4:
            return True, str(uuid4())
        elif command == cls.UUID4_HEX:
            return True, uuid4().hex
        elif command == cls.PROCESS_ID:
            return True, current_process().pid
        elif command == cls.PROCESS_NAME:
            return True, current_process().name
        elif command == cls.CPU_COUNT:
            return True, cpu_count()
        else:
            return False, None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get(self,
            key: str,
            res_type: Any = any,
            default: Any = None,
            auto_convert: bool = False,
            allow_el_command: bool = False,
            save_unknown_config: bool = True) -> Any:
        """
        return the config value.
        :param key: the config name.
        :param res_type: the response type you want to get. if the value is <any>, don't check the response type.
        :param default: if can't found the config value, return default value.
        :param auto_convert: if the response type is incorrect, try convert the value.
        :param allow_el_command: use el command.
        :param save_unknown_config: save the config value with default value when can't found the config value.
        :return: config value. if can't found the config value, return default value.
                 if the response type is incorrect and can't convert the value, return default value.
        """
        if key == MocaConfig.GET_ALL_CONFIG:
            return self.__config_cache
        try:
            if allow_el_command:
                status, response = self.el_command_parser(key)
                if status:
                    value = response
                else:
                    value = self.__config_cache[key]
            else:
                value = self.__config_cache[key]
        except (KeyError, Exception):
            if save_unknown_config:
                self.set(key, default)
            return default
        if res_type is any:  # check response type
            return value
        elif isinstance(value, res_type):
            return value
        elif auto_convert:
            if res_type is str:
                return str(value)
            elif res_type is int:
                try:
                    return int(value)
                except (TypeError, ValueError, Exception):
                    return default
            elif res_type is float:
                try:
                    return float(value)
                except (TypeError, ValueError, Exception):
                    return default
            elif res_type is bool:
                return bool(value)
            elif res_type is tuple:
                try:
                    return tuple([item for item in value])
                except (TypeError, Exception):
                    return default
            elif res_type is list:
                try:
                    return [item for item in value]
                except (TypeError, Exception):
                    return default
            elif res_type is dict:
                try:
                    index = 0
                    res = {}
                    for item in value:
                        res[index] = item
                        index += 1
                except (TypeError, Exception):
                    return default
            elif res_type is set:
                try:
                    return {item for item in value}
                except (TypeError, Exception):
                    return default
            else:
                return default
        else:
            return default

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set(self,
            key: str,
            value: Any) -> bool:
        """
        set a config value.
        if the key already exists, overwrite it.
        :param key: the config name.
        :param value: the config value.
        :return: status, [success] or [failed]
        """
        try:
            self.__config_cache[key] = value
            with open(str(self.path), mode='w', encoding='utf-8') as config_file:
                dump(self.__config_cache,
                     config_file,
                     ensure_ascii=False,
                     indent=4,
                     sort_keys=False,
                     separators=(',', ': '))
            return True
        except (FileNotFoundError, PermissionError, OSError, Exception):
            del self.__config_cache[key]
            return False

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def check(self,
              key: str,
              res_type: Any,
              value: Any) -> bool:
        """
        check is value correct.
        :param key: the config name.
        :param res_type: the config value type.
        :param value: input value to check.
        :return: status, [correct] or [incorrect]
        """
        return self.get(key, res_type, allow_el_command=False) == value

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @classmethod
    def get_instance(cls,
                     name: str) -> Any:
        """Return already created instance."""
        try:
            return cls.__instance_list[name]
        except (KeyError, Exception):
            return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

# -------------------------------------------------------------------------- Main Class --

# -- Public Functions --------------------------------------------------------------------------


def run_server(config_name: str = '',
               moca_config_instance: Optional[MocaConfig] = None,
               filepath: Optional[Union[Path, str]] = None,
               filename: str = '',
               reload_interval: float = 5.0,
               port: int = 5800,
               server_access_token: str = '',
               ssl: Optional[SSLContext] = None,
               workers: int = 0,
               **kwargs) -> None:
    """
    Create a MocaConfig instance and run sanic server.
    :param config_name: the name of the MocaConfig instance
    :param moca_config_instance the instance of MocaConfig class
    :param filepath: the path of json config file.
    :param filename: the name of json config file.
    :param reload_interval: the interval to reload config file. if the value is -1, never reload config file
    :param port: server port.
    :param server_access_token: server access token.
    :param ssl: ssl context.
    :param workers: number of workers.
    :return: None.

    Raise
    _____
        MocaUsageError: if can't create MocaConfig isinstance with received arguments.
        TypeError: from MocaConfig.__init__ method
        MocaFileError: from MocaConfig.__init__ method
    """
    #############################
    if kwargs.get('mochi', False):
        server_headers['MOCHI'] = 'もっちもっちにゃんにゃん'
    #############################
    # create instance
    moca_config: MocaConfig
    if moca_config_instance is not None and isinstance(moca_config_instance, MocaConfig):
        moca_config = moca_config_instance
    elif MocaConfig.get_instance(config_name) is not None:
        moca_config = MocaConfig.get_instance(config_name)
    elif config_name != '' and filepath is not None:
        moca_config = MocaConfig(config_name, filepath, filename, reload_interval)
    else:
        raise MocaUsageError("Can't create MocaConfig instance with received arguments.")
    # set token
    moca_config.set('config_server_token', server_access_token)
    # initialize Sanic server
    app = Sanic('MocaConfig')
    app.config["API_TITLE"] = 'MocaConfig'
    app.config["API_DESCRIPTION"] = """
    EN: Common Server Side APIs for front-end applications.
    JA: フロントエンドアプリケーション開発のための、サーバーサイドの共通API。
    ZH: 为前端软件开发准备的，通用型服务器端API群。
    """
    app.config["API_TERMS_OF_SERVICE"] = 'https://www.el-ideal-ideas.com'
    app.config["API_LICENSE_NAME"] = "MIT"
    app.config["API_HOST"] = moca_config.get('config_server_host',
                                             str,
                                             default='127.0.0.1') + ':' + moca_config.get('config_server_port',
                                                                                          int,
                                                                                          default=port)
    if ssl is not None:
        app.config["API_SCHEMES"] = ["https"]
    else:
        app.config["API_SCHEMES"] = ["http"]

    # -- Route --------------------------------------------------------------------------

    @doc.tag('Redirect')
    @doc.summary('redirect to swagger document')
    @doc.description("""
        <pre>
        EN: redirect to /swagger
        JA: /swagger にリダイレクトします。
        ZH: 跳转到 /swagger
        </pre>
    """)
    async def redirect_to_swagger_route(request):
        """Redirect to swagger"""
        return redirect('/swagger')

    @doc.tag('Config')
    @doc.summary('set config')
    @doc.consumes(doc.JsonBody(
        {
            'key': doc.String(name='key', description='the config name', required=True),
            'value': doc.String(name='value', description="the config value(not only string)", required=True),
            'token': doc.String(name='token', description='server access token', required=True),
        }
    ), location='body', required=True)
    @doc.description("""
    <pre>
        EN: set a config, if already exists, overwrite it.
        JA: 設定を追加します。すでに存在している場合は上書きします。
        ZH: 添加设定。如果设定已经存在，覆盖原有设定。
    </pre>
    """)
    @doc.response(200, 'Success', description='Success')
    @doc.response(403, 'Access denied', description='Access denied')
    @doc.response(400, 'Missing required parameters', description='Missing required parameters')
    async def set_route_with_post_method(request):
        """Set config route"""
        try:
            key = request.json['key']
            value = request.json['value']
            token = request.json['token']
            if moca_config.check('config_server_token', str, token):
                moca_config.set(key, value)
                return text('Success', headers=server_headers)
            else:
                raise Forbidden('Access denied')
        except KeyError:
            raise InvalidUsage('Missing required parameters')

    @doc.tag('Config')
    @doc.summary('set config')
    @doc.consumes(doc.String(name='key', description='the config name', required=True),
                  location='query', required=True)
    @doc.consumes(doc.String(name='value', description='the config value', required=True),
                  location='query', required=True)
    @doc.consumes(doc.String(name='token', description='server access token', required=True),
                  location='query', required=True)
    @doc.description("""
    <pre>
        EN: set a config, if already exists, overwrite it.
        JA: 設定を追加します。すでに存在している場合は上書きします。
        ZH: 添加设定。如果设定已经存在，覆盖原有设定。
    </pre>
    """)
    @doc.response(200, 'Success', description='Success')
    @doc.response(403, 'Access denied', description='Access denied')
    @doc.response(400, 'Missing required parameters', description='Missing required parameters')
    async def set_route_with_get_method(request):
        """Set config route"""
        key = request.args.get('key')
        value = request.args.get('value')
        token = request.args.get('token')
        if token is not None and key is not None and value is not None:
            if moca_config.check('config_server_token', str, token):
                moca_config.set(key, value)
                return text('Success', headers=server_headers)
            else:
                raise Forbidden('Access denied')
        else:
            raise InvalidUsage('Missing required parameters')

    @doc.tag('Config')
    @doc.summary('get config')
    @doc.consumes(doc.String(name='key', description='the config name', required=True),
                  location='query', required=True)
    @doc.consumes(doc.String(name='token', description='server access token', required=True),
                  location='query', required=True)
    @doc.description("""
    <pre>
        EN: get the config value. if can't found it, return null.
            if key is "[el]#moca_get_all_config#" system will return all config value.
        JA: 設定情報を取得します。情報が存在しない場合はnullを返します。
            keyの値が"[el]#moca_get_all_config#"である場合はすべての設定の値を返します。
        ZH: 获取设定信息。如果设定不存在返回null。
            如果key的值是"[el]#moca_get_all_config#"系统会返回所有设定信息。
    </pre>
    """)
    @doc.response(200, 'config value (JSON type)', description='Success')
    @doc.response(403, 'Access denied', description='Access denied')
    @doc.response(400, 'Missing required parameters', description='Missing required parameters')
    async def get_route_with_get_method(request):
        """Get config route"""
        key = request.args.get('key')
        token = request.args.get('token')
        if key is not None and token is not None:
            if moca_config.check('config_server_token', str, token):
                if key == MocaConfig.GET_ALL_CONFIG:
                    return json(moca_config.get_all_config(), headers=server_headers)
                else:
                    return json(moca_config.get(key, any, default=None), headers=server_headers)
            else:
                raise Forbidden('Access denied')
        else:
            raise InvalidUsage('Missing required parameters')

    @doc.tag('Config')
    @doc.summary('get config')
    @doc.consumes(doc.JsonBody(
        {
            'key': doc.String(name='key', description='the config name', required=True),
            'token': doc.String(name='token', description='server access token', required=True),
        }
    ), location='body', required=True)
    @doc.description("""
    <pre>
        EN: get the config value. if can't found it, return null.
            if key is "[el]#moca_get_all_config#" system will return all config value.
        JA: 設定情報を取得します。情報が存在しない場合はnullを返します。
            keyの値が"[el]#moca_get_all_config#"である場合はすべての設定の値を返します。
        ZH: 获取设定信息。如果设定不存在返回null。
            如果key的值是"[el]#moca_get_all_config#"系统会返回所有设定信息。
    </pre>
    """)
    @doc.response(200, 'config value (JSON type)', description='Success')
    @doc.response(403, 'Access denied', description='Access denied')
    @doc.response(400, 'Missing required parameters', description='Missing required parameters')
    async def get_route_with_post_method(request):
        """Get config route"""
        try:
            key = request.json['key']
            token = request.json['token']
            if moca_config.check('config_server_token', str, token):
                if key == MocaConfig.GET_ALL_CONFIG:
                    return json(moca_config.get_all_config(), headers=server_headers)
                else:
                    return json(moca_config.get(key, any, default=None), headers=server_headers)
            else:
                raise Forbidden('Access denied')
        except KeyError:
            raise InvalidUsage('Missing required parameters')

    @doc.tag('Config')
    @doc.summary('check config')
    @doc.consumes(doc.String(name='key', description='the config name', required=True),
                  location='query', required=True)
    @doc.consumes(doc.String(name='value', description='the config value', required=True),
                  location='query', required=True)
    @doc.consumes(doc.String(name='token', description='server access token', required=True),
                  location='query', required=True)
    @doc.description("""
    <pre>
        EN: check the config value. return True or False.
        JA: 設定情報をチェックして真偽値を返します。
        ZH: 获取设定信息并且返回布尔值。
    </pre>
    """)
    @doc.response(200, 'status "true" or "false"', description='Success')
    @doc.response(403, 'Access denied', description='Access denied')
    @doc.response(400, 'Missing required parameters', description='Missing required parameters')
    async def check_route_with_get_method(request):
        """Check config route"""
        key = request.args.get('key')
        value = request.args.get('value')
        token = request.args.get('token')
        if key is not None and value is not None and token is not None:
            if moca_config.check('config_server_token', str, token):
                return json(moca_config.check(key, any, value), headers=server_headers)
            else:
                raise Forbidden('Access denied')
        else:
            raise InvalidUsage('Missing required parameters')

    @doc.tag('Config')
    @doc.summary('check config')
    @doc.consumes(doc.JsonBody(
        {
            'key': doc.String(name='key', description='the config name', required=True),
            'value': doc.String(name='value', description="the config value(not only string)", required=True),
            'token': doc.String(name='token', description='server access token', required=True),
        }
    ), location='body', required=True)
    @doc.description("""
    <pre>
        EN: check the config value. return True or False.
        JA: 設定情報をチェックして真偽値を返します。
        ZH: 获取设定信息并且返回布尔值。
    </pre>
    """)
    @doc.response(200, 'status "true" or "false"', description='Success')
    @doc.response(403, 'Access denied', description='Access denied')
    @doc.response(400, 'Missing required parameters', description='Missing required parameters')
    async def check_route_with_post_method(request):
        """Check config route"""
        try:
            key = request.json['key']
            value = request.json['value']
            token = request.json['token']
            if moca_config.check('config_server_token', str, token):
                return json(moca_config.check(key, any, value), headers=server_headers)
            else:
                raise Forbidden('Access denied')
        except KeyError:
            raise InvalidUsage('Missing required parameters')

    # -------------------------------------------------------------------------- Route --

    # -------------------------------------------------------------------------- Set Listener --

    @app.listener('after_server_stop')
    async def after_server_stop(sanic_app, loop):
        """Sanic Listener"""
        _exit(0)

    # -------------------------------------------------------------------------- Set Listener --

    # add documentation redirect route
    app.blueprint(swagger_blueprint)
    app.add_route(redirect_to_swagger_route, '/doc', methods={'GET'})
    app.add_route(redirect_to_swagger_route, '/documentation', methods={'GET'})
    # add routes
    app.add_route(set_route_with_get_method, '/set', methods={'GET'})
    app.add_route(set_route_with_post_method, '/set', methods={'POST', 'OPTIONS'})
    app.add_route(get_route_with_get_method, '/get', methods={'GET'})
    app.add_route(get_route_with_post_method, '/get', methods={'POST', 'OPTIONS'})
    app.add_route(check_route_with_get_method, '/check', methods={'GET'})
    app.add_route(check_route_with_post_method, '/check', methods={'POST', 'OPTIONS'})
    # run server
    app.run('0.0.0.0',
            port=port,
            debug=False,
            ssl=ssl,
            workers=workers,
            access_log=False)


# -------------------------------------------------------------------------- Public Functions --

# -- Run As Main --------------------------------------------------------------------------

def main():
    args = docopt(__USAGE)
    if args.get('help'):
        print(__HELP)
    elif args.get('PATH') is not None:
        try:
            config_server_name = args.get('--name')[0]
        except IndexError:
            config_server_name = 'Unknown'
        try:
            server_port = args.get('--port')[0]
        except IndexError:
            server_port = 5800
        try:
            server_token = args.get('--token')[0]
        except IndexError:
            server_token = 'mochimochi'
        try:
            worker_number = int(args.get('--worker')[0])
        except (IndexError, TypeError, ValueError):
            worker_number = 1
        try:
            interval = float(args.get('--interval')[0])
        except (IndexError, TypeError, ValueError):
            interval = 5.0
        ssl_context: Optional[SSLContext]
        try:
            cert_path = args.get('--certfile')[0]
            key_path = args.get('--keyfile')[0]
            ssl_context = create_default_context(Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(certfile=cert_path,
                                        keyfile=key_path)
        except IndexError:
            ssl_context = None
        try:
            run_server(config_name=config_server_name,
                       port=server_port,
                       filepath=args.get('PATH'),
                       reload_interval=interval,
                       ssl=ssl_context,
                       workers=worker_number,
                       server_access_token=server_token)
        except (ValueError, TypeError):
            print('-- ValueError or TypeError ------------------------------------------------------------------------')
            print("EN: Can't create the instance of the MocaConfig class, Please check your arguments.")
            print("JA: MocaConfigクラスのインスタントを作成できませんでした。コマンドの引数を確認してください。")
            print("ZH: 无法生成MocaConfig类的实例，请再次确认指令参数。")
            print('------------------------------------------------------------------------ ValueError or TypeError --')
        except MocaFileError:
            print('-- MocaFileError ------------------------------------------------------------------------')
            print("EN: Can't use this config file. Please check the file path and the file permissions.")
            print("JA: 指定されて設定ファイルが使用できません。ファイルパスとファイル権限を確認してください。")
            print("ZH: 您指定的设定文件无法使用，请再次确认文件地址和文件权限。")
            print('------------------------------------------------------------------------ MocaFileError --')
    else:
        print(EL_S)
        sleep(1)
        print("""
        ----------------------------------------------------------------------------
        ----------------------------------------------------------------------------
        This is the config module developed by el.ideal-ideas for Moca System.
        This config module is json based.
        All config data in the json file, will be loaded into memory, and can be used from MocaConfig class.
        MocaConfig class will reload the json file in 5(default value) seconds.
        If the json file was changed. the new config value will overwrite the old config value that in memory.
        -------
        これはモカシステムのためにel.ideal-ideasによって開発された設定モジュールである。
        この設定モジュールはJSON形式を採用しています。
        JSONファイル内のすべての設定情報はメモリ内にロードされ、そしてMocaConfigクラスを経由して取得できます。
        MocaConfigクラスはデフォルト設定では5秒ごとJSONファイルをリロードします。
        JSONファイルに変更があった場合、その変更はメモリ内の設定情報にも反映されます。
        -------
        这是el.ideal-ideas为茉客系统开发的设定模块。
        这个设定模块采用了JSON格式。
        JSON文件内的所有设定信息会被保存到内存里，您可以通过MocaConfig类来获取各种设定信息。
        MocaConfig类会每5（初期值）秒重新读取一次JSON文件。
        如果JSON文件被改写，内存内的设定信息也会和JSON文件同步。
        ----------------------------------------------------------------------------
        ----------------------------------------------------------------------------
        """)
        sleep(1)
        print(__USAGE)


if __name__ == '__main__':
    main()

# -------------------------------------------------------------------------- Run As Main --
