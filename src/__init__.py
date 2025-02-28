# 创建必要的 __init__.py 文件

import os

# 创建目录结构
dirs = [
    'src',
    'src/core',
    'src/utils',
    'src/visualization',
    'src/experiments'
]

# 创建目录和空 __init__.py 文件
for dir_path in dirs:
    os.makedirs(dir_path, exist_ok=True)
    init_path = os.path.join(dir_path, '__init__.py')

    # 如果文件不存在，创建空文件
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write('# Python package initialization\n')
        print(f"Created {init_path}")

print("初始化完成")