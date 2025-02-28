# AIM Traffic Optimization

## 项目简介

AIM（Artificial Intelligence Mobility）交通优化项目是一个基于多智能体的交通系统仿真与优化研究项目。该项目旨在通过先进的数学建模和优化算法，改善城市交通系统的效率和公平性。

## 主要特点

- 多智能体交通流仿真
- 车辆路径与信号灯协同优化
- 考虑小汽车和公交车的差异性能
- 支持不同车流密度场景模拟
- 灵活的性能评估与可视化

## 项目架构

```
AIM_Traffic_Optimization/
├── src/                # 源代码
│   ├── core/           # 核心优化模型
│   ├── utils/          # 工具函数
│   ├── visualization/  # 可视化工具
│   └── experiments/    # 实验管理
├── tests/              # 单元测试
├── configs/            # 配置文件
├── notebooks/          # Jupyter笔记本
├── requirements.txt
└── setup.py
```

## 环境准备

1. 克隆项目
```bash
git clone https://github.com/yourusername/AIM_Traffic_Optimization.git
cd AIM_Traffic_Optimization
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Windows使用 venv\Scripts\activate
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 安装Gurobi求解器许可证
注意：需要单独申请Gurobi许可证

## 使用示例

### 运行基础实验

```python
from src.experiments.experiment_manager import ExperimentManager

# 初始化实验管理器
experiment_manager = ExperimentManager()

# 运行车流密度实验
results = experiment_manager.run_density_experiments()

# 分析结果
from src.visualization.performance_metrics import PerformanceAnalyzer
comparison = PerformanceAnalyzer.compare_experiments(results)
```

### 自定义实验配置

修改 `configs/default_config.yaml` 可自定义实验参数

## 核心功能

1. 车流生成
2. 交通优化建模
3. 性能指标分析
4. 可视化展示

## 性能指标

- 总延迟时间
- 车辆通行效率
- 公交车与小汽车公平性

## 开发与贡献

1. Fork 项目
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 许可证

基于 MIT 许可证分发 - 详见 LICENSE 文件

## 引用

如果这个项目对您的研究有帮助，请引用：

```
@software{aim_traffic_optimization,
  title = {AIM Traffic Optimization},
  author = {Your Name},
  year = {2024},
  url = {https://github.com/yourusername/AIM_Traffic_Optimization}
}
```

## 联系方式

- 项目负责人：[Your Name]
- 邮箱：[your.email@example.com]
- 项目链接：[https://github.com/yourusername/AIM_Traffic_Optimization]