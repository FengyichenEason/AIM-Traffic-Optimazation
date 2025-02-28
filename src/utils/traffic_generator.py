import numpy as np
import pandas as pd
from typing import List, Optional


class TrafficGenerator:
    @staticmethod
    def generate_vehicle_flows(
            p_list: List[float],
            total_time: int,
            bus_start_time: int = 2,
            bus_interval: int = 8
    ) -> pd.DataFrame:
        """
        生成多路段车流信息

        :param p_list: 每条道路的车流密度概率
        :param total_time: 总模拟时间
        :param bus_start_time: 公交车起始时间
        :param bus_interval: 公交车发车间隔
        :return: 车流信息DataFrame
        """
        car_information_list = []

        for road_index, p in enumerate(p_list):
            # 生成小汽车车流
            car_flow = np.random.binomial(n=1, p=p, size=int(total_time / 2 + 1))

            # 添加公交车
            for i in range(len(car_flow)):
                if i < bus_start_time / 2:
                    if car_flow[i] == 0:
                        car_flow[i] = None
                    elif car_flow[i] == 1:
                        car_flow[i] = 0
                else:
                    if (i - bus_start_time / 2) % (bus_interval / 2) == 0:
                        car_flow[i] = 1
                    elif car_flow[i] == 0:
                        car_flow[i] = None
                    elif car_flow[i] == 1:
                        car_flow[i] = 0

            car_information_list.append(car_flow)

        return pd.DataFrame(car_information_list).T

    @staticmethod
    def generate_experiment_scenarios(
            base_density: float = 0.3,
            num_experiments: int = 6,
            time: int = 50
    ) -> List[pd.DataFrame]:
        """
        生成不同车流密度的实验场景

        :param base_density: 基础车流密度
        :param num_experiments: 实验组数
        :param time: 总模拟时间
        :return: 实验场景列表
        """
        scenarios = []

        for i in range(num_experiments):
            # 生成基础车流密度列表
            p_list = [base_density] * 12

            # 对第一条道路调整车流密度
            p_list[0] = base_density + 2 * i / 10

            # 生成车流信息
            scenario = TrafficGenerator.generate_vehicle_flows(
                p_list=p_list,
                total_time=time
            )

            scenarios.append(scenario)

        return scenarios


def main():
    # 生成实验场景示例
    scenarios = TrafficGenerator.generate_experiment_scenarios()

    # 保存每个场景
    for i, scenario in enumerate(scenarios, 1):
        scenario.to_csv(f'experiment_{i}.csv', index=False)
        print(f"生成实验场景 {i}")


if __name__ == '__main__':
    main()