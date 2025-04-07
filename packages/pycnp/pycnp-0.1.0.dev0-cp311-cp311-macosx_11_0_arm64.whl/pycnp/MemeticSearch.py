"""
MemeticSearch.py - 种群演化搜索算法实现

提供了基于种群演化搜索的图问题求解框架，支持多种问题类型和搜索策略
"""

import time
import random
from typing import Set, Optional, Tuple, List, Union, Dict, Any

# 导入Python版本的停止准则
from pycnp.stop import StoppingCriterion, MaxIterations, MaxRuntime, NoImprovement, MultipleCriteria
# 导入Result类
from pycnp.Result import Result
import PyCNP

# 问题类型和搜索策略的常量映射
PROBLEM_TYPES = {
    "CNP": PyCNP.CNP,
    "DCNP": PyCNP.DCNP,
    "NWCNP": PyCNP.NWCNP,
}

SEARCH_STRATEGIES = {
    "CBNS": PyCNP.CBNS,
    "CHNS": PyCNP.CHNS,
    "DLAS": PyCNP.DLAS,
    "BCLS": PyCNP.BCLS,
}

class MemeticSearchParams:
    """
    种群搜索参数类，用于配置MemeticSearch算法
    兼容C++版本的MemeticSearchParams接口
    """
    def __init__(self, **kwargs):
        """
        初始化种群搜索参数
        
        参数:
            **kwargs: 可选参数
                - initPopSize: 初始种群大小 (默认: 5)
                - MAXPOPULATIONSIZE: 最大种群大小 (默认: 20)
                - MAX_IDLE_STEPS: 最大允许空闲步数 (默认: 100)
                - IS_POP_VARIABLE: 种群大小是否可变 (默认: True)
                - INCREASE_POP_SIZE: 每次扩展增加的种群大小 (默认: 3)
                - search_strategy: 搜索策略 (默认: CHNS)
        """
        # 默认参数与C++侧保持一致
        self._params = {
            "initPopSize": 5,
            "MAXPOPULATIONSIZE": 20,
            "MAX_IDLE_STEPS": 100,
            "IS_POP_VARIABLE": True,
            "INCREASE_POP_SIZE": 3,
            "search_strategy": PyCNP.CHNS  # 默认使用CHNS策略
        }
        
        # 更新用户提供的参数
        for key, value in kwargs.items():
            if key == 'search_strategy' and isinstance(value, str):
                if value in SEARCH_STRATEGIES:
                    self._params[key] = SEARCH_STRATEGIES[value]
                else:
                    raise ValueError(f"不支持的搜索策略: {value}")
            else:
                self._params[key] = value
    
    def __getattr__(self, name: str) -> Any:
        """
        获取参数值
        
        参数:
            name: 参数名称
            
        返回:
            参数值
            
        异常:
            AttributeError: 当参数不存在时抛出
        """
        # 支持通过search_strategy和searchStrategy两种方式访问
        if name == "searchStrategy" and "search_strategy" in self._params:
            return self._params["search_strategy"]
        # 检查属性是否在内部参数字典中
        if name in self._params:
            return self._params[name]
        # 如果属性不存在，抛出AttributeError异常
        raise AttributeError(f"'MemeticSearchParams' object has no attribute '{name}'")
    
    def __setattr__(self, name: str, value: Any) -> None:
        """
        设置参数值
        
        参数:
            name: 参数名称
            value: 参数值
        """
        # 如果是设置_params属性本身，使用父类的__setattr__方法
        if name == '_params':
            super().__setattr__(name, value)
        # 支持通过searchStrategy设置search_strategy，兼容C++接口
        elif name == "searchStrategy":
            self._params["search_strategy"] = value
        # 其他情况，直接在参数字典中设置值
        else:
            self._params[name] = value
    
    def __repr__(self) -> str:
        """
        返回参数对象的字符串表示
        
        返回:
            格式化的参数字符串
        """
        # 根据search_strategy的值查找对应的策略名称
        strategy_name = next((name for name, value in SEARCH_STRATEGIES.items() 
                             if value == self._params["search_strategy"]), "未知")
        
        # 返回格式化的字符串，显示主要参数
        return (f"MemeticSearchParams(initPopSize={self._params['initPopSize']}, "
                f"MAXPOPULATIONSIZE={self._params['MAXPOPULATIONSIZE']}, "
                f"MAX_IDLE_STEPS={self._params['MAX_IDLE_STEPS']}, "
                f"search_strategy={strategy_name})")

def auto_convert(func):
    """
    装饰器：自动将字符串类型的问题类型转换为PyCNP常量
    
    参数:
        func: 要装饰的函数
        
    返回:
        装饰后的函数
    """
    def wrapper(self, *args, **kwargs):
        # 处理位置参数
        new_args = list(args)
        
        # 在MemeticSearch.__init__中，problem_type是第2个参数(索引为1)
        if len(args) > 1:
            # 转换problem_type
            new_args[1] = MemeticSearch._convert_problem_type(args[1])
        
        # 处理关键字参数
        new_kwargs = kwargs.copy()
        if 'problem_type' in kwargs:
            new_kwargs['problem_type'] = MemeticSearch._convert_problem_type(kwargs['problem_type'])
            
        return func(self, *new_args, **new_kwargs)
    return wrapper

