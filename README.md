# System Requirements
- Python >= 3.7
- moca_core

# Installation
```
pip install moca_config==1.5.2
or
pip install moca_config
```

# Overview
##### English
This is the config module developed by el.ideal-ideas for Moca System.
This config module is json based.
All config data in the json file, will be loaded into memory, and can be used from MocaConfig class.
MocaConfig class will reload the json file in 1(default value) seconds If it was changed.
If the json file was changed. the new config value will overwrite the old config value that in memory.
If the config file contains `"__private__": True,` the config file will be a private file.
If the config key is starts with `"_"` , the config will be a private config.
If you want to access the private config, you should input the access token or the root password.

---
##### 日本語
これはモカシステムのためにel.ideal-ideasによって開発された設定モジュールである。
この設定モジュールはJSON形式を採用しています。
JSONファイル内のすべての設定情報はメモリ内にロードされ、そしてMocaConfigクラスを経由して取得できます。
MocaConfigクラスはデフォルト設定では1秒ごとJSONファイルをリロードします(変更があった場合)。
JSONファイルに変更があった場合、その変更はメモリ内の設定情報にも反映されます。
設定ファイルが`"__private__": True,`を含む場合、その設定ファイルはプライベートな設定ファイルになります。
`"_"`から始まる設定内容も同様にプライベートになります。
プライベートな設定情報にアクセスする場合、アクセストークンまたはrootパスワードが必要になります。

---
##### 简体中文
这是el.ideal-ideas为茉客系统开发的设定模块。
这个设定模块采用了JSON格式。
JSON文件内的所有设定信息会被保存到内存里，您可以通过MocaConfig类来获取各种设定信息。
MocaConfig类会每1（初期值）秒重新读取一次JSON文件（如果有变更）。
如果JSON文件被改写，内存内的设定信息也会和JSON文件同步。
如果设定文件包含`"__private__": True,`该设定文件则为隐私文件。
如果设定key由`"_"`开始，该设定则为隐私设定。
访问隐私设定的时候，需要输入access-token或者root密码。

# Usage Example
###### Use in your application
```python
# Create a instance.
# インスタンス化。
# 创建实例。
moca_config = MocaConfig('test', './test/test.json')

# Try get language config. 
# If lang info is in the json file and it is string type,
# return the value, if not, return default value.
# 言語設定の取得を試みます。
# もしlang項目がJSONファイルにありかつ文字列形式である場合。その値を返します。
# 他の場合はデフォルト値を返します。
# 尝试获取语言设定。
# 如果JSON文件里面有名为lang的数据，并且是文字列格式的话，返回其值。
# 其他情况返回初始值。
moca_config.get('lang', str, default='english')

# If set any type to the argument. MocaConfig will return the config value without type check.
# 第２引数をanyとして設定した場合、MocaConfigは返り値の型をチェックしません。
# 如果第2个参数的值是any的话，MocaConfig不会对返回值进行类型检测。
moca_config.get('lang', any, default='english')

# If set auto_convert=True, MocaConfig will try convert the config value when the type of config value is incorrect
# auto_convert=Trueが設定されている場合は設定データの形式が異なるとき、返り値の自動型変換を試みます。
# 如果您设定了auto_convert=True，返回值的类型错误时，MocaConfig会对返回值尝试进行类型转换。
moca_config.get('lang', str, default='english', auto_convert=True)

# Set a config value, and update the json file.
# 設定情報を追加してJSONファイルを更新します。
# 添加设定信息并且更新JSON文件
moca_config.set('lang', 'english')

# Check the config value, if lang config is 'english', return True. 
# 設定のチェック、もしlang設定がenglishの文字列である場合はTrueを返す。
# 对比设定，如果lang设定的值是english则返回True。
moca_config.check('lang', str, 'english')
```

