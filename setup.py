from setuptools import setup, find_packages
import os


# 读取README内容
def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding='utf-8') as f:
        return f.read()


# 读取requirements
def read_requirements():
    with open(os.path.join(os.path.dirname(__file__), 'requirements.txt'), 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]


setup(
    name='aim-traffic-optimization',
    version='0.1.0',

    # 包发现
    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    # 作者信息
    author='Your Name',
    author_email='your.email@example.com',

    # 项目描述
    description='AI-driven Multi-Agent Traffic Optimization System',
    long_description=read_readme(),
    long_description_content_type='text/markdown',

    # 项目主页
    url='https://github.com/yourusername/aim-traffic-optimization',

    # 依赖项
    install_requires=read_requirements(),

    # 可选依赖
    extras_require={
        'dev': [
            'pytest>=6.2.0',
            'pytest-cov>=2.12.0',
            'mypy>=0.910',
            'black>=21.5b1',
            'flake8>=3.9.0'
        ],
        'docs': [
            'sphinx>=4.0.0',
            'sphinx-rtd-theme>=0.5.2'
        ],
        'visualization': [
            'plotly>=5.0.0'
        ]
    },

    # 分类
    classifiers=[
        # 开发状态
        'Development Status :: 3 - Alpha',

        # 目标受众
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',

        # 主题
        'Topic :: Scientific/Engineering :: Transportation',
        'Topic :: Software Development :: Libraries :: Python Modules',

        # 许可证
        'License :: OSI Approved :: MIT License',

        # Python版本
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',

        # 操作系统
        'Operating System :: OS Independent',
    ],

    # 关键词
    keywords='traffic-optimization multi-agent ai transportation',

    # Python版本要求
    python_requires='>=3.8',

    # 项目资源文件
    include_package_data=True,

    # 配置文件
    package_data={
        'aim_traffic_optimization': ['configs/*.yaml'],
    },

    # 控制台脚本入口
    entry_points={
        'console_scripts': [
            'aim-traffic-optimize=src.experiments.experiment_manager:main',
        ],
    },

    # 项目许可证
    license='MIT',
)