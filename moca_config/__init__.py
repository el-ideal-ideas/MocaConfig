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


from .MocaConfig import MocaConfig, MocaFileError, run_server, VERSION

__copyright__ = 'Copyright (C) 2020.1.17 <el.ideal-ideas: https://www.el-ideal-ideas.com>'
__version__ = VERSION
__license__ = 'MIT'
__author__ = 'el.ideal-ideas'
__author_email__ = 'el.idealideas@gmail.com'
__url__ = 'https://github.com/el-ideal-ideas/MocaConfig'

__all__ = ['MocaConfig', 'MocaFileError', 'run_server', 'VERSION']
