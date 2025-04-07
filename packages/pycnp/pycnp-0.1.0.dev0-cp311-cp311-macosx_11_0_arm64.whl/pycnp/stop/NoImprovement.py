"""
NoImprovement.py - 停滞准则实现

当算法在指定迭代次数内未能改进最优解时触发停止
"""

from typing import Optional
from .StoppingCriterion import StoppingCriterion


class NoImprovement:
    """
    解改进停滞准则
    
    当算法在指定的迭代次数内未能改进最优解时触发停止
    """

    def __init__(self, max_iterations: int):
        """
        初始化解改进停滞准则
        
        参数:
            max_iterations: 允许的最大未改进迭代次数
            
        异常:
            ValueError: 当max_iterations小于0时抛出
        """
        if max_iterations < 0:
            raise ValueError("最大未改进迭代次数不能小于0")

        self._max_iterations = max_iterations
        self._target: Optional[float] = None  # 首次调用时为None
        self._counter = 0

    def __call__(self, best_cost: float) -> bool:
        """
        判断是否达到停滞条件
        
        参数:
            best_cost: 当前最优解的成本值
            
        返回:
            如果连续未改进次数达到阈值则返回True，否则返回False
        """
        if self._target is None or best_cost < self._target:
            self._target = best_cost
            self._counter = 0
        else:
            self._counter += 1

        return self._counter >= self._max_iterations
        
    def reset(self) -> None:
        """
        重置准则状态
        """
        self._target = None
        self._counter = 0
        
    def get_name(self) -> str:
        """
        获取准则名称
        
        返回:
            准则名称
        """
        return "Stagnation"
