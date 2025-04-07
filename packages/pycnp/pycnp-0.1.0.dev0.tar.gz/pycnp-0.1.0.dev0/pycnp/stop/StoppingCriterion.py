"""
StoppingCriterion.py - 停止准则协议定义

定义了停止准则必须实现的接口协议，所有具体的停止准则类都应符合该协议
"""

from typing import Protocol


class StoppingCriterion(Protocol):  # pragma: no cover
    """
    停止准则协议
    
    定义了所有停止准则类必须实现的接口方法
    """

    def __call__(self, best_cost: float) -> bool:
        """
        调用停止准则判断是否应该停止算法
        
        当被调用时，如果返回True则表示算法应该停止，否则继续运行
        
        参数:
            best_cost: 当前最优解的成本值
            
        返回:
            True表示算法应该停止，False表示继续运行
        """

    def get_name(self) -> str:
        """
        获取停止准则的名称
        
        返回:
            停止准则的名称字符串
        """
        return self.__class__.__name__
