"""
Result.py - 搜索结果类

定义了算法执行结果的数据结构
"""

from typing import Set, Dict, Any, Optional

class Result:
    """
    搜索结果类，用于存储算法执行的结果
    """
    def __init__(self, best_solution: Optional[Set[int]] = None, 
                best_obj_value: float = float('inf'),
                iterations: int = 0,
                runtime: float = 0.0):
        """
        初始化结果对象
        
        参数:
            best_solution: 最优解的节点集合
            best_obj_value: 最优解的目标值
            iterations: 算法执行的迭代次数
            runtime: 算法执行的运行时间(秒)
        """
        self.best_solution = best_solution if best_solution is not None else set()
        self.best_obj_value = best_obj_value
        self.iterations = iterations
        self.runtime = runtime
    
    def __str__(self) -> str:
        """
        返回结果的字符串表示
        
        返回:
            简洁的结果字符串，包含目标值、运行时间和迭代次数
        """
        return (f"Result(best_obj_value={self.best_obj_value}, "
                f"runtime={self.runtime:.2f}s, iterations={self.iterations})")
    
    def __repr__(self) -> str:
        """
        返回结果的详细表示
        
        返回:
            详细的结果字符串，包含最优解、目标值、迭代次数和运行时间
        """
        return (f"Result(best_solution={self.best_solution}, "
                f"best_obj_value={self.best_obj_value}, "
                f"iterations={self.iterations}, runtime={self.runtime})")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        将结果转换为字典形式
        
        返回:
            包含结果数据的字典
        """
        return {
            "best_solution": self.best_solution,
            "best_obj_value": self.best_obj_value,
            "iterations": self.iterations,
            "runtime": self.runtime
        } 