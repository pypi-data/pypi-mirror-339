from typing import Dict, Any, List, Optional, Union
from . import global_variable as glv

class Store:
    """
    全局存储类，用于管理应用程序的全局变量。
    
    提供设置、获取、删除全局变量的方法，以及字典操作。
    """
    
    def __init__(self, dict: Optional[Dict[str, Any]] = None) -> None:
        """
        初始化Store实例。
        
        Args:
            dict: 可选的初始字典，用于初始化全局变量
        """
        if dict is not None:
            glv._init()
            glv.GLOBALS_DICT = dict

    def set(self, key: Union[str, Dict[str, Any]], value: Any = None) -> None:
        """
        设置全局变量的值。
        
        Args:
            key: 字符串键或字典对象
            value: 当key为字符串时的值，当key为字典时忽略此参数
            
        Raises:
            TypeError: 当key既不是字符串也不是字典时
        """
        if isinstance(key, str):
            glv.set(key, value)
        elif isinstance(key, dict):
            for each_key in key:
                glv.set(each_key, key[each_key])
        else:
            raise TypeError("key must be str or dict")
        
    def setDict(self, setDict: Dict[str, Any]) -> None:
        """
        设置整个全局字典。
        
        Args:
            setDict: 要设置的字典
            
        Raises:
            TypeError: 当setDict不是字典类型时
        """
        if not isinstance(setDict, dict):
            raise TypeError("setDict must be a dictionary")
        glv.GLOBALS_DICT = setDict.copy()  # 使用副本避免外部修改
      
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取全局变量的值。
        
        Args:
            key: 要获取的键
            default: 当键不存在时返回的默认值
            
        Returns:
            键对应的值，如果键不存在则返回默认值
        """
        return glv.get(key, default)
    
    def has(self, key: str) -> bool:
        """
        检查全局变量中是否存在指定的键。
        
        Args:
            key: 要检查的键
            
        Returns:
            如果键存在返回True，否则返回False
        """
        return key in glv.GLOBALS_DICT
    
    def getDict(self) -> Dict[str, Any]:
        """
        获取整个全局字典的副本。
        
        Returns:
            全局字典的副本
        """
        return glv.GLOBALS_DICT.copy()  # 返回副本避免外部修改
    
    def print(self, key: str) -> None:
        """
        打印指定键的值。
        
        Args:
            key: 要打印的键
        """
        glv.printParam(key)
    
    def keys(self) -> List[str]:
        """
        获取所有全局变量的键。
        
        Returns:
            键的列表
        """
        return list(glv.GLOBALS_DICT.keys())
    
    def values(self) -> List[Any]:
        """
        获取所有全局变量的值。
        
        Returns:
            值的列表
        """
        return list(glv.GLOBALS_DICT.values())
    
    def remove(self, key: Optional[str] = None) -> None:
        """
        移除指定的全局变量或所有全局变量。
        
        Args:
            key: 要移除的键，如果为None则移除所有变量
        """
        if key is None:
            glv.GLOBALS_DICT = {}
        elif key in glv.GLOBALS_DICT:
            del glv.GLOBALS_DICT[key]
        # 如果键不存在，静默忽略