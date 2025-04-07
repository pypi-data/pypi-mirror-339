# PyCNP：临界节点问题求解框架的Python绑定

PyCNP是一个用于求解临界节点问题(Critical Node Problem, CNP)及其变种的Python库。它提供了C++实现的核心算法的Python绑定，以及纯Python实现的易用接口。

## 功能特点

- 支持多种临界节点问题变种：
  - 标准CNP问题
  - 有向CNP问题(DCNP)
  - 带节点权重的CNP问题(NWCNP)
- 提供多种搜索策略：
  - 基于组件的邻域搜索(CBNS)
  - 基于连接与噪声的邻域搜索(CHNS)
  - 有向局部搜索(DLAS)
  - 基于介数中心性的局部搜索(BCLS)
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
git clone https://github.com/yourusername/PyCNP.git
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
import PyCNP
from pycnp import MemeticSearch, MemeticSearchParams

# 创建问题数据
problem_data = PyCNP.ProblemData(20)  # 创建20个节点的图
# 添加一些边
for i in range(20):
    for j in range(i+1, 20):
        if (i+j) % 3 == 0:
            problem_data.add_edge(i, j)

# 配置参数
seed = 2
bound = 5
problem_type = PyCNP.CNP
search_strategy = PyCNP.CHNS

# 创建时间约束准则
stopping_criterion = PyCNP.StoppingCriterionFactory.createTimeCriterion(60)  # 60秒时间限制

# 配置种群参数
memetic_search_params = MemeticSearchParams()
memetic_search_params.IS_POP_VARIABLE = False  # 是否使用变种群
memetic_search_params.initPopSize = 5          # 初始种群大小

# 创建原始图
original_graph = problem_data.create_original_graph(problem_type, bound, seed)

# 初始化种群
population = PyCNP.Population(memetic_search_params.initPopSize)

# 获取随机解并添加到种群
for i in range(memetic_search_params.initPopSize):
    temp_graph = original_graph.get_random_feasible_graph()
    removed_nodes = temp_graph.get_removed_nodes()
    obj_value = temp_graph.get_objective_value()
    population.add(removed_nodes, obj_value)

# 使用MemeticSearch算法求解
ms = MemeticSearch(
    original_graph=original_graph,
    search_strategy=search_strategy,
    population=population,
    memetic_search_params=memetic_search_params,
    is_ir_used=True,
    seed=seed,
    stopping_criterion=stopping_criterion
)

# 运行算法
result = ms.run()

# 输出结果
print(f"最佳目标值: {result['best_obj_value']}")
print(f"最佳解: {list(result['best_solution'])}")
```

更多示例请参见`examples`目录。

## 开发指南

### 添加新的搜索策略

新的搜索策略需要继承`SearchStrategy`类并实现`execute`和`getName`方法：

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

### 添加新的停止准则

新的停止准则需要继承`StoppingCriterion`类并实现必要的方法：

```cpp
class MyNewCriterion : public StoppingCriterion
{
public:
    MyNewCriterion(/* 参数 */);
    ~MyNewCriterion() override = default;
    
    void initialize() override;
    bool shouldStop(int iterations, int current_obj_value) override;
    std::string getName() const override { return "MyNewCriterion"; }
    StoppingCriterion* clone() const override { return new MyNewCriterion(/* 参数 */); }
    
private:
    // 准则特定的变量
};
```

然后在`StoppingCriterion.cpp`文件中添加相应的工厂方法：

```cpp
std::unique_ptr<StoppingCriterion> StoppingCriterionFactory::createMyNewCriterion(/* 参数 */)
{
    return std::make_unique<MyNewCriterion>(/* 参数 */);
}
```

## 贡献

欢迎贡献代码、报告问题或提出建议。请通过GitHub Issues或Pull Requests提交您的贡献。

## 许可证

此项目使用 MIT 许可证。详情请参见 [LICENSE](LICENSE) 文件。