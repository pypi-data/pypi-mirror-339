"""
stop - 算法停止准则模块

提供了各种用于控制优化算法停止条件的准则类实现
"""

from .StoppingCriterion import StoppingCriterion
from .MaxIterations import MaxIterations
from .MaxRuntime import MaxRuntime
from .NoImprovement import NoImprovement
from .MultipleCriteria import MultipleCriteria

__all__ = [
    'StoppingCriterion',
    'MaxIterations',
    'MaxRuntime',
    'NoImprovement',
    'MultipleCriteria',
]
