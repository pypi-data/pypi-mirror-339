import os
import json
import logging
from typing import Any, Dict, List, Optional, Union

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LocalStore:
    """
    本地 JSON 文件存储类，提供简单的键值对存储功能。
    
    支持以下操作：
    - 读取和写入 JSON 文件
    - 获取、设置和删除键值对
    - 批量更新数据
    """
    
    def __init__(self, path: str = 'app.json') -> None:
        """
        初始化 LocalStore 实例。
        
        Args:
            path: JSON 文件的路径，默认为 'app.json'
        """
        self.json_path = path
        self._cache: Optional[Dict[str, Any]] = None
        self._cache_dirty = False
    
    def _load_json(self) -> Dict[str, Any]:
        """
        从文件加载 JSON 数据。
        
        Returns:
            包含 JSON 数据的字典，如果文件不存在或解析失败则返回空字典
        """
        if self._cache is not None and not self._cache_dirty:
            return self._cache
            
        if not os.path.exists(self.json_path):
            self._cache = {}
            return self._cache
            
        try:
            with open(self.json_path, 'r', encoding="utf-8") as json_file:
                self._cache = json.load(json_file)
                return self._cache
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析错误: {e}")
            self._cache = {}
            return self._cache
        except IOError as e:
            logger.error(f"读取文件错误: {e}")
            self._cache = {}
            return self._cache

    def _save_json(self, data: Dict[str, Any]) -> bool:
        """
        将数据保存到 JSON 文件。
        
        Args:
            data: 要保存的数据字典
            
        Returns:
            保存成功返回 True，否则返回 False
        """
        try:
            dir_path = os.path.dirname(self.json_path)
            if dir_path and not os.path.exists(dir_path):
                os.makedirs(dir_path)
                
            with open(self.json_path, 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                
            self._cache = data
            self._cache_dirty = False
            return True
        except IOError as e:
            logger.error(f"保存数据错误: {e}")
            return False

    def getAll(self) -> Dict[str, Any]:
        """
        获取所有存储的数据。
        
        Returns:
            包含所有数据的字典
        """
        return self._load_json()

    def get(self, key: Optional[str] = None) -> Any:
        """
        获取指定键的值，如果键不存在则返回 None。
        
        Args:
            key: 要获取的键，如果为 None 则返回所有数据
            
        Returns:
            键对应的值，如果键不存在则返回 None
        """
        data = self._load_json()
        if key is None:
            return data
        return data.get(key, None)

    def delete(self, key: str) -> bool:
        """
        删除指定键的数据。
        
        Args:
            key: 要删除的键
            
        Returns:
            删除成功返回 True，否则返回 False
        """
        data = self._load_json()
        if key in data:
            data.pop(key)
            self._cache_dirty = True
            return self._save_json(data)
        else:
            logger.warning(f"未找到键: {key}")
            return False

    def save(self, key: Union[str, Dict[str, Any], List[Any]], value: Any = None) -> bool:
        """
        保存数据。
        
        Args:
            key: 如果是字符串，则为要保存的键；如果是字典，则批量更新；如果是列表，则替换整个数据
            value: 当 key 为字符串时，要保存的值
            
        Returns:
            保存成功返回 True，否则返回 False
        """
        data = self._load_json()
        
        if isinstance(key, str):
            data[key] = value
        elif isinstance(key, dict):
            data.update(key)
        elif isinstance(key, list):
            data = key
        
        self._cache_dirty = True
        return self._save_json(data)
        
    def clear(self) -> bool:
        """
        清空所有数据。
        
        Returns:
            清空成功返回 True，否则返回 False
        """
        self._cache = {}
        self._cache_dirty = True
        return self._save_json({})
        
    def exists(self, key: str) -> bool:
        """
        检查键是否存在。
        
        Args:
            key: 要检查的键
            
        Returns:
            键存在返回 True，否则返回 False
        """
        data = self._load_json()
        return key in data