```python
# The __init__ method in MocaConfig class.
# MocaConfigクラスのイニシャライザー。
# MocaConfig类的生成器。
def __init__(self,
             name: str,
             filepath: Union[Path, str],
             filename: str = '',
             reload_interval: float = 5.0,
             access_token: str = '',
             **kwargs):
    """
    The initializer of MocaConfig class.
    :param name: the name of this instance
    :param filepath: the path of json config file.
    :param filename: the name of json config file.
    :param reload_interval: the interval to reload config file. if the value is -1, never reload config file
    :param access_token: the access token of config file.

    Raise
    -----
        TypeError: if the arguments type is incorrect.
        MocaFileError: if can't find, open or create config file.
    """
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

###### Main Class Methods

- def set_root_pass(password: str) -> bool:
    - Set the root password, only can run once.
    - rootパスワードを設定します、一度しか実行できません。
    - 设定root密码，仅可以执行一次。
    
- def change_root_pass(new_password: str, old_password: str) -> bool:
    - Change root password.
    - rootパスワードを変更します。
    - 更改root密码。

- def get_instance_list() -> List[str]:
    - Get all name of instance as a list.
    - すべてのインストールの名前をリストとして取得します。
    - 以列表的格式获取所有实例名。
    
- def get_instance(name: str) -> Any:
    - Get the created instance by name.
    - 名前によって生成済みのインスタンスを取得します。
    - 通过名字获取已生成的实例。

###### Main Instance Methods

- def change_reload_interval(interval: float) -> None:
    - Change the interval to reload config file.
    - 設定ファイルの再読み込み間隔を変更します。
    - 更改设定文件的重新读取的间隔。
    
- def stop_auto_reload(self) -> None:
    - Stop auto reload config file.
    - 設定ファイルの自動再読み込みを停止します。
    - 停止设定文件的自动重读。
    
- def change_config_file_path(path: Union[Path, str]) -> Path:
    - Change the config file path.
    - 設定ファイルのパスを変更します。
    - 更改设定文件的地址。
    
- def reload_config() -> None:
    - Reload json config file manually.
    - JSON設定ファイルを手動で再読み込みします。
    - 手动重读JSON设定文件。

- def get_config_size() -> int:
    - Return the size of the config directory.
    - 設定情報の数を返す。
    - 返回设定信息的数量。
    
- def get_all_config(access_token: str = '', root_pass: str = '') -> Optional[dict]:
    - Return all configs as a dictionary
    - すべての設定情報を一つの辞書として返します。
    - 以字典格式返回所有的设定信息。
    
def get_all_config_key(access_token: str = '', root_pass: str = '') -> Optional[Tuple]:
    - Return all config keys
    - すべての設定の項目名を返す。
    - 返回所有设定的名称。
    
- def get(key: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False, save_unknown_config: bool = True, access_token: str = '', root_pass: str = '') -> Any:
    - Return the value of config.
    - 設定の値を返す。
    - 返回设定的值。
```python
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
```
    
- def set(key: str, value: Any, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Set a value of config.
    - 値を設定項目に設定します。
    - 添加一个设定值。
```python
    def set(self,
            key: str,
            value: Any,
            access_token: str = '',
            root_pass: str = '') -> Optional[bool]:
        """
        set a config value.
        if the key already exists, overwrite it.
        :param key: the config name.
        :param value: the config value.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [success] or [failed], If can't access to the config file return None
        """
```

def remove_config(key: str, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Remove the config.
    - 設定を作成します。
    - 删除设定文件。
    
- def check(key: str, res_type: Any, value: Any, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Check the value is same or not with config value.
    - 値が設定値と等しいかどうかをチェックします。
    - 检测参数值是否和设定值相同。
```python
    def check(self,
              key: str,
              res_type: Any,
              value: Any,
              access_token: str = '',
              root_pass: str = '') -> Optional[bool]:
        """
        check is value correct.
        :param key: the config name.
        :param res_type: the config value type.
        :param value: input value to check.
        :param access_token: the access token of config file.
        :param root_pass: the root password.
        :return: status, [correct] or [incorrect]. If can't access to this config file. return None.
        """
```

- def set_config_private() -> bool:
    - Make this config file private.
    - 設定ファイルにプライベート属性を設定します。
    - 给设定文件添加隐私属性。
    
- def set_config_public(access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Make this config file public.
    - 設定ファイルに公開属性を設定します。
    - 给设定文件添加公开属性。
    
- def is_private() -> bool:
    - Check is the config private.
    - 設定ファイルがプライベートかどうかをチェックします。
    - 检测设定文件是否是隐私文件。
    
- def set_access_token(root_pass: str, token: str = '') -> Optional[bool]:
    - Set a access token to config file.
    - 設定ファイルにアクセストークンを追加します。
    - 向设定文件添加access-token
    
- def check_access_token(root_pass: str, token: str) -> Optional[bool]:
    - Check is access token correct.
    - アクセストークンをチェックします。
    - 检测access-token是否正确。
    
- def delete_this_config_file(access_token: str = '', root_pass: str = '') -> bool:
    - Delete config file.
    - 設定ファイルを削除します。
    - 删除设定文件。
    
- def set_and_encrypt(key: str, value: Any, encrypt_pass: str, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Similar to the set method, but this method encrypt the data in config file.
    - set メソッドとほぼ同じ機能だが、設定ファイルないのデータを暗号化します。
    - 和set方法几乎相同，但是会对设定文件内部的数据加密。
    
- def get_encrypted_config(key: str, encrypt_pass: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False, save_unknown_config: bool = True, access_token: str = '', root_pass: str = '') -> Any:
    - Similar to the get method, but this method can get encrypted config.
    - get メソッドとほぼ同じ機能だが、暗号化された設定も取得可能。
    - 和get方法几乎相同，但是可以读取被加密的数据。
    
- def add_handler(name: str, handler: Callable, args: Tuple, kwargs: Dict, keys: Union[List[str], str]) -> None:
    - Add a handler to run some action when the config was changed.
    - 設定が変更されたときに呼び出されるハンドラーを設定できます。
    - 可以添加一个在设定信息被更改是调用的函数。
    
def remove_handler(name: str) -> None:
    - Remove the registered handler.
    - 追加済みハンドラーを削除します。
    - 删掉已添加的更改检测函数。
    
- def get_handler(name: str) -> Optional[Callable]:
    - Get the registered handler.
    - 追加済みハンドラーを取得します。
    - 获取已添加的更改检测函数。

###### Optional Methods
    
- def random_string(length: int) -> str:
    - Return random string with length argument.
    - 指定した長さのランダムな文字列を返す。
    - 返回指定长度的随机文字列。
    
- def random_integers(length: int) -> str:
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