class MemeticSearch:
    """
    多种群搜索算法实现
    
    结合了种群管理、交叉操作和局部搜索的进化算法框架，用于解决CNP/DCNP/NWCNP问题
    """
    
    @staticmethod
    def _convert_problem_type(problem_type: Union[str, int]) -> int:
        """
        将问题类型转换为PyCNP常量
        
        参数:
            problem_type: 问题类型，可以是字符串或PyCNP常量
            
        返回:
            PyCNP常量
            
        异常:
            ValueError: 当问题类型不支持时抛出
        """
        if isinstance(problem_type, str) and problem_type in PROBLEM_TYPES:
            return PROBLEM_TYPES[problem_type]
        elif isinstance(problem_type, int) and problem_type in [PyCNP.CNP, PyCNP.DCNP, PyCNP.NWCNP]:
            return problem_type
        raise ValueError(f"不支持的问题类型: {problem_type}")
    
    @auto_convert
    def __init__(self, problem_data: 'PyCNP.ProblemData', 
                 problem_type: Union[str, int], 
                 bound: int,
                 K: int = 2**30,  
                 memetic_search_params: MemeticSearchParams = None, 
                 is_ir_used: bool = True, 
                 seed: int = 0,
                 stopping_criterion: Optional[StoppingCriterion] = None, 
                 verbose: bool = False):
        """
        初始化MemeticSearch算法
        
        参数:
            problem_data: 问题数据引用
            problem_type: 问题类型 ("CNP", "DCNP", "NWCNP")或PyCNP常量
            bound: 需要移除的节点数量
            K: NWCNP问题的k值，默认为无穷大
            memetic_search_params: 种群参数，包含搜索策略
            is_ir_used: 是否使用IR技术
            seed: 随机数种子
            stopping_criterion: 停止准则
            verbose: 是否打印详细信息
        """
        self.problem_data = problem_data
        self.problem_type = problem_type  # 已经被装饰器转换为PyCNP常量
        self.bound = bound
        self.K = K
        self.memetic_search_params = memetic_search_params or MemeticSearchParams()
        self.is_ir_used = is_ir_used
        self.seed = seed 
        self.verbose = verbose
        
        # 设置Python随机数种子
        random.seed(seed)
        
        # 检查问题类型和搜索策略的兼容性
        if self.problem_type == PyCNP.DCNP:
            # 如果问题类型是DCNP，则搜索策略只能是BCLS
            search_strategy = getattr(self.memetic_search_params, "searchStrategy", None)
            if search_strategy is not None and search_strategy != PyCNP.BCLS:
                raise ValueError("DCNP问题类型目前只支持BCLS搜索策略")
        elif self.problem_type in [PyCNP.CNP, PyCNP.NWCNP]:
            # CNP和NWCNP不支持BCLS搜索策略
            search_strategy = getattr(self.memetic_search_params, "searchStrategy", None)
            if search_strategy is not None and search_strategy == PyCNP.BCLS:
                raise ValueError("CNP和NWCNP问题类型不支持BCLS搜索策略")
                
        # 记录最优解信息
        self.best_solution = set()
        self.best_obj_value = float('inf')
        
        # 停止准则
        self.stopping_criterion = stopping_criterion
        
        # 记录算法开始时间
        self.algorithm_start_time = time.time()
        
        # 初始化原始图 - 注意将种子显式传递给createOriginalGraph
        try:
            self.original_graph = self.problem_data.create_original_graph(
                self.problem_type, self.bound, self.seed, self.K
            )
        except Exception as e:
            raise RuntimeError(f"创建原始图失败: {e}, 参数: problem_type={self.problem_type}, "
                               f"bound={self.bound}, seed={self.seed}")
    
    def initialize_population(self) -> None:
        """
        初始化种群并生成随机解
        """
        if self.verbose:
            print(f"初始化种群 (大小: {self.memetic_search_params.initPopSize})...")
        
        # 创建种群对象
        self.population = PyCNP.Population(self.original_graph, self.memetic_search_params, self.seed)
        
        # 初始化种群，获取初始最优解
        best_solution, best_obj_value = self.population.initialize(
            self.verbose, 
            self.stopping_criterion if self.stopping_criterion else None
        )
        
        # 重置除了最大运行时间以外的其他停止准则状态
        if self.stopping_criterion is not None:
            # 如果是多准则停止条件
            if hasattr(self.stopping_criterion, "criteria"):
                for criterion in self.stopping_criterion.criteria:
                    # 跳过最大运行时间准则
                    if criterion.get_name() == "MaxRuntime":
                        continue
                    # 重置其他准则状态
                    if hasattr(criterion, "reset"):
                        criterion.reset()
            # 如果是单个准则且不是最大运行时间准则
            elif self.stopping_criterion.get_name() != "MaxRuntime":
                if hasattr(self.stopping_criterion, "reset"):
                    self.stopping_criterion.reset()
        
        # 更新最优解
        if best_obj_value < self.best_obj_value:
            self.best_obj_value = best_obj_value
            self.best_solution = best_solution
    
    def get_elapsed_time(self) -> float:
        """
        获取算法已运行时间
        
        返回:
            已运行时间(秒)
        """
        return time.time() - self.algorithm_start_time
    
    def expand_population(self) -> None:
        """
        扩展种群大小
        
        当种群长时间无改进时，扩大种群以增加解的多样性
        """
        if self.verbose:
            print(f"扩展种群，当前大小: {self.population.get_size()}")
        
        # 使用C++的expand方法
        self.population.expand()
        
        if self.verbose:
            print(f"扩展后的种群大小: {self.population.get_size()}")
    
    def rebuild_population(self) -> None:
        """
        重建种群
        
        当种群长时间无改进且已达到最大种群大小时，重建种群以避免陷入局部最优
        """
        if self.verbose:
            print("重建种群")
        
        # 使用C++的rebuild方法
        self.population.rebuild()
        
        if self.verbose:
            print(f"重建种群完成，种群大小: {self.population.get_size()}")
    
    def apply_crossover(self) -> 'PyCNP.Graph':
        """
        执行交叉操作
        
        根据不同的图类型选择相应的交叉策略
        
        返回:
            交叉后的子代图
        """
        from PyCNP import Crossover
        # 创建Crossover对象并设置种子
        crossover = Crossover(self.seed)
        
        # 根据图类型选择适当的交叉策略
        if self.original_graph.__class__.__name__ == "DCNP_Graph":
            # DCNP图使用三重骨架交叉
            sol1, sol2, sol3 = self.population.get_all_three_solutions()
            offspring_graph = crossover.triple_backbone_based_crossover(
                self.original_graph, [sol1, sol2, sol3])
        else:
            # 其他图类型使用双重骨架交叉或RSC
            parent1, parent2 = self.population.random_select_two_solutions()
            parent_ptrs = [parent1, parent2]
            
            if self.is_ir_used:
                offspring_graph = crossover.reduce_solve_combine(self.original_graph, parent_ptrs)
            else:
                offspring_graph = crossover.double_backbone_based_crossover(self.original_graph, parent_ptrs)
        
        return offspring_graph
    
    def apply_local_search(self, graph: 'PyCNP.Graph') -> 'PyCNP.SearchResult':
        """
        执行局部搜索
        
        参数:
            graph: 要搜索的图
            
        返回:
            搜索结果
        """
        from PyCNP import Search
        # 创建Search对象并传递种子
        search = Search(graph, self.seed)
        search.set_strategy(self.memetic_search_params.search_strategy)
        return search.run()
    
    def run(self) -> 'Result':
        """
        运行算法
        
        返回:
            算法结果对象，包含最优解和目标值、迭代次数、运行时间
            
        异常:
            RuntimeError: 当未设置停止准则时
        """
        if not self.stopping_criterion:
            raise RuntimeError("未设置停止准则")
        
        # 初始化种群
        self.initialize_population()
        num_idle_generations = 0
        iterations = 0
        
        # 主循环 - 使用停止准则控制
        while not self.stopping_criterion(self.best_obj_value):
            iterations += 1
            
            # 执行交叉操作
            offspring_graph = self.apply_crossover()
            
            # 执行局部搜索
            result = self.apply_local_search(offspring_graph)
            
            # 更新种群
            self.population.update(result.solution, result.obj_value)
            
            # 处理种群管理 - 扩展或重建
            if (num_idle_generations > 0 and 
                num_idle_generations % self.memetic_search_params.MAX_IDLE_STEPS == 0 and 
                self.memetic_search_params.IS_POP_VARIABLE):
                # 如果种群大小小于最大大小，则扩展种群
                if self.population.get_size() < self.memetic_search_params.MAXPOPULATIONSIZE:
                    self.expand_population()
                # 如果种群大于最小大小，则重建种群
                else:
                    self.rebuild_population()
                
            
            # 更新最优解
            if result.obj_value < self.best_obj_value:
                self.best_solution = result.solution
                self.best_obj_value = result.obj_value
                num_idle_generations = 0
            else:
                num_idle_generations += 1
            
            # 定期输出状态信息
            if self.verbose and iterations % 10 == 0:
                elapsed = self.get_elapsed_time()
                print(f"迭代 {iterations} ({elapsed:.2f}秒): 当前最优值 = {self.best_obj_value}, "
                      f"空闲代数 = {num_idle_generations}, 种群大小 = {self.population.get_size()}")
        
        # 算法结束，输出结果
        if self.verbose:
            print(f"算法完成! 迭代次数: {iterations}, 总运行时间: {self.get_elapsed_time():.2f}秒")
            print(f"最优解: {sorted(list(self.best_solution))}")
            print(f"最优值: {self.best_obj_value}")
        
        # 创建返回结果
        return Result(
            best_solution=self.best_solution, 
            best_obj_value=self.best_obj_value,
            iterations=iterations,
            runtime=self.get_elapsed_time()
        )
