# PyCNP：临界节点问题求解框架的Python绑定

PyCNP是一个用于求解临界节点问题(Critical Node Problem, CNP)及其变种的Python库。它提供了C++实现的核心算法的Python绑定，以及纯Python实现的易用接口。

## 功能特点

- 支持多种临界节点问题变种：
  - 标准CNP问题
  - 基于距离的CNP问题(DCNP)
  - 带节点权重的CNP问题(NWCNP)
- 提供多种搜索策略：
  - 基于分量的邻域搜索(CBNS)
  - 基于分量的混合邻域搜索(CHNS)
  - 多样性的延迟接受搜索(DLAS)
  - 基于介数中心性的延迟接受搜索(BCLS)
- 支持多种停止准则：
  - 迭代次数
  - 求解时间限制
  - 解停滞
  - 多准则组合
- 提供Python友好的接口
- 高效的C++实现核心算法，提供最佳性能

## 安装

### 前提条件

- C++17兼容的编译器
- CMake 3.10+
- Python 3.6+
- pybind11

### 从源码安装

```bash
git clone https://github.com/xuebo100/PyCNP.git
cd PyCNP
./rebuild.sh
```

如果想要全局使用该库，请将以下行添加到您的`~/.bashrc`或`~/.zshrc`文件中：
```bash
export PYTHONPATH=/path/to/PyCNP:$PYTHONPATH
```

## 快速开始

以下是一个简单的例子，展示如何使用PyCNP库求解CNP问题：

```python
import sys
import os
import time
from pycnp import MemeticSearch, read, MemeticSearchParams
from pycnp.stop import MaxRuntime

# 确保PyCNP模块可以被找到
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 读取问题数据
problem_data = read("./Instances/NWCNP/model/ErdosRenyi_n941.txt")

# 配置参数
seed = 49
bound = 140  # 移除的节点数量
problem_type = "CNP"  # 问题类型

# 创建停止准则
max_runtime = 300  # 最大运行时间（秒）
stopping_criterion = MaxRuntime(max_runtime)

# 配置算法参数
params = MemeticSearchParams(
    search_strategy="CHNS",  # 使用混合邻域搜索策略
    IS_POP_VARIABLE=True,    # 使用变种群
    MAXPOPULATIONSIZE=20,    # 最大种群大小
    initPopSize=5,           # 初始种群大小
    INCREASE_POP_SIZE=3,     # 每次扩展增加3个个体
    MAX_IDLE_STEPS=100       # 100次迭代无改进则扩展/重建种群
)

# 使用MemeticSearch算法求解
ms = MemeticSearch(
    problem_data=problem_data,
    problem_type=problem_type,
    bound=bound,
    K=3,
    memetic_search_params=params,
    seed=seed,
    stopping_criterion=stopping_criterion,
    verbose=True
)

# 运行算法
start_time = time.time()
result = ms.run()
end_time = time.time()

# 输出结果
print(f"总运行时间: {end_time - start_time:.2f}秒")
print(f"最佳目标值: {result.best_obj_value}")
print(f"最佳解包含的节点数: {len(result.best_solution)}")
```

或者，您也可以使用更高级的Model接口：

```python
from pycnp import Model, MemeticSearchParams
from pycnp.stop import MaxRuntime

# 创建Model实例
model = Model()

# 添加节点和边
for i in range(10):
    model.add_node(i)

edges = [
    (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4),
    (3, 4), (3, 5), (4, 5), (5, 6), (6, 7), (7, 8),
    (7, 9), (8, 9)
]
for u, v in edges:
    model.add_edge(u, v)

# 设置停止准则
model.set_stopping_criterion(MaxRuntime(2))

# 求解CNP问题
result = model.solve(
    problem_type="CNP",
    bound=2,
    memetic_search_params=MemeticSearchParams(),
    is_ir_used=True,
    seed=1,
    verbose=True
)

print(f"最优解：{sorted(list(result.best_solution))}")
print(f"目标值：{result.best_obj_value}")
```

更多示例请参见`examples`目录。

## 开发指南

### 添加新的搜索策略

新的搜索策略需要继承`SearchStrategy`类并实现必要的方法。在C++中，搜索策略的实现如下：

```cpp
class MyNewStrategy : public SearchStrategy
{
public:
    MyNewStrategy(Graph &graph, const std::unordered_map<std::string, std::any> &params);
    virtual ~MyNewStrategy() = default;

    SearchResult execute() override;
    std::string getName() const override { return "MyNew"; }
    
    static std::unordered_map<std::string, std::any> getDefaultConfig();

private:
    Graph &graph;
    std::unordered_map<std::string, std::any> params;
    // 策略特定的变量和方法
};
```

然后在`Search.cpp`文件中注册新策略：

```cpp
void Search::registerStrategies()
{
    // 已有的策略...
    
    // 添加新策略
    strategyFactory["MyNew"] = [](Graph &g, const std::unordered_map<std::string, std::any> &p) {
        return std::make_unique<MyNewStrategy>(g, p);
    };
}
```

## 贡献

欢迎贡献代码、报告问题或提出建议。请通过GitHub Issues或Pull Requests提交您的贡献。

## 许可证

此项目使用 MIT 许可证。详情请参见 [LICENSE](LICENSE) 文件。