import nbformat as nbf
import os
import sys
import json
import logging


class NotebookGenerator:
    def __init__(self, output_dir='notebooks'):
        """
        初始化Notebook生成器

        :param output_dir: 输出目录
        """
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s: %(message)s'
        )
        self.logger = logging.getLogger(__name__)

        # 确保输出目录存在
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

        # 设置Python路径
        self._setup_python_path()

    def _setup_python_path(self):
        """
        设置Python模块搜索路径
        """
        # 获取项目根目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, '..'))

        # 添加项目根目录到系统路径
        if project_root not in sys.path:
            sys.path.insert(0, project_root)

        self.logger.info(f"项目根目录已添加: {project_root}")

    def _create_markdown_cell(self, content):
        """
        创建Markdown单元格

        :param content: Markdown内容
        :return: Markdown单元格
        """
        return nbf.v4.new_markdown_cell(content)

    def _create_code_cell(self, content, metadata=None):
        """
        创建代码单元格

        :param content: 代码内容
        :param metadata: 单元格元数据
        :return: 代码单元格
        """
        return nbf.v4.new_code_cell(
            source=content,
            metadata=metadata or {}
        )

    def generate_analysis_notebook(self):
        """
        生成综合分析Notebook

        :return: Notebook对象
        """
        # 创建新的Notebook
        nb = nbf.v4.new_notebook()
        nb['cells'] = []

        # 添加标题和介绍
        nb['cells'].append(self._create_markdown_cell("""
# 交通优化系统综合分析报告

## 项目概述
本Notebook提供了交通优化实验的全面分析，包括:
- 实验结果比较
- 性能指标分析
- 多维度可视化
- 关键洞察

**注意**: 运行此Notebook需要完整的项目环境和依赖。
"""))

        # 添加环境和路径设置
        nb['cells'].append(self._create_code_cell("""
# 环境配置与依赖导入
import sys
import os
import warnings

# 抑制警告信息
warnings.filterwarnings('ignore')

# 获取并打印当前Python路径
print("Python Path:")
for path in sys.path:
    print(path)

# 导入数据科学和可视化库
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 项目特定模块
try:
    from src.experiments.experiment_manager import ExperimentManager
    from src.visualization.performance_metrics import PerformanceAnalyzer
    print("成功导入项目模块")
except ImportError as e:
    print(f"模块导入错误: {e}")
    print("请检查项目结构和PYTHONPATH")

# 配置可视化样式
plt.style.use('seaborn')
sns.set_context('notebook')
"""))

        # 运行实验并分析
        nb['cells'].append(self._create_code_cell("""
# 运行实验并获取结果
try:
    experiment_manager = ExperimentManager()
    results = experiment_manager.run_density_experiments()

    # 性能比较
    comparison = PerformanceAnalyzer.compare_experiments(results)
    print("实验结果综合比较:")
    for key, value in comparison.items():
        print(f"{key}: {value}")
except Exception as e:
    print(f"实验运行出错: {e}")
"""))

        # 数据处理与转换
        nb['cells'].append(self._create_code_cell("""
# 数据预处理
try:
    # 将实验结果转换为DataFrame以便分析
    df_results = pd.DataFrame(results)

    # 基本统计描述
    print("\\n实验结果描述性统计:")
    print(df_results.describe())
except Exception as e:
    print(f"数据处理出错: {e}")
"""))

        # 多样化可视化
        nb['cells'].append(self._create_code_cell("""
# 多维度可视化分析
try:
    # 1. 目标函数值箱线图
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=df_results['objective_value'])
    plt.title('目标函数值分布')
    plt.xlabel('目标函数值')
    plt.tight_layout()
    plt.show()

    # 2. 求解时间散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(
        df_results.index, 
        df_results['solve_time'], 
        alpha=0.7
    )
    plt.title('实验求解时间')
    plt.xlabel('实验组')
    plt.ylabel('求解时间(秒)')
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"可视化出错: {e}")
"""))

        # 高级统计分析
        nb['cells'].append(self._create_code_cell("""
# 高级统计分析
try:
    # 目标函数值相关性分析
    correlation_matrix = df_results[['objective_value', 'solve_time']].corr()
    print("\\n相关性矩阵:")
    print(correlation_matrix)

    # 假设检验
    from scipy import stats

    # 单样本t检验
    t_statistic, p_value = stats.ttest_1samp(
        df_results['objective_value'], 
        popmean=np.mean(df_results['objective_value'])
    )
    print("\\n目标函数值单样本t检验:")
    print(f"t统计量: {t_statistic}")
    print(f"p值: {p_value}")
except Exception as e:
    print(f"统计分析出错: {e}")
"""))

        # 保存Notebook
        notebook_path = os.path.join(self.output_dir, 'comprehensive_analysis.ipynb')

        try:
            with open(notebook_path, 'w', encoding='utf-8') as f:
                nbf.write(nb, f)

            self.logger.info(f"Notebook已成功保存到 {notebook_path}")
            return nb

        except Exception as e:
            self.logger.error(f"保存Notebook时发生错误: {e}")
            return None


def main():
    generator = NotebookGenerator()
    generator.generate_analysis_notebook()


if __name__ == '__main__':
    main()