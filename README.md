# System Requirements
- Python >= 3.7
- sanic
- sanic_openapi
- docopt

# Installation
```
pip install moca_config==1.0.7
or
pip install moca_config
```

# Overview
##### English
This is the config module developed by el.ideal-ideas for Moca System.
This config module is json based.
All config data in the json file, will be loaded into memory, and can be used from MocaConfig class.
MocaConfig class will reload the json file in 5(default value) seconds.
If the json file was changed. the new config value will overwrite the old config value that in memory.
---
##### 日本語
これはモカシステムのためにel.ideal-ideasによって開発された設定モジュールである。
この設定モジュールはJSON形式を採用しています。
JSONファイル内のすべての設定情報はメモリ内にロードされ、そしてMocaConfigクラスを経由して取得できます。
MocaConfigクラスはデフォルト設定では5秒ごとJSONファイルをリロードします。
JSONファイルに変更があった場合、その変更はメモリ内の設定情報にも反映されます。
---
##### 简体中文
这是el.ideal-ideas为茉客系统开发的设定模块。
这个设定模块采用了JSON格式。
JSON文件内的所有设定信息会被保存到内存里，您可以通过MocaConfig类来获取各种设定信息。
MocaConfig类会每5（初期值）秒重新读取一次JSON文件。
如果JSON文件被改写，内存内的设定信息也会和JSON文件同步。

# Usage Example
###### Use in your application
```python
# Create a instance.
# インスタンス化。
# 创建实例。
moca_config = MocaConfig('test', './test/test.json')
# Try get language config. 
# if lang info is in the json file and it is string type,
# return the value, if not, return default value.
# 言語設定の取得を試みます。
# もしlang項目がJSONファイルにありかつ文字列形式である場合。その値を返します。
# 他の場合はデフォルト値を返します。
# 尝试获取语言设定。
# 如果JSON文件里面有名为lang的数据，并且是文字列格式的话，返回其值。
# 其他情况返回初始值。
moca_config.get('lang', str, default='english')
# Set a config value, and update the json file.
# 設定情報を追加してJSONファイルを更新します。
# 添加设定信息并且更新JSON文件
moca_config.set('lang', 'english')
```
###### Use in terminal
MocaConfig can run as a standalone api(set or get config and so on) server.
For more details, please read api documentation(swagger).

MocaConfigは独立動作する設定に関する機能と提供APIサーバーとしても使用可能。
詳細に関してはswaggerによって作られたAPIドキュメントをご覧ください。

MocaConfig也可以作为一个独立运行的提供关于设定的API服务器。
详细信息请看用swagger生成的API文档。

```bash
moca_config ./config/config.json -p 5901 
```

# MocaConfig Class
###### For more information please read the document in the source code.

#### Attributes
- path
    - This is the path to the json file. The type of the data is instance of pathlib.Path.
    - これはJSONファイルのパスです。データ型はpathlib.Pathのインスタンスです。
    - 这是JSON文件的地址。数据类型是pathlib.Path的实例。
- reload_interval
    - This is the interval to reload the json file. The type of the data is float.
    - この値はJSONファイルの再読み込みインターバルです。データ型はfloatである。
    - 这个值是JSON文件的重读间隔。数据类型是float。
- status(read-only)
    - This value shows the status of the instance. The type of the data is int.
        - 0: correct.
        - 1: can't decode the json file.
        - 2: can't found the json file.
        - 3: can't load the json file(permission error).
        - 4: can't load the json file(os error).
        - 5: can't load the json file(unknown error).
    - この値はインスタンスの動作状態を表します。データ型はintである。
        - 0: 正常。
        - 1: JSONファイルのデコードに失敗しました。
        - 2: JSONファイルが見つかりません。
        - 3: JSONファイルを読み込めません(権限エラー)。
        - 4: JSONファイルを読み込めません(OSエラー)。
        - 5: JSONファイルを読み込めません(不明なエラー)。
    - 这个值代表实例的运行状态。数据类型是int。
        - 0: 正常。
        - 1: 无法解析JSON文件。
        - 2: 无法找到JSON文件。
        - 3: 无法读取JSON文件(权限异常)。
        - 4: 无法读取JSON文件(OS异常)。
        - 5: 无法读取JSON文件(未知异常)。
  
#### Special Value
###### Following values may have special meaning in some methods.

```python3
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
```

###### For example

```python3
moca_config = MocaConfig('example', './example.json')
print(moca_config.get('[el]#moca_now#'))
print(moca_config.get(MocaConfig.NOW))
# output
# 2020-01-17 13:23:59.486562
# 2020-01-17 13:23:59.486562
```

#### Public Methods

###### Main Methods
- def get_config_size() -> int:
    - Return the size of the config directory.
    - 設定情報の数を返す。
    - 返回设定信息的数量。
    
- def get_all_config() -> dict:
    - Return all configs as a dictionary
    - すべての設定情報を一つの辞書として返します。
    - 以字典格式返回所有的设定信息。
    
