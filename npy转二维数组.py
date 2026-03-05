import numpy as np

# 1. 指定你的 .npy 文件路径
file_name = "depth_map_20x450.npy"

# 2. 读取文件并赋值给一个变量
depth_array = np.load(file_name)

# 3. 验证一下是否成功
print(f"成功读取！")
print(f"数组的形状是: {depth_array.shape}")  # 应该输出 (20, 450)
print(f"数组的数据类型是: {depth_array.dtype}")

# 你可以打印左上角的一小块数据看看（比如前 3 行，前 5 列）
print("\n左上角 3x5 的数据样本:")
print(depth_array)