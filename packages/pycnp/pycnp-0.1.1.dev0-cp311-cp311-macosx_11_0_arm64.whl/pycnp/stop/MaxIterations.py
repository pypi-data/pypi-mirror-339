"""
MaxIterations.py - 最大迭代次数停止准则

提供基于最大迭代次数的算法停止控制
"""

from .StoppingCriterion import StoppingCriterion


class MaxIterations:
    """
    最大迭代次数停止准则
    
    当算法达到预设的最大迭代次数时触发停止
    """

    def __init__(self, max_iterations: int):
        """
        初始化最大迭代次数停止准则
        
        参数:
            max_iterations: 最大允许的迭代次数
            
        异常:
            ValueError: 当max_iterations小于0时抛出
        """
        if max_iterations < 0:
            raise ValueError("最大迭代次数不能小于0")

        self._max_iters = max_iterations
        self._curr_iter = 0

    def __call__(self, best_cost: float) -> bool:
        """
        判断是否达到最大迭代次数
        
        参数:
            best_cost: 当前最优解的成本值(本准则不使用此参数)
            
        返回:
            如果当前迭代次数超过最大迭代次数则返回True，否则返回False
        """
        self._curr_iter += 1
        return self._curr_iter >= self._max_iters

    def reset(self) -> None:
        """
        重置当前迭代计数器
        """
        self._curr_iter = 0

    def get_name(self) -> str:
        """
        获取准则名称
        
        返回:
            准则名称
        """
        return "MaxIterations"
