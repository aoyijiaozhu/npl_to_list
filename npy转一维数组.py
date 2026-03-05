#行优先符合要求
import numpy as np

# 1. 读取你保存的二维数组 (20行 x 400列)
# 为了演示，如果你还没有这个文件，你可以用 np.zeros((20, 400)) 代替测试
try:
    depth_array_2d = np.load("conveyor_depth_20x450.npy")
except FileNotFoundError:
    print("没找到文件，生成一个模拟矩阵...")
    depth_array_2d = np.arange(1, 7).reshape(2, 3) # 模拟一个极小的 2x3 数组来演示
    print(f"模拟二维数组:\n{depth_array_2d}\n")

print("="*40)

### 版本一：行优先 (Row-Major) - 默认 ###
# 提取顺序: (x1,y1), (x2,y1) ... 扫完第一行 -> (x1,y2), (x2,y2) ... 扫第二行
# 参数 order='C' (C-style)，这是 flatten() 的默认行为

array_row_major = depth_array_2d.flatten(order='C')
list_row_major = array_row_major.tolist()

print("【版本一：行优先】")
print(f"数据总长度: {len(list_row_major)}")
print(f"前 500 个元素预览: {list_row_major[:500]}")


print("\n" + "="*40 + "\n")


### 版本二：列优先 (Column-Major) ###
# 提取顺序: (x1,y1), (x1,y2) ... 扫完第一列 -> (x2,y1), (x2,y2) ... 扫第二列
# 工业意义：相当于传送带往前走一格(X)，截取一个完整的横截面轮廓(Y)
# 参数 order='F' (Fortran-style)

array_col_major = depth_array_2d.flatten(order='F')
list_col_major = array_col_major.tolist()

print("【版本二：列优先】")
print(f"数据总长度: {len(list_col_major)}")
print(f"前 100 个元素预览: {list_col_major[:100]}")