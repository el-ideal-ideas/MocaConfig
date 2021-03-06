# MocaConfig --- A json based config management module.

This is the config module developed by el.ideal-ideas for Moca System.
This config module is json based.
All config data in the json file, will be loaded into memory, and can be used from MocaConfig class.
MocaConfig class will reload the json file in 1(default value) seconds If it was changed.
If the json file was changed. the new config value will overwrite the old config value that in memory.
If the config file contains `"__private__": True,` the config file will be a private file.
If the config key is starts with `"_"` , the config will be a private config.
If you want to access the private config, you should input the access token or the root password.

#### life is short - you need Python!

# Documents
- [English Document](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README.md)
- [日本語ドキュメント](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README_JA.md)
- [简体中文文档](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README_ZH.md)

### System Requirements
- Python >= 3.7
- pycryptodome

### Installation
```
pip3 install moca_config
```

# Usage Example
```python
# Create a instance.
moca_config = MocaConfig('test', './test/test.json')

# Try get language config. 
# If lang info is in the json file and it is string type,
# return the value, if not, return default value.
moca_config.get('lang', str, default='english')

# If set any type to the argument. MocaConfig will return the config value without type check.
moca_config.get('lang', any, default='english')

# If set auto_convert=True, MocaConfig will try convert the config value when the type of config value is incorrect
moca_config.get('lang', str, default='english', auto_convert=True)

# Set a config value, and update the json file.
moca_config.set('lang', 'english')

# Check the config value, if lang config is 'english', return True. 
moca_config.check('lang', str, 'english')
```

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
    
- def change_root_pass(new_password: str, old_password: str) -> bool:
    - Change root password.    

- def get_instance_list() -> List[str]:
    - Get all name of instance as a list.
    
- def get_instance(name: str) -> Any:
    - Get the created instance by name.

###### Main Instance Methods

- def change_reload_interval(interval: float) -> None:
    - Change the interval to reload config file.
    
- def stop_auto_reload(self) -> None:
    - Stop auto reload config file.    
    
- def change_config_file_path(path: Union[Path, str]) -> Path:
    - Change the config file path.
    
- def reload_config() -> None:
    - Reload json config file manually.

- def get_config_size() -> int:
    - Return the size of the config directory.
    
- def get_all_config(access_token: str = '', root_pass: str = '') -> Optional[dict]:
    - Return all configs as a dictionary
    
def get_all_config_key(access_token: str = '', root_pass: str = '') -> Optional[Tuple]:
    - Return all config keys
    
- def get(key: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False, save_unknown_config: bool = True, access_token: str = '', root_pass: str = '') -> Any:
    - Return the value of config.
    
- def set(key: str, value: Any, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Set a value of config.

def remove_config(key: str, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Remove the config.
    
- def check(key: str, res_type: Any, value: Any, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Check the value is same or not with config value.

- def set_config_private() -> bool:
    - Make this config file private.
   
- def set_config_public(access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Make this config file public.
    
- def is_private() -> bool:
    - Check is the config private.
   
- def set_access_token(root_pass: str, token: str = '') -> Optional[bool]:
    - Set a access token to config file.
    
- def check_access_token(root_pass: str, token: str) -> Optional[bool]:
    - Check is access token correct.
    
- def delete_this_config_file(access_token: str = '', root_pass: str = '') -> bool:
    - Delete config file.
    
- def set_and_encrypt(key: str, value: Any, encrypt_pass: str, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - Similar to the set method, but this method encrypt the data in config file.
    
- def get_encrypted_config(key: str, encrypt_pass: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False, save_unknown_config: bool = True, access_token: str = '', root_pass: str = '') -> Any:
    - Similar to the get method, but this method can get encrypted config.
     
- def add_handler(name: str, handler: Callable, args: Tuple, kwargs: Dict, keys: Union[List[str], str]) -> None:
    - Add a handler to run some action when the config was changed.
   
def remove_handler(name: str) -> None:
    - Remove the registered handler.
     
- def get_handler(name: str) -> Optional[Callable]:
    - Get the registered handler.
    
###### Optional Methods
    
- def random_string(length: int) -> str:
    - Return random string with length argument.
    
- def random_integers(length: int) -> str:
    - Return random string that made up of integers with length argument.
     
- def random_integer_list(length: int) -> List[int]:
    - Return a list made up of random integers with length argument.
    
- def el_command_parser(command: str) -> Tuple[bool, Any]:
    - Parse the special constants.

# License (MIT)
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