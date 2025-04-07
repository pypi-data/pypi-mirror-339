"""
MaxRuntime.py - 最大运行时间停止准则

提供基于最大运行时间的算法停止控制
"""

import time
from typing import Optional
from .StoppingCriterion import StoppingCriterion


class MaxRuntime:
    """
    最大运行时间停止准则
    
    当算法运行时间超过指定的最大时间(秒)时触发停止
    """

    def __init__(self, max_runtime: float):
        """
        初始化最大运行时间停止准则
        
        参数:
            max_runtime: 最大允许的运行时间(秒)
            
        异常:
            ValueError: 当max_runtime小于0时抛出
        """
        if max_runtime < 0:
            raise ValueError("最大运行时间不能小于0")

        self._max_runtime = max_runtime
        self._start_runtime: Optional[float] = None

    def __call__(self, best_cost: float) -> bool:
        """
        判断是否达到最大运行时间
        
        参数:
            best_cost: 当前最优解的成本值(本准则不使用此参数)
            
        返回:
            如果当前运行时间超过最大运行时间则返回True，否则返回False
        """
        if self._start_runtime is None:
            # 初次调用时，记录当前时间
            self._start_runtime = time.perf_counter()

        return time.perf_counter() - self._start_runtime > self._max_runtime
    
    def reset(self) -> None:
        """
        重置计时器
        """
        self._start_runtime = None

    def get_name(self) -> str:
        """
        获取准则名称
        
        返回:
            准则名称
        """
        return "TimeLimit"

