# MocaConfig --- 基于JSON的设定管理模块。

这是el.ideal-ideas为茉客系统开发的设定模块。
这个设定模块采用了JSON格式。
JSON文件内的所有设定信息会被保存到内存里，您可以通过MocaConfig类来获取各种设定信息。
MocaConfig类会每1（初期值）秒重新读取一次JSON文件（如果有变更）。
如果JSON文件被改写，内存内的设定信息也会和JSON文件同步。
如果设定文件包含`"__private__": True,`该设定文件则为隐私文件。
如果设定key由`"_"`开始，该设定则为隐私设定。
访问隐私设定的时候，需要输入access-token或者root密码。

#### life is short - you need Python!

# 文档
- [English Document](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README.md)
- [日本語ドキュメント](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README_JA.md)
- [简体中文文档](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README_ZH.md)

### 依赖
- Python >= 3.7
- pycryptodome

### 安装
```
pip3 install moca_config
```

# Usage Example
```python
# 创建实例。
moca_config = MocaConfig('test', './test/test.json')

# 尝试获取语言设定。
# 如果JSON文件里面有名为lang的数据，并且是文字列格式的话，返回其值。
# 其他情况返回初始值。
moca_config.get('lang', str, default='english')

# 如果第2个参数的值是any的话，MocaConfig不会对返回值进行类型检测。
moca_config.get('lang', any, default='english')

# 如果您设定了auto_convert=True，返回值的类型错误时，MocaConfig会对返回值尝试进行类型转换。
moca_config.get('lang', str, default='english', auto_convert=True)

# 添加设定信息并且更新JSON文件
moca_config.set('lang', 'english')

# 对比设定，如果lang设定的值是english则返回True。
moca_config.check('lang', str, 'english')
```

#### 特殊值
###### 下面的这些值，有一些特殊的作用。

```python3
NOW: str = '[el]#moca_now#'  # 当前时间
NOW_DATE: str = '[el]#moca_now_date#'  # 当前日期
RANDOM_STRING: str = '[el]#moca_random_string<length>#'  # 随机字符串
RANDOM_INTEGER: str = '[el]#moca_random_integer#'  # 随机的数值
RANDOM_INTEGER_LIST: str = '[el]#moca_random_integer_list<length>#'  # 随机的数组
RANDOM_INTEGERS: str = '[el]#moca_random_integers<length>#'  # 由随机的数字组成的字符串
UUID1: str = '[el]#moca_uuid1#'  # uuid1
UUID1_HEX: str = '[el]#moca_uuid1_hex#'  # uuid1 hex
UUID4: str = '[el]#moca_uuid4#'  # uuid4
UUID4_HEX: str = '[el]#moca_uuid4_hex#'  # uuid4 hex
PROCESS_ID: str = '[el]#moca_process_id#'  # 进程ID
PROCESS_NAME: str = '[el]#moca_process_name#'  # 进程名
CPU_COUNT: str = '[el]#moca_cpu_count#'  # CPU数
GET_ALL_CONFIG: str = '[el]#moca_get_all_config#'  # 获取全部设定
```

###### 例子

```python3
moca_config = MocaConfig('example', './example.json')
print(moca_config.get('[el]#moca_now#'))
print(moca_config.get(MocaConfig.NOW))
# 输出
# 2020-01-17 13:23:59.486562
# 2020-01-17 13:23:59.486562
```

#### 公开方法

###### 主要的类方法

- def set_root_pass(password: str) -> bool:
    - 设定root密码，仅可以执行一次。
    
- def change_root_pass(new_password: str, old_password: str) -> bool:
    - 更改root密码。

- def get_instance_list() -> List[str]:
    - 以列表的格式获取所有实例名。
    
- def get_instance(name: str) -> Any:
    - 通过名字获取已生成的实例。

###### 主要的实例方法

- def change_reload_interval(interval: float) -> None:
    - 更改设定文件的重新读取的间隔。
    
- def stop_auto_reload(self) -> None:
    - 停止设定文件的自动重读。
    
- def change_config_file_path(path: Union[Path, str]) -> Path:
    - 更改设定文件的地址。
    
- def reload_config() -> None:
    - 手动重读JSON设定文件。

- def get_config_size() -> int:
    - 返回设定信息的数量。
    
- def get_all_config(access_token: str = '', root_pass: str = '') -> Optional[dict]:
    - 以字典格式返回所有的设定信息。
    
def get_all_config_key(access_token: str = '', root_pass: str = '') -> Optional[Tuple]:
    - 返回所有设定的名称。
    
- def get(key: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False, save_unknown_config: bool = True, access_token: str = '', root_pass: str = '') -> Any:
    - 返回设定的值。
    
- def set(key: str, value: Any, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - 添加一个设定值。

def remove_config(key: str, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - 删除设定文件。
    
- def check(key: str, res_type: Any, value: Any, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - 检测参数值是否和设定值相同。

- def set_config_private() -> bool:   
    - 给设定文件添加隐私属性。
    
- def set_config_public(access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - 给设定文件添加公开属性。
    
- def is_private() -> bool:    
    - 检测设定文件是否是隐私文件。
    
- def set_access_token(root_pass: str, token: str = '') -> Optional[bool]:
    - 向设定文件添加access-token
    
- def check_access_token(root_pass: str, token: str) -> Optional[bool]:
    - 检测access-token是否正确。
    
- def delete_this_config_file(access_token: str = '', root_pass: str = '') -> bool:
    - 删除设定文件。
    
- def set_and_encrypt(key: str, value: Any, encrypt_pass: str, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - 和set方法几乎相同，但是会对设定文件内部的数据加密。
    
- def get_encrypted_config(key: str, encrypt_pass: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False, save_unknown_config: bool = True, access_token: str = '', root_pass: str = '') -> Any:
    - 和get方法几乎相同，但是可以读取被加密的数据。
    
- def add_handler(name: str, handler: Callable, args: Tuple, kwargs: Dict, keys: Union[List[str], str]) -> None:
    - 可以添加一个在设定信息被更改是调用的函数。
    
def remove_handler(name: str) -> None:
    - 删掉已添加的更改检测函数。
    
- def get_handler(name: str) -> Optional[Callable]:
    - 获取已添加的更改检测函数。

###### 其余的方法
    
- def random_string(length: int) -> str:
    - 返回指定长度的随机文字列。
    
- def random_integers(length: int) -> str:
    - 返回指定长度的由随机数字组成的文字列。
    
- def random_integer_list(length: int) -> List[int]:
    - 返回一个指定长度的由随机数字组成的数组。
    
- def el_command_parser(command: str) -> Tuple[bool, Any]:
    - 用于解析特殊值的方法。
    
    
# 使用许可 (MIT)
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
    
# 其他信息
- el.ideal-ideas
    - https://www.el-ideal-ideas.com