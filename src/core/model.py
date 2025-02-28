import gurobipy
import numpy as np
from typing import List, Dict, Any


class TrafficOptimizationModel:
    def __init__(self, config: Dict[str, Any]):
        """
        初始化交通优化模型

        :param config: 模型配置参数
        """
        self.config = config

        # 从配置中提取关键参数
        self.total_time = config.get('total_time', 80)
        self.road_length = config.get('road_length', [154, 145, 154, 145])
        self.vehicle_types = config.get('vehicle_types', {
            'car': {'v_min': 0, 'v_max': 12, 'a_min': -3, 'a_max': 3},
            'bus': {'v_min': 0, 'v_max': 10, 'a_min': -2, 'a_max': 2}
        })

        # 初始化Gurobi模型
        self.model = gurobipy.Model()
        self.model.Params.NonConvex = 2
        self.model.Params.MIPGap = 0.001
        self.model.Params.TimeLimit = 1500

    def create_variables(self, car_count: int):
        """
        创建优化变量

        :param car_count: 车辆数量
        """
        # 位置变量
        self.x = self.model.addVars(car_count, self.total_time, name='x')

        # 速度变量
        self.v = self.model.addVars(car_count, self.total_time, name='v')

        # 是否在有效区域变量
        self.w = self.model.addVars(car_count, self.total_time,
                                    vtype=gurobipy.GRB.BINARY, name='w')

        # 是否进入初始点变量
        self.theta = self.model.addVars(car_count, self.total_time,
                                        vtype=gurobipy.GRB.BINARY, name='theta')

    def add_constraints(self,
                        car_count: int,
                        car_type: List[int],
                        car_route: List[int],
                        initial_time: List[int]):
        """
        添加约束条件

        :param car_count: 车辆数量
        :param car_type: 车辆类型列表
        :param car_route: 车辆路线列表
        :param initial_time: 车辆初始时间列表
        """
        # 初始速度约束
        self.model.addConstrs(
            self.v[c, initial_time[c]] == self.config.get('initial_velocity', 6)
            for c in range(car_count)
        )

        # 速度和加速度约束
        for c in range(car_count):
            vehicle_type = 'bus' if car_type[c] else 'car'
            type_config = self.vehicle_types[vehicle_type]

            # 速度下限约束
            self.model.addConstrs(
                self.v[c, t] >= type_config['v_min']
                for t in range(initial_time[c], self.total_time)
            )

            # 速度上限约束
            self.model.addConstrs(
                self.v[c, t] <= type_config['v_max']
                for t in range(initial_time[c], self.total_time)
            )

            # 加速度约束
            self.model.addConstrs(
                (self.v[c, t] - self.v[c, t - 1]) >= type_config['a_min']
                for t in range(initial_time[c] + 1, self.total_time)
            )
            self.model.addConstrs(
                (self.v[c, t] - self.v[c, t - 1]) <= type_config['a_max']
                for t in range(initial_time[c] + 1, self.total_time)
            )

    def set_objective(self, car_count: int, car_type: List[int]):
        """
        设置目标函数

        :param car_count: 车辆数量
        :param car_type: 车辆类型列表
        """
        # 最小化延迟成本
        cost_car = self.config.get('cost_car', 1)
        cost_bus = self.config.get('cost_bus', 1)

        self.model.setObjective(
            gurobipy.quicksum(
                (cost_car * (1 - car_type[c]) + cost_bus * car_type[c]) * self.w[c, t]
                for c in range(car_count)
                for t in range(self.total_time)
            ),
            sense=gurobipy.GRB.MINIMIZE
        )

    def solve(self):
        """
        求解优化模型
        """
        self.model.optimize()
        return self.model


def run_traffic_optimization(config: Dict[str, Any]):
    """
    运行交通优化

    :param config: 配置参数
    :return: 优化结果
    """
    # 车辆信息生成
    car_list = config.get('car_list', [])

    # 初始化模型
    optimizer = TrafficOptimizationModel(config)

    # 创建变量
    optimizer.create_variables(len(car_list))

    # 提取车辆信息
    car_type = [car[1] for car in car_list]
    car_route = [car[2] for car in car_list]
    initial_time = [car[0] for car in car_list]

    # 添加约束
    optimizer.add_constraints(
        car_count=len(car_list),
        car_type=car_type,
        car_route=car_route,
        initial_time=initial_time
    )

    # 设置目标函数
    optimizer.set_objective(
        car_count=len(car_list),
        car_type=car_type
    )

    # 求解并返回结果
    return optimizer.solve()


# 使用示例
if __name__ == '__main__':
    sample_config = {
        'total_time': 80,
        'road_length': [154, 145, 154, 145],
        'vehicle_types': {
            'car': {'v_min': 0, 'v_max': 12, 'a_min': -3, 'a_max': 3},
            'bus': {'v_min': 0, 'v_max': 10, 'a_min': -2, 'a_max': 2}
        },
        'initial_velocity': 6,
        'cost_car': 1,
        'cost_bus': 1,
        # 在这里添加车辆列表等其他配置
    }

    result = run_traffic_optimization(sample_config)