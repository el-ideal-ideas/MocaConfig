# MocaConfig --- JSONベースの設定管理モジュール。

これはモカシステムのためにel.ideal-ideasによって開発された設定モジュールである。
この設定モジュールはJSON形式を採用しています。
JSONファイル内のすべての設定情報はメモリ内にロードされ、そしてMocaConfigクラスを経由して取得できます。
MocaConfigクラスはデフォルト設定では1秒ごとJSONファイルをリロードします(変更があった場合)。
JSONファイルに変更があった場合、その変更はメモリ内の設定情報にも反映されます。
設定ファイルが`"__private__": True,`を含む場合、その設定ファイルはプライベートな設定ファイルになります。
`"_"`から始まる設定内容も同様にプライベートになります。
プライベートな設定情報にアクセスする場合、アクセストークンまたはrootパスワードが必要になります。

#### life is short - you need Python!

# ドキュメント
- [English Document](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README.md)
- [日本語ドキュメント](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README_JA.md)
- [简体中文文档](https://github.com/el-ideal-ideas/MocaConfig/blob/master/README_ZH.md)

### システム要件
- Python >= 3.7
- pycryptodome

### インストール
```
pip3 install moca_config
```

# Usage Example
```python
# インスタンス化。
moca_config = MocaConfig('test', './test/test.json')

# 言語設定の取得を試みます。
# もしlang項目がJSONファイルにありかつ文字列形式である場合。その値を返します。
# 他の場合はデフォルト値を返します。
moca_config.get('lang', str, default='english')

# 第２引数をanyとして設定した場合、MocaConfigは返り値の型をチェックしません。
moca_config.get('lang', any, default='english')

# auto_convert=Trueが設定されている場合は設定データの形式が異なるとき、返り値の自動型変換を試みます。
moca_config.get('lang', str, default='english', auto_convert=True)

# 設定情報を追加してJSONファイルを更新します。
moca_config.set('lang', 'english')
 
# 設定のチェック、もしlang設定がenglishの文字列である場合はTrueを返す。
moca_config.check('lang', str, 'english')
```

#### 特殊な値
###### 下記の数値はそれぞれ特殊な意味を持っています。

```python3
NOW: str = '[el]#moca_now#'  # 現在時間
NOW_DATE: str = '[el]#moca_now_date#'  # 現在の日付
RANDOM_STRING: str = '[el]#moca_random_string<length>#'  # ランダムな文字列
RANDOM_INTEGER: str = '[el]#moca_random_integer#'  # ランダムな数値
RANDOM_INTEGER_LIST: str = '[el]#moca_random_integer_list<length>#'  # ランダムな数値のリスト
RANDOM_INTEGERS: str = '[el]#moca_random_integers<length>#'  # ランダムな数値から作られた文字列
UUID1: str = '[el]#moca_uuid1#'  # uuid1
UUID1_HEX: str = '[el]#moca_uuid1_hex#'  # uuid1 hex
UUID4: str = '[el]#moca_uuid4#'  # uuid4
UUID4_HEX: str = '[el]#moca_uuid4_hex#'  # uuid4 hex
PROCESS_ID: str = '[el]#moca_process_id#'  # プロセスID
PROCESS_NAME: str = '[el]#moca_process_name#'  # プロセス名
CPU_COUNT: str = '[el]#moca_cpu_count#'  # CPUの数
GET_ALL_CONFIG: str = '[el]#moca_get_all_config#'  # すべての設定
```

###### 使用例

```python3
moca_config = MocaConfig('example', './example.json')
print(moca_config.get('[el]#moca_now#'))
print(moca_config.get(MocaConfig.NOW))
# 出力
# 2020-01-17 13:23:59.486562
# 2020-01-17 13:23:59.486562
```

#### パブリックメソッド

###### 主なクラスメソッド

- def set_root_pass(password: str) -> bool:
    - rootパスワードを設定します、一度しか実行できません。
    
- def change_root_pass(new_password: str, old_password: str) -> bool:
    - rootパスワードを変更します。

- def get_instance_list() -> List[str]:
    - すべてのインストールの名前をリストとして取得します。    
    
- def get_instance(name: str) -> Any:
    - 名前によって生成済みのインスタンスを取得します。

###### 主なインスタンスメソッド

- def change_reload_interval(interval: float) -> None:
    - 設定ファイルの再読み込み間隔を変更します。
    
- def stop_auto_reload(self) -> None:
    - 設定ファイルの自動再読み込みを停止します。
    
- def change_config_file_path(path: Union[Path, str]) -> Path:
    - 設定ファイルのパスを変更します。
    
- def reload_config() -> None:
    - JSON設定ファイルを手動で再読み込みします。    

- def get_config_size() -> int:
    - 設定情報の数を返す。
    
- def get_all_config(access_token: str = '', root_pass: str = '') -> Optional[dict]:
    - すべての設定情報を一つの辞書として返します。    
    
def get_all_config_key(access_token: str = '', root_pass: str = '') -> Optional[Tuple]:    
    - すべての設定の項目名を返す。    
    
- def get(key: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False, save_unknown_config: bool = True, access_token: str = '', root_pass: str = '') -> Any:
    - 設定の値を返す。
    
- def set(key: str, value: Any, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - 値を設定項目に設定します。

def remove_config(key: str, access_token: str = '', root_pass: str = '') -> Optional[bool]:    
    - 設定を作成します。    
    
- def check(key: str, res_type: Any, value: Any, access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - 値が設定値と等しいかどうかをチェックします。

- def set_config_private() -> bool:
    - 設定ファイルにプライベート属性を設定します。
    
- def set_config_public(access_token: str = '', root_pass: str = '') -> Optional[bool]:
    - 設定ファイルに公開属性を設定します。
    
- def is_private() -> bool:   
    - 設定ファイルがプライベートかどうかをチェックします。
    
- def set_access_token(root_pass: str, token: str = '') -> Optional[bool]:
    - 設定ファイルにアクセストークンを追加します。
    
- def check_access_token(root_pass: str, token: str) -> Optional[bool]:    
    - アクセストークンをチェックします。
    
- def delete_this_config_file(access_token: str = '', root_pass: str = '') -> bool:
    - 設定ファイルを削除します。
    
- def set_and_encrypt(key: str, value: Any, encrypt_pass: str, access_token: str = '', root_pass: str = '') -> Optional[bool]:    
    - set メソッドとほぼ同じ機能だが、設定ファイルないのデータを暗号化します。
    
- def get_encrypted_config(key: str, encrypt_pass: str, res_type: Any = any, default: Any = None, auto_convert: bool = False, allow_el_command: bool = False, save_unknown_config: bool = True, access_token: str = '', root_pass: str = '') -> Any:
    - get メソッドとほぼ同じ機能だが、暗号化された設定も取得可能。    
    
- def add_handler(name: str, handler: Callable, args: Tuple, kwargs: Dict, keys: Union[List[str], str]) -> None:
    - 設定が変更されたときに呼び出されるハンドラーを設定できます。
    
def remove_handler(name: str) -> None:
    - 追加済みハンドラーを削除します。    
    
- def get_handler(name: str) -> Optional[Callable]:    
    - 追加済みハンドラーを取得します。

###### その他のメソッド
    
- def random_string(length: int) -> str:
    - 指定した長さのランダムな文字列を返す。    
    
- def random_integers(length: int) -> str:
    - 指定した長さのランダムな数字によって構成された文字列を返す。
    
- def random_integer_list(length: int) -> List[int]:
    - 指定した長さのランダムな数値によって構成されたリストを返す。
    
- def el_command_parser(command: str) -> Tuple[bool, Any]:
    - 特殊キーワードの解析用メソッド。
    
# ライセンス (MIT)
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
    
# 追加情報
- el.ideal-ideas
    - https://www.el-ideal-ideas.com