import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


def point_cloud_to_depth_map(ply_file):
    # 定义网格尺寸：20行(Y轴), 400列(X轴)
    grid_rows = 20  # 对应 Y 轴
    grid_cols = 400  # 对应 X 轴

    # 1. 读取点云
    print(f"正在读取文件: {ply_file}...")
    pcd = o3d.io.read_point_cloud(ply_file)
    if pcd.is_empty():
        print("读取失败，请检查文件路径。")
        return

    points = np.asarray(pcd.points)
    x = points[:, 0]
    y = points[:, 1]
    z = points[:, 2]

    # 2. 将 X 和 Y 坐标分别归一化到 [0, 1] 之间
    x_norm = (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-8)
    y_norm = (y - np.min(y)) / (np.max(y) - np.min(y) + 1e-8)

    # 映射到对应的网格索引中
    x_idx = np.floor(x_norm * grid_cols).astype(int)
    y_idx = np.floor(y_norm * grid_rows).astype(int)

    # 防止最大值越界
    x_idx = np.clip(x_idx, 0, grid_cols - 1)
    y_idx = np.clip(y_idx, 0, grid_rows - 1)

    # 3. 创建 20 * 400 的二维数组
    depth_map = np.zeros((grid_rows, grid_cols))
    counts = np.zeros((grid_rows, grid_cols))

    # 累加每个格子里的 Z 值和点数 (注意 NumPy 的索引是 [行, 列]，即 [y, x])
    np.add.at(depth_map, (y_idx, x_idx), z)
    np.add.at(counts, (y_idx, x_idx), 1)

    # 计算平均高度
    with np.errstate(invalid='ignore', divide='ignore'):
        depth_map = np.divide(depth_map, counts)

    # 将没有点落入的“空洞”格子设为 0
    depth_map[counts == 0] = 0

    print(f"成功生成深度二维数组，当前形状: {depth_map.shape} (行x列)")

    # 4. 可视化
    plt.figure(figsize=(15, 3))

    # cmap='jet' 保留光谱渐变，origin='lower' 让 Y 轴起点在下方
    plt.imshow(depth_map, cmap='jet', aspect='auto', origin='lower')
    plt.colorbar(label='Z Depth (Height)')
    plt.title("20x400 Depth Map Array (Y-axis vs X-axis)")
    plt.xlabel("X-axis (400 cols)")
    plt.ylabel("Y-axis (20 rows)")
    plt.show()

    # 5. 保存
    save_name = "depth_map_20x450.npy"
    np.save(save_name, depth_map)
    print(f"二维数组已保存为 {save_name}。")

    return depth_map


if __name__ == "__main__":
    my_depth_array = point_cloud_to_depth_map("cleaned_cloud.ply")