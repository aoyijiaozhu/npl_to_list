
import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


def point_cloud_to_fixed_ratio_depth_map(ply_file):
    # 定义固定的网格尺寸
    GRID_Y = 20  # Y轴固定映射为20行
    MAX_GRID_X = 450  # X轴最大400列

    # 1. 读取点云
    print(f"正在读取文件: {ply_file}...")
    pcd = o3d.io.read_point_cloud(ply_file)
    if pcd.is_empty():
        print("读取失败，请检查文件路径。")
        return None

    points = np.asarray(pcd.points)
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    # 2. 计算物理分辨率（极其重要的一步）
    # 获取 Y 轴的物理极值
    y_min, y_max = np.min(y), np.max(y)
    x_min = np.min(x)

    # 物理分辨率 = Y轴总物理宽度 / 20 个格子
    # 加上 1e-8 防止除零错误
    resolution = (y_max - y_min + 1e-8) / GRID_Y

    print(f"传送带物理宽度: {y_max - y_min:.4f} 单位")
    print(f"每个网格代表的物理尺寸: {resolution:.4f} 单位/格")

    # 3. 计算 X 和 Y 对应的网格索引 (采用完全相同的 resolution)
    y_idx = np.floor((y - y_min) / resolution).astype(int)
    x_idx = np.floor((x - x_min) / resolution).astype(int)

    # 安全限制：确保 y_idx 最高不超过 19
    y_idx = np.clip(y_idx, 0, GRID_Y - 1)

    # 4. 过滤掉超出 400 列长度的 X 点（如果物体比传送带缓冲区还长）
    # 如果物体较短，这里所有的点都会被保留 (x_idx < 400)
    valid_mask = x_idx < MAX_GRID_X
    x_idx = x_idx[valid_mask]
    y_idx = y_idx[valid_mask]
    z_valid = z[valid_mask]

    actual_length_grids = np.max(x_idx) + 1 if len(x_idx) > 0 else 0
    print(f"当前物体实际占据的 X 轴列数: {actual_length_grids} / 400")

    # 5. 创建 20 * 400 的固定尺寸二维数组 (默认全 0)
    depth_map = np.zeros((GRID_Y, MAX_GRID_X))
    counts = np.zeros((GRID_Y, MAX_GRID_X))

    # 累加每个格子里的 Z 值和点数
    np.add.at(depth_map, (y_idx, x_idx), z_valid)
    np.add.at(counts, (y_idx, x_idx), 1)

    # 计算平均高度
    with np.errstate(invalid='ignore', divide='ignore'):
        depth_map = np.divide(depth_map, counts)

    # 将没有点落入的空格子（包含右侧未填满的区域）设为 0
    depth_map[counts == 0] = 0

    # 6. 可视化验证
    plt.figure(figsize=(15, 3))
    plt.imshow(depth_map, cmap='jet', aspect='auto', origin='lower')
    plt.colorbar(label='Z Depth (Height)')

    # 画一条垂直的虚线，标示出物体实际结束的位置，方便你直观检查
    if actual_length_grids < MAX_GRID_X:
        plt.axvline(x=actual_length_grids, color='white', linestyle='--', label='End of Object')
        plt.legend(loc='upper right')

    plt.title(f"20x400 Conveyor Belt Depth Map (Actual length: {actual_length_grids} grids)")
    plt.xlabel("X-axis (Max 400 cols)")
    plt.ylabel("Y-axis (20 rows)")
    plt.show()

    # 7. 保存结果
    #save_name = "conveyor_depth_20x450.npy"
    #np.save(save_name, depth_map)
    #print(f"\n完美！二维数组已生成并保存为 {save_name}。")

    return depth_map


if __name__ == "__main__":
    my_depth_array = point_cloud_to_fixed_ratio_depth_map("cleaned_cloud.ply")