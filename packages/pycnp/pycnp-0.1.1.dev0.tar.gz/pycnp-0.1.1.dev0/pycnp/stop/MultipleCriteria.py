"""
MultipleCriteria.py - 多准则停止条件

提供同时使用多个停止准则的组合控制功能
"""

from typing import List, Sequence
from .StoppingCriterion import StoppingCriterion


class MultipleCriteria:
    """
    多准则停止条件
    
    将多个停止准则组合在一起，当任意一个准则满足时触发停止
    """

    def __init__(self, criteria: Sequence[StoppingCriterion]) -> None:
        """
        初始化多准则停止条件
        
        参数:
            criteria: 停止准则列表
            
        异常:
            ValueError: 当准则列表为空时抛出
        """
        if len(criteria) == 0:
            raise ValueError("至少需要一个停止准则")

        self.criteria = list(criteria)

    def __call__(self, best_cost: float) -> bool:
        """
        判断是否满足任一停止准则
        
        参数:
            best_cost: 当前最优解的成本值
            
        返回:
            如果任何一个准则返回True则返回True，否则返回False
        """
        return any(crit(best_cost) for crit in self.criteria)
    
    def add_criterion(self, criterion: StoppingCriterion) -> None:
        """
        添加新的停止准则
        
        参数:
            criterion: 要添加的停止准则
        """
        self.criteria.append(criterion)

    def get_name(self) -> str:
        """
        获取准则名称
        
        返回:
            准则名称以及包含的子准则数量
        """
        names = [crit.get_name() for crit in self.criteria]
        return f"Multiple({', '.join(names)})"