- def get_all_config_key() -> tuple:
    - Return all config keys
    - すべての設定の項目名を返す。
    - 返回所有设定的名称。
    
- def get(key: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False) -> Any:
    - Return the value of config.
    - 設定の値を返す。
    - 返回设定的值。
```python
def get(self,
        key: str,
        res_type: Any = any,
        default: Any = None,
        auto_convert: bool = False,
        allow_el_command: bool = False) -> Any:
    """
    return the config value.
    :param key: the config name.
    :param res_type: the response type you want to get. if the value is <any>, don't check the response type.
    :param default: if can't found the config value, return default value.
    :param auto_convert: if the response type is incorrect, try convert the value.
    :param allow_el_command: use el command.
    :return: config value. if can't found the config value, return default value.
             if the response type is incorrect and can't convert the value, return default value.
    """
```
    
- def set(key: str, value: Any) -> bool:
    - Set a value of config.
    - 値を設定項目に設定します。
    - 添加一个设定值。
```python
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
```
    
- def check(key: str, res_type: Any, value: Any) -> bool:
    - Check the value is same or not with config value.
    - 値が設定値と等しいかどうかをチェックします。
    - 检测参数值是否和设定值相同。
```python
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
```

###### Optional Methods

- def reload_config() -> None:
    - Reload json config file manually.
    - JSON設定ファイルを手動で再読み込みします。
    - 手动重读JSON设定文件。
    
- def random_string(length: int) -> str:
    - Return random string with length argument.
    - 指定した長さのランダムな文字列を返す。
    - 返回指定长度的随机文字列。
    
- random_integers(length: int) -> str:
    - Return random string that made up of integers with length argument.
    - 指定した長さのランダムな数字によって構成された文字列を返す。
    - 返回指定长度的由随机数字组成的文字列。
    
- def random_integer_list(length: int) -> List[int]:
    - Return a list made up of random integers with length argument.
    - 指定した長さのランダムな数値によって構成されたリストを返す。
    - 返回一个指定长度的由随机数字组成的数组。
    
- def el_command_parser(command: str) -> Tuple[bool, Any]:
    - Parse the special constants.
    - 特殊キーワードの解析用メソッド。
    - 用于解析特殊值的方法。
    
- def get_instance(name: str) -> Any:
    - Get the created instance by name.
    - 名前によって生成済みのインスタンスを取得します。
    - 通过名字获取已生成的实例。
    
# Public Functions
This Module only has one public function.
The run_server function can run a standalone config server.
About config server API please read swagger document in following URL.
API Document URL: `<your ip>:<your port>/doc`

このモジュールには１つだけ公開された関数があります。
run_server関数を用いることで独立動作する設定サーバーを起動できます。
設定サーバーのAPIに関してはswaggerを使用したドキュメントが用意されています。
APIドキュメントのURL: `<your ip>:<your port>/doc`

这个模块仅包含一个公开函数。
通过run_server这个函数可以启动一个可以独立运行的设定服务器。
设定服务器有自己的用swagger创建的API文档。
API文档地址: `<your ip>:<your port>/doc`

```python
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
        ValueError: if can't create MocaConfig isinstance with received arguments.
        TypeError: from MocaConfig.__init__ method
        MocaFileError: from MocaConfig.__init__ method
    """
```

# Global command
This module will install a global command in your system.
You can use it with `moca_config` command in your terminal.

このモジュールはシステムにグローバルなコマンドを追加します。
`moca_config`という名前でターミナルから使用可能です。

本模块还会在系统内安装一个全局指令。
您可以在终端通过`moca_config`指令来使用。
```
    Usage:
        moca_config
        moca_config help
        moca_config PATH [-p|--port <PORT>] [-n|--name <NAME>] [-t|--token <TOKEN>] [-w|--workers <WORKERS>] 
                         [-c|--certfile <CERT_PATH>] [-k|--keyfile <KEY_PATH>] [-i|--interval <RELOAD_INTERVAL>] 

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
```

# Public Variables

- config_routes_v1: Blueprint
    - You can use this variable add config server apis to other sanic server.
    - この変数を使用して設定サーバーのAPIを他のsanicサーバーに追加できます。
    - 使用这个变量可以把设定服务器的API添加到其他的sanic服务器里面。
    
# License

- MIT License

```
Copyright 2020.1.17 <el.ideal-ideas: https://www.el-ideal-ideas.com>

Permission is hereby granted, free of charge, 
to any person obtaining a copy of this software 
and associated documentation files (the "Software"),
to deal in the Software without restriction, 
including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons
to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF 
ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED 
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, 
DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH 
THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
    
# Other Information
- el.ideal-ideas
    - https://www.el-ideal-ideas.com
- Sanic
    - https://github.com/huge-success/sanic
- Sanic License Info
    - https://github.com/huge-success/sanic-openapi/blob/master/LICENSE
- Sanic OpenAPI License Info
    - https://github.com/huge-success/sanic-openapi/blob/master/LICENSE
- Docpt License Info
    - https://github.com/docopt/docopt/blob/master/LICENSE-MIT
