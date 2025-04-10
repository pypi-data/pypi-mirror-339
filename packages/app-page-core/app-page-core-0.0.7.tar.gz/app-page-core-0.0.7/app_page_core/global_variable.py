#!/usr/bin/env python3
# -*- coding:utf-8-*-
# 全局变量管理模块global_variable

from typing import Any, Dict, Optional, Union

# 初始化全局变量
IS_INIT: bool = False
GLOBALS_DICT: Dict[str, Any] = {}

def _init() -> None:
    """初始化全局变量。
    
    在主模块中调用此函数来初始化全局变量。
    """
    global IS_INIT, GLOBALS_DICT
    IS_INIT = False
    GLOBALS_DICT = {}

def set(key: str, value: Any) -> bool:
    """设置全局变量的值。
    
    Args:
        key: 全局变量的键名
        value: 要设置的值
        
    Returns:
        bool: 设置成功返回True，失败返回False
    """
    try:
        GLOBALS_DICT[key] = value
        return True
    except Exception:
        return False

def get(key: str, default: Any = None) -> Any:
    """获取全局变量的值。
    
    Args:
        key: 全局变量的键名
        default: 当键不存在时返回的默认值
        
    Returns:
        Any: 全局变量的值，如果键不存在则返回默认值
    """
    return GLOBALS_DICT.get(key, default)

def printParam(key: Optional[str] = None) -> None:
    """打印全局变量的值。
    
    Args:
        key: 要打印的全局变量的键名，如果为None则打印所有全局变量
    """
    if key is None:
        import json
        print('GLOBALS_DICT:', json.dumps(GLOBALS_DICT, indent=2, ensure_ascii=False))
        return
    
    if key in GLOBALS_DICT:
        print(f"{key}: {GLOBALS_DICT[key]}")
    else:
        print('Not Found')

def getDict() -> Dict[str, Any]:
    """获取全局变量字典。
    
    Returns:
        Dict[str, Any]: 全局变量字典
    """
    return GLOBALS_DICT