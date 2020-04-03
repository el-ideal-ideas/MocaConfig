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
Copyright (c) 2020.1.17 [el.ideal-ideas]
This software is released under the MIT License.
see LICENSE.txt or following URL.
https://www.el-ideal-ideas.com/MocaLog/LICENSE/
"""


# -- Imports --------------------------------------------------------------------------

from typing import *
from pathlib import Path
from json import load, dump, JSONDecodeError, dumps, loads
from time import sleep
from datetime import datetime
from random import choice, randint
from string import ascii_letters, digits
from uuid import uuid1, uuid4
from multiprocessing import current_process, cpu_count
from base64 import b64encode, b64decode
from traceback import print_exc
from os import stat
from threading import Thread
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from typing import Optional

# -------------------------------------------------------------------------- Imports --

# -- Variables --------------------------------------------------------------------------

VERSION = '3.0.0'

# -------------------------------------------------------------------------- Variables --

# -- MocaConfig --------------------------------------------------------------------------


class MocaConfig(object):
    """
    -- english --------------------------------------------------------------------------
    This is the config module developed by el.ideal-ideas for Moca System.
    This config module is json based.
    All config data in the json file, will be loaded into memory, and can be used from MocaConfig class.
    MocaConfig class will reload the json file in 1(default value) seconds If it was changed.
    If the json file was changed. the new config value will overwrite the old config value that in memory.
    If the config file contains "__private__": True, the config file will be a private file.
    If the config key is starts with "_" , the config will be a private config.
    If you want to access the private config, you should input the access token or the root password.

    -- 日本語 --------------------------------------------------------------------------
    これはモカシステムのためにel.ideal-ideasによって開発された設定モジュールである。
    この設定モジュールはJSON形式を採用しています。
    JSONファイル内のすべての設定情報はメモリ内にロードされ、そしてMocaConfigクラスを経由して取得できます。
    MocaConfigクラスはデフォルト設定では1秒ごとJSONファイルをリロードします(変更があった場合)。
    JSONファイルに変更があった場合、その変更はメモリ内の設定情報にも反映されます。
    設定ファイルが"__private__": True,を含む場合、その設定ファイルはプライベートな設定ファイルになります。
    "_"から始まる設定内容も同様にプライベートになります。
    プライベートな設定情報にアクセスする場合、アクセストークンまたはrootパスワードが必要になります。

    -- 中文 --------------------------------------------------------------------------
    这是el.ideal-ideas为茉客系统开发的设定模块。
    这个设定模块采用了JSON格式。
    JSON文件内的所有设定信息会被保存到内存里，您可以通过MocaConfig类来获取各种设定信息。
    MocaConfig类会每1（初期值）秒重新读取一次JSON文件（如果有变更）。
    如果JSON文件被改写，内存内的设定信息也会和JSON文件同步。
    如果设定文件包含"__private__": True,该设定文件则为隐私文件。
    如果设定key由"_"开始，该设定则为隐私设定。
    访问隐私设定的时候，需要输入access-token或者root密码。

    Attributes
    ----------
    _path: Path
        the config file path

    _reload_interval: float
        the reload interval

    _config_cache: dict
        config cache

    _status: int
        the status of config module, 0 is correct

    _handlers: Dict[str, List]
        the handlers

    _handled_keys: Dict[str, List[str]]
        the keys handled by handlers.

    _timestamp: Optional[int]
        the timestamp of the config file.
        
    _name: str
        the name of this instance.
    """

    _INIT_MSG = {
        "__MocaConfig__": "Welcome to MocaConfig, the config module is now available.",
        "__MocaConfig_version__": VERSION,
        "__private__": False,
    }

    _ROOT_PASS = ''

    _instance_list: dict = {}

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
    MOCHI: str = '[el]#moca_mochi#'  # もっちもっちにゃんにゃん

    def __init__(self,
                 name: str,
                 filepath: Union[Path, str],
                 filename: str = '',
                 reload_interval: float = 1.0,
                 access_token: str = '',
                 debug_mode: bool = False,
                 **kwargs):
        """
        The initializer of MocaConfig class.
        :param name: the name of this instance
        :param filepath: the path of json config file.
        :param filename: the name of json config file.
        :param reload_interval: the interval to reload config file. if the value is -1, never reload config file
        :param access_token: the access token of config file.
        :param debug_mode: turn on debug mode.

        Raise
        -----
            TypeError: if the arguments type is incorrect.
        """
        # set name
        self._name: str = name
        # set debug mode
        self._debug_mode = debug_mode
        # initialize timestamp variable
        self._timestamp: Optional[float] = None
        # initialize handlers dictionary
        self._handlers: Dict[str, List] = {}
        # initialize handled keys list
        self._handled_keys: Dict[str, List[str]] = {}
        #############################
        if kwargs.get('mochi', False):
            MocaConfig._INIT_MSG['__mochi__'] = 'もっちもっちにゃんにゃん'
        #############################
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
        self._path: Path = self.change_config_file_path(path)
        # set reload interval
        if isinstance(reload_interval, float) or isinstance(reload_interval, int):
            self._reload_interval: float = float(reload_interval)
        else:
            TypeError('Argument type error, '
                      'Expected reload_interval: float, '
                      f'But received reload_interval: {type(reload_interval)}')
        # initialize cache variable
        self._config_cache: dict = {}
        # set current status
        self._status: int = MocaConfig.CORRECT
        # load config file
        self.reload_config()
        # start reload-config-loop on other thread
        Thread(target=self._reload_config_loop, name='reload_config_loop', daemon=True).start()
        # initialize access token
        self.get('__moca_config_access_token__', access_token, root_pass=MocaConfig._ROOT_PASS)
        # initialize config name
        self.get('__config_instance_name__', name, root_pass=MocaConfig._ROOT_PASS)
        # write version
        self.set('__MocaConfig_version__', VERSION, root_pass=MocaConfig._ROOT_PASS)
        # add self to instance list
        MocaConfig._instance_list[name] = self

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def status(self) -> int:
        """Return the self.__status"""
        return self._status

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def name(self) -> str:
        """Return the self.__name"""
        return self._name

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @classmethod
    def set_root_pass(cls,
                      password: str) -> bool:
        """
        Root password only can set once.
        :param password: the root password.
        :return: status, [success] or [failed]
        """
        if cls._ROOT_PASS == '':
            cls._ROOT_PASS = password
            return True
        else:
            return False

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @classmethod
    def change_root_pass(cls,
                         new_password: str,
                         old_password: str) -> bool:
        """
        Change the root password.
        :param new_password: the new root password.
        :param old_password: the old root password.
        :return: status, [success] or [failed]
        """
        if cls._ROOT_PASS == old_password:
            cls._ROOT_PASS = new_password
            return True
        else:
            return False

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def path(self) -> Path:
        """Return the self.__path"""
        return self._path

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @property
    def reload_interval(self) -> float:
        """Return the self.__reload_interval"""
        return self._reload_interval

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @classmethod
    def get_instance_list(cls) -> List[str]:
        """Return a list of instance names"""
        return list(cls._instance_list.keys())

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def change_reload_interval(self,
                               interval: float) -> None:
        """Change the reload interval"""
        self._reload_interval = interval

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def stop_auto_reload(self) -> None:
        """Stop auto reload"""
        self._reload_interval = -1

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def change_config_file_path(self,
                                path: Union[Path, str]) -> Path:
        """
        Change the path of config file.
        :param path: the path of the config file.
        :return: the path of the config file.
        """
        config_file_path: Path
        if isinstance(path, str):
            config_file_path = Path(path)
        else:
            config_file_path = path
        # try create parent directory.
        config_file_path.parent.mkdir(parents=True, exist_ok=True)
        if not config_file_path.is_file():  # if file is not exists, create new file.
            with open(str(config_file_path), mode='w', encoding='utf-8') as config_file:
                dump(MocaConfig._INIT_MSG,
                     config_file,
                     ensure_ascii=False,
                     indent=4,
                     sort_keys=False,
                     separators=(',', ': '))
        self._path = config_file_path
        return config_file_path

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def reload_config(self) -> None:
        """Reload json config file."""
        try:
            time = stat(str(self._path)).st_mtime
            if (self._timestamp is None) or (time != self._timestamp):
                with open(str(self._path), mode='r', encoding='utf-8') as config_file:
                    new_cache = load(config_file)
                    old_cache = self._config_cache
                    self._config_cache = new_cache
                    self._run_handler_total(old_cache, new_cache)
            self._timestamp = time
            self._status = MocaConfig.CORRECT
        except JSONDecodeError:
            if self._debug_mode:
                print_exc()
            self._status = MocaConfig.DECODE_ERROR
        except FileNotFoundError:
            if self._debug_mode:
                print_exc()
            self._status = MocaConfig.FILE_NOT_FOUND
        except PermissionError:
            if self._debug_mode:
                print_exc()
            self._status = MocaConfig.PERMISSION_ERROR
        except OSError:
            if self._debug_mode:
                print_exc()
            self._status = MocaConfig.OS_ERROR
        except Exception:
            if self._debug_mode:
                print_exc()
            self._status = MocaConfig.UNKNOWN_ERROR

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

    def _reload_config_loop(self) -> None:
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
        return len(self._config_cache)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get_all_config(self,
                       access_token: str = '',
                       root_pass: str = '') -> Optional[dict]:
        """
        Return all config.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: if can't access to the config file, return None
        """
        if self.is_private():
            if (MocaConfig._ROOT_PASS == root_pass) or bool(self.check_access_token(access_token,
                                                                                    MocaConfig._ROOT_PASS)):
                return self._config_cache
            else:
                return None
        else:
            if (MocaConfig._ROOT_PASS == root_pass) or bool(self.check_access_token(access_token,
                                                                                    MocaConfig._ROOT_PASS)):
                return self._config_cache
            else:
                return {key: value for key, value in self._config_cache.items() if not key.startswith('_')}

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get_all_config_key(self,
                           access_token: str = '',
                           root_pass: str = '') -> Optional[Tuple]:
        """
        Return all key in self.__config_cache.
        If the access token or root password is correct, the response will contains private configs.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: if can't access to the config file, return None
        """
        if self.is_private():
            if (MocaConfig._ROOT_PASS == root_pass) or bool(self.check_access_token(access_token,
                                                                                    MocaConfig._ROOT_PASS)):
                return tuple(self._config_cache.keys())
            else:
                return None
        else:
            if (MocaConfig._ROOT_PASS == root_pass) or bool(self.check_access_token(access_token,
                                                                                    MocaConfig._ROOT_PASS)):
                return tuple(self._config_cache.keys())
            else:
                return tuple([key for key in self._config_cache.keys() if not key.startswith('_')])

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
        if isinstance(command, str):
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
            elif command == cls.MOCHI:
                return True, 'もっちもっちにゃんにゃん'
            else:
                return False, None
        else:
            return False, None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def _is_allowed(self,
                    key: str,
                    root_pass: str,
                    access_token: str) -> bool:
        """Check is access allowed."""
        allow: bool
        if self.is_private():
            if (MocaConfig._ROOT_PASS == root_pass) or bool(self.check_access_token(access_token,
                                                                                    MocaConfig._ROOT_PASS)):
                allow = True
            else:
                allow = False
        else:
            if key.startswith('_'):
                if (MocaConfig._ROOT_PASS == root_pass) or bool(self.check_access_token(access_token,
                                                                                        MocaConfig._ROOT_PASS)):
                    allow = True
                else:
                    allow = False
            else:
                allow = True
        return allow

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get(self,
            key: str,
            res_type: Any = any,
            default: Any = None,
            auto_convert: bool = False,
            allow_el_command: bool = False,
            save_unknown_config: bool = True,
            access_token: str = '',
            root_pass: str = '') -> Any:
        """
        return the config value.
        :param key: the config name.
        :param res_type: the response type you want to get. if the value is <any>, don't check the response type.
        :param default: if can't found the config value, return default value.
        :param auto_convert: if the response type is incorrect, try convert the value.
        :param allow_el_command: use el command.
        :param save_unknown_config: save the config value with default value when can't found the config value.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: config value. if can't found the config value, return default value.
                 if the response type is incorrect and can't convert the value, return default value.
                 if can't access to the config file, return default value.
        """
        if self._is_allowed(key, root_pass, access_token):
            try:
                if allow_el_command:
                    if key == MocaConfig.GET_ALL_CONFIG:
                        return self._config_cache
                    status, response = self.el_command_parser(key)
                    if status:
                        value = response
                    else:
                        value = self._config_cache[key]
                else:
                    value = self._config_cache[key]
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
        else:
            return default

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def _save_config_to_file(self) -> bool:
        """
        Save the config data to config file
        :return: status, [success] or [failed]
        """
        try:
            json_string = dumps(self._config_cache,
                                ensure_ascii=False,
                                indent=4,
                                sort_keys=True,
                                separators=(',', ': '))
            with open(str(self.path), mode='w', encoding='utf-8') as config_file:
                config_file.write(json_string)
            return True
        except FileNotFoundError:
            if self._debug_mode:
                print_exc()
            self.__status = MocaConfig.FILE_NOT_FOUND
            return False
        except PermissionError:
            if self._debug_mode:
                print_exc()
            self.__status = MocaConfig.PERMISSION_ERROR
            return False
        except OSError:
            if self._debug_mode:
                print_exc()
            self.__status = MocaConfig.OS_ERROR
            return False
        except Exception:
            if self._debug_mode:
                print_exc()
            self.__status = MocaConfig.UNKNOWN_ERROR
            return False

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set(self,
            key: str,
            config_value: Any,
            allow_el_command: bool = False,
            access_token: str = '',
            root_pass: str = '') -> Optional[bool]:
        """
        set a config value.
        if the key already exists, overwrite it.
        :param key: the config name.
        :param config_value: the config value.
        :param allow_el_command: use el command.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [success] or [failed], If can't access to the config file return None
        """
        if self._is_allowed(key, root_pass, access_token):
            try:
                _ = dumps(config_value)
                value = config_value
            except TypeError:
                value = str(config_value)
            if allow_el_command:
                status, response = self.el_command_parser(value)
                if status:
                    new_value = response
                else:
                    new_value = value
            else:
                new_value = value
            try:
                old_value = self._config_cache[key]
            except KeyError:
                old_value = None
            self._config_cache[key] = new_value
            res = self._save_config_to_file()
            if res:
                if old_value is not None:
                    self._run_handler_one(key, old_value, new_value)
                return True
            else:
                try:
                    del self._config_cache[key]
                except KeyError:
                    pass
                return False
        else:
            return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def remove_config(self,
                      key: str,
                      access_token: str = '',
                      root_pass: str = '') -> Optional[bool]:
        """
        Remove a config data.
        :param key: the config key.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [success] or [failed]. If can't access to this config file. return None.
        """
        if self._is_allowed(key, root_pass, access_token):
            try:
                value = self._config_cache[key]
                del self._config_cache[key]
                res = self._save_config_to_file()
                if res:
                    return True
                else:
                    self._config_cache[key] = value
                    return False
            except KeyError:
                return False
        else:
            return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def check(self,
              key: str,
              res_type: Any,
              value: Any,
              access_token: str = '',
              root_pass: str = '') -> bool:
        """
        check is value correct.
        :param key: the config name.
        :param res_type: the config value type.
        :param value: input value to check.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [correct] or [incorrect].
        """
        return self.get(key, res_type, allow_el_command=False,
                        access_token=access_token, root_pass=root_pass, default='[el]#moca_null#') == value

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @classmethod
    def get_instance(cls,
                     name: str) -> Any:
        """Return already created instance."""
        try:
            return cls._instance_list[name]
        except (KeyError, Exception):
            return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set_config_private(self) -> bool:
        """
        Set the config private. Can't access without access token.
        :return: status, [success] or [failed]
        """
        return bool(self.set('__private__', True, root_pass=MocaConfig._ROOT_PASS))

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set_config_public(self,
                          access_token: str = '',
                          root_pass: str = '') -> Optional[bool]:
        """
        Set the config public. Can access without access token.'
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [success] or [failed]
        """
        return self.set('__private__', False, access_token=access_token, root_pass=root_pass)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def is_private(self) -> bool:
        """Check is config private"""
        try:
            return bool(self._config_cache['__private__'])
        except (TypeError, ValueError, Exception):
            return True

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set_access_token(self,
                         token: str,
                         root_pass: str = '') -> Optional[bool]:
        """
        Set a access token for config file.
        :param root_pass: the root password.
        :param token: the access token of config file.
        :return status, [success] or [failed]. If can't access to this config file. return None.
        """
        return self.set('__moca_config_access_token__', token, root_pass=root_pass)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def check_access_token(self,
                           token: str,
                           root_pass: str = '') -> Optional[bool]:
        """
        Check is the access token of config file correct.
        :param token: config file access token.
        :param root_pass: the root password.
        :return: status, [correct] or [incorrect].
        If can't access to this config file. return None.
        If root password is incorrect return None.
        If some other error occurred return None.
        """
        try:
            if MocaConfig._ROOT_PASS == root_pass:
                return self._config_cache['__moca_config_access_token__'] == token
            else:
                return None
        except IndexError:
            return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def delete_this_config_file(self,
                                access_token: str = '',
                                root_pass: str = '') -> bool:
        """
        Delete the config file.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [success] or [failed]
        """
        if (MocaConfig._ROOT_PASS == root_pass) or bool(self.check_access_token(access_token,
                                                                                MocaConfig._ROOT_PASS)):
            try:
                self._path.unlink()
                return True
            except (FileNotFoundError, PermissionError, OSError, Exception):
                if self._debug_mode:
                    print_exc()
                return False
        else:
            return False

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def mochi() -> str:
        """٩(ˊᗜˋ*)و"""
        return 'もっちもっちにゃんにゃん'

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def print_mochi() -> None:
        """♫ヽ(゜∇゜ヽ)♪"""
        print(MocaConfig.mochi())

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def _create_aes(password: str,
                    iv: bytes):
        """
        create aes object
        :param password: password
        :param iv: initialization vector
        :return: aes object
        """
        sha256_hash = SHA256.new()
        sha256_hash.update(password.encode())
        hashed_key = sha256_hash.digest()
        return AES.new(hashed_key, AES.MODE_CFB, iv)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def encrypt(data: bytes,
                password: str) -> bytes:
        """
        encrypt data
        :param data: plain data
        :param password: password
        :return: encrypted data
        """
        iv = Random.new().read(AES.block_size)
        return iv + MocaConfig._create_aes(password, iv).encrypt(data)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def decrypt(data: bytes,
                password: str) -> bytes:
        """
        decrypt data
        :param data: encrypted data
        :param password: password
        :return: plain data
        """
        iv, cipher = data[:AES.block_size], data[AES.block_size:]
        return MocaConfig._create_aes(password, iv).decrypt(cipher)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def encrypt_string(text: str,
                       password: str) -> Optional[str]:
        """
        encrypt string data.
        :param text: target string.
        :param password: password.
        :return: encrypted string. if password is incorrect, return None
        """
        try:
            encrypted_bytes = MocaConfig.encrypt(text.encode(), password)
            return b64encode(encrypted_bytes).decode()
        except UnicodeDecodeError:
            return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @staticmethod
    def decrypt_string(text: str,
                       password: str) -> Optional[str]:
        """
        decrypt string data.
        :param text: encrypted string.
        :param password: password.
        :return: plain string. if password is incorrect, return None
        """
        plain_bytes = MocaConfig.decrypt(b64decode(text), password)
        return plain_bytes.decode()

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def set_and_encrypt(self,
                        key: str,
                        value: Any,
                        encrypt_pass: str,
                        access_token: str = '',
                        root_pass: str = '') -> Optional[bool]:
        """
        set a config value and encrypt it in the config file.
        if the key already exists, overwrite it.
        :param key: the config name.
        :param value: the config value.
        :param encrypt_pass: the password to decrypt the config.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [success] or [failed], If can't access to the config file return None
        """
        json_string = dumps(value)
        encrypted_value = MocaConfig.encrypt(json_string.encode('utf-8'), password=encrypt_pass)
        encrypted_string = b64encode(encrypted_value).decode('utf-8')
        return self.set(key, encrypted_string, access_token=access_token, root_pass=root_pass)

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get_encrypted_config(self,
                             key: str,
                             encrypt_pass: str,
                             res_type: Any = any,
                             default: Any = None,
                             auto_convert: bool = False,
                             allow_el_command: bool = False,
                             save_unknown_config: bool = True,
                             access_token: str = '',
                             root_pass: str = '') -> Any:
        """
        return the config value.
        :param key: the config name.
        :param encrypt_pass: the password to decrypt the config.
        :param res_type: the response type you want to get. if the value is <any>, don't check the response type.
        :param default: if can't found the config value, return default value.
        :param auto_convert: if the response type is incorrect, try convert the value.
        :param allow_el_command: use el command.
        :param save_unknown_config: save the config value with default value when can't found the config value.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: config value. if can't found the config value, return default value.
                 if the response type is incorrect and can't convert the value, return default value.
                 if can't access to the config file, return default value.
        """
        moca_null = '[el]#moca_null#'
        encrypted_string = self.get(key,
                                    res_type,
                                    moca_null,
                                    auto_convert,
                                    allow_el_command,
                                    save_unknown_config,
                                    access_token, root_pass)
        if encrypted_string == moca_null:
            return default
        else:
            encrypted_value = b64decode(encrypted_string.encode('utf-8'))
            plain_value = MocaConfig.decrypt(encrypted_value, encrypt_pass).decode()
            try:
                return loads(plain_value)
            except JSONDecodeError:
                return default

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def add_handler(self,
                    name: str,
                    keys: Union[List[str], str],
                    handler: Callable,
                    args: Tuple = (),
                    kwargs: Dict = {}) -> None:
        """
        Add a handler to do something when the config value was changed.
        :param name: the name of this handler. if same name is already exists, overwrite it.
        :param keys: the keys of the config.
        :param handler: the handler function.  arguments(the_updated_key, old_value, new_value, *args, **kwargs)
        :param args: arguments to the handler.
        :param kwargs: keyword arguments to the handler.
        :return: None
        """
        self._handlers[name] = [keys, handler, args, kwargs]
        if isinstance(keys, str):
            try:
                self._handled_keys[keys].append(name)
            except KeyError:
                self._handled_keys[keys] = [name, ]
        else:
            for key in keys:
                try:
                    self._handled_keys[key].append(name)
                except KeyError:
                    self._handled_keys[key] = [name]

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def remove_handler(self,
                       name: str) -> None:
        """Remove the registered handler"""
        try:
            del self._handlers[name]
            for key in self._handled_keys:
                try:
                    self._handled_keys[key].remove(name)
                except ValueError:
                    pass
        except KeyError:
            pass

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def get_handler(self,
                    name: str) -> Optional[Callable]:
        """Get the registered handler"""
        try:
            return self._handlers[name][1]
        except KeyError:
            return None

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def _run_handler_total(self,
                           old_cache: dict,
                           new_cache: dict) -> None:
        """Run the handlers if needed."""
        for key in self._handled_keys:
            try:
                if old_cache[key] != new_cache[key]:
                    for name in self._handled_keys[key]:
                        try:
                            self._handlers[name][1](key,
                                                    old_cache[key],
                                                    new_cache[key],
                                                    *self._handlers[name][2],
                                                    **self._handlers[name][3])
                        except SystemExit:
                            raise
                        except Exception:
                            if self._debug_mode:
                                print_exc()
            except KeyError:
                pass

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def _run_handler_one(self,
                         key: str,
                         old_value: Any,
                         new_value: Any) -> None:
        """Run the handlers if needed."""
        try:
            for name in self._handled_keys[key]:
                try:
                    self._handlers[name][1](key,
                                            old_value,
                                            new_value,
                                            *self._handlers[name][2],
                                            **self._handlers[name][3])
                except SystemExit:
                    raise
                except Exception:
                    if self._debug_mode:
                        print_exc()
        except KeyError:
            pass

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    def change_name(self,
                    name: str) -> None:
        """Change the name of the instance."""
        try:
            del MocaConfig._instance_list[self._name]
        except KeyError:
            pass
        self._name = name
        MocaConfig._instance_list[name] = self

    # ----------------------------------------------------------------------------
    # ----------------------------------------------------------------------------

    @classmethod
    def load_config_files(cls,
                          config_dir: Union[Path, str]) -> int:
        """
        Load all config files in the config directory.
        :param config_dir: the path to the config directory.
        :return: the number of loaded config files. If config_dir is not a directory, return -1.
        """
        count = 0
        # set target directory
        target: Path
        if isinstance(config_dir, str):
            target = Path(config_dir)
        else:
            target = config_dir
        if target.is_dir():  # check target directory
            config_file_list = [item for item in list(target.iterdir()) if item.is_file()]
        else:
            return -1
        for config_file in config_file_list:
            try:
                with open(str(config_file), mode='r', encoding='utf-8') as config:
                    try:
                        value = load(config)
                        if isinstance(value, dict):
                            cls(value.get('__config_instance_name__', uuid4().hex), config_file)
                            count += 1
                        else:
                            pass
                    except JSONDecodeError:
                        pass
            except (FileNotFoundError, PermissionError, OSError, Exception):
                pass
        return count

# -------------------------------------------------------------------------- MocaConfig --
