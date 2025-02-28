import os
import yaml
import logging
from typing import Dict, Any, List
import pandas as pd

from src.core.model import run_traffic_optimization
from src.utils.traffic_generator import TrafficGenerator
from src.visualization.performance_metrics import PerformanceAnalyzer


class ExperimentManager:
    def __init__(self, config_path: str = 'configs/default_config.yaml'):
        """
        初始化实验管理器

        :param config_path: 配置文件路径
        """
        # 配置日志
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.__class__.__name__)

        # 加载配置
        self.load_config(config_path)

        # 创建输出目录
        self.create_output_directories()

    def load_config(self, config_path: str):
        """
        加载配置文件

        :param config_path: 配置文件路径
        """
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            self.logger.info(f"成功加载配置文件: {config_path}")
        except Exception as e:
            self.logger.error(f"加载配置文件失败: {e}")
            raise

    def create_output_directories(self):
        """
        创建输出目录
        """
        output_dirs = [
            self.config.get('output_dir', 'outputs'),
            os.path.join(self.config.get('output_dir', 'outputs'), 'experiments'),
            os.path.join(self.config.get('output_dir', 'outputs'), 'visualizations'),
            os.path.join(self.config.get('output_dir', 'outputs'), 'logs')
        ]

        for dir_path in output_dirs:
            os.makedirs(dir_path, exist_ok=True)

    def run_density_experiments(
            self,
            base_density: float = 0.3,
            num_experiments: int = 6
    ):
        """
        运行不同车流密度的系列实验

        :param base_density: 基础车流密度
        :param num_experiments: 实验组数
        :return: 实验结果列表
        """
        results = []

        # 生成车流场景
        scenarios = TrafficGenerator.generate_experiment_scenarios(
            base_density=base_density,
            num_experiments=num_experiments
        )

        for exp_index, scenario in enumerate(scenarios, 1):
            self.logger.info(f"开始第 {exp_index} 组实验")

            try:
                # 准备实验配置
                exp_config = self.config.copy()
                exp_config['car_list'] = self._convert_scenario_to_car_list(scenario)

                # 运行优化模型
                model_result = run_traffic_optimization(exp_config)

                # 分析性能
                performance = PerformanceAnalyzer.analyze_model_results(model_result)

                # 保存结果
                self._save_experiment_results(exp_index, scenario, performance)

                results.append(performance)

            except Exception as e:
                self.logger.error(f"实验 {exp_index} 失败: {e}")

        return results

    def _convert_scenario_to_car_list(self, scenario: pd.DataFrame) -> List[List[int]]:
        """
        将场景转换为车辆列表

        :param scenario: 车流场景DataFrame
        :return: 车辆信息列表
        """
        car_list = []

        for road in range(scenario.shape[1]):
            for time, vehicle_type in enumerate(scenario.iloc[:, road]):
                if pd.notna(vehicle_type):
                    car_list.append([
                        time * 2,  # 发车时间
                        int(vehicle_type),  # 车辆类型(0:小汽车, 1:公交车)
                        road + 1  # 道路编号
                    ])

        return car_list

    def _save_experiment_results(
            self,
            exp_index: int,
            scenario: pd.DataFrame,
            performance: Dict[str, Any]
    ):
        """
        保存实验结果

        :param exp_index: 实验编号
        :param scenario: 车流场景
        :param performance: 性能指标
        """
        # 保存车流场景
        scenario_path = os.path.join(
            self.config.get('output_dir', 'outputs'),
            'experiments',
            f'scenario_{exp_index}.csv'
        )
        scenario.to_csv(scenario_path, index=False)

        # 保存性能指标
        performance_path = os.path.join(
            self.config.get('output_dir', 'outputs'),
            'experiments',
            f'performance_{exp_index}.yaml'
        )
        with open(performance_path, 'w') as f:
            yaml.dump(performance, f)


def main():
    # 运行实验管理器示例
    experiment_manager = ExperimentManager()

    # 运行车流密度实验
    results = experiment_manager.run_density_experiments()

    # 打印总体结果
    for i, result in enumerate(results, 1):
        print(f"实验 {i} 结果:")
        print(result)


if __name__ == '__main__':
    main()