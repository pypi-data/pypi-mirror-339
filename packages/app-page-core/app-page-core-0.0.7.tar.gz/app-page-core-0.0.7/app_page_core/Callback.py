from collections import defaultdict
from typing import Any, Callable, List, Optional

class Callback:
    def __init__(self):
        """
        初始化回调管理对象
        """
        self.callback_dict = defaultdict(list)
        
    def has(self, name: str) -> bool:
        """
        检查是否存在指定名称的回调函数
        :param name: 回调函数名称
        :return: 如果存在返回True，否则返回False
        """
        return name in self.callback_dict

    def add(self, name: str, function: Callable) -> None:
        """
        添加回调函数
        :param name: 回调函数名称
        :param function: 要添加的回调函数
        """
        self.callback_dict[name].append(function)

    def get(self, name: str) -> List[Callable]:
        """
        获取指定名称的所有回调函数
        :param name: 回调函数名称
        :return: 回调函数列表，如果名称不存在则返回空列表
        """
        return self.callback_dict.get(name, [])

    def count(self, name: str) -> int:
        """
        获取指定名称的回调函数数量
        :param name: 回调函数名称
        :return: 回调函数数量
        """
        return len(self.callback_dict.get(name, []))

    def run(self, name: str, *args: Any) -> List[Any]:
        """
        运行指定名称的所有回调函数
        :param name: 回调函数名称
        :param args: 传递给回调函数的参数
        :return: 所有回调函数执行结果的列表
        """
        result = []
        for callback in self.get(name):
            if callback:
                result.append(callback(*args))
            else:
                result.append(None)
        return result

    def remove(self, name: Optional[str] = None, function: Optional[Callable] = None) -> None:
        """
        移除回调函数
        :param name: 回调函数名称，如果为None则移除所有回调函数
        :param function: 具体的回调函数，如果为None则移除该名称下的所有回调函数
        """
        if name is None:
            # 移除所有回调函数
            self.callback_dict.clear()
            return
            
        if name not in self.callback_dict:
            return
            
        if function is None:
            # 移除指定名称下的所有回调函数
            del self.callback_dict[name]
        else:
            # 移除指定的回调函数
            callbacks = self.callback_dict[name]
            if function in callbacks:
                callbacks.remove(function)
            # 如果该名称下没有回调函数了，则删除该名称
            if not callbacks:
                del self.callback_dict[name]

    def clear(self) -> None:
        """
        清除所有回调函数，与destroy方法功能相同
        """
        self.callback_dict.clear()
        
    def destroy(self) -> None:
        """
        销毁回调管理对象，清除所有回调函数
        """
        self.clear()