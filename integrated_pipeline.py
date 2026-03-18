import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


def process_point_cloud(input_file, y_min=0.3, y_max=1.65, nb_neighbors=10, std_ratio=3, grid_y=20, grid_x=450, visualize=False):
    """
    将PLY点云转换为一维深度数组

    Args:
        input_file: 输入PLY文件路径
        y_min: Y轴裁剪最小值（传送带宽度方向）
        y_max: Y轴裁剪最大值
        nb_neighbors: 异常点检测邻居数量
        std_ratio: 异常点检测标准差倍数
        grid_y: 网格行数（固定20行）
        grid_x: 网格列数（最大450列）
        visualize: 是否可视化每个处理阶段

    Returns:
        list: 行优先一维深度数组，长度为grid_y * grid_x
    """

    # 读取点云
    pcd = o3d.io.read_point_cloud(input_file)
    if pcd.is_empty():
        raise FileNotFoundError(f"Cannot read: {input_file}")
    if visualize:
        o3d.visualization.draw_geometries([pcd], window_name="1. 原始点云")

    # 第一次原点偏移：将XY最小值移至原点
    points = np.asarray(pcd.points)
    points[:, :2] -= points[:, :2].min(axis=0)
    if visualize:
        o3d.visualization.draw_geometries([pcd], window_name="2. 第一次原点偏移")

    # 裁剪Y轴范围
    mask = (points[:, 1] >= y_min) & (points[:, 1] <= y_max)
    pcd = pcd.select_by_index(np.where(mask)[0])
    if visualize:
        o3d.visualization.draw_geometries([pcd], window_name="3. 裁剪Y轴")

    # 去除异常点
    _, ind = pcd.remove_statistical_outlier(nb_neighbors, std_ratio)
    points = np.asarray(pcd.points)[ind]
    if visualize:
        pcd_clean = pcd.select_by_index(ind)
        o3d.visualization.draw_geometries([pcd_clean], window_name="4. 去除异常点")

    # 第二次原点偏移
    points[:, :2] -= points[:, :2].min(axis=0)

    # 计算网格分辨率并映射到网格索引
    x, y, z = points.T
    res = (y.max() - y.min() + 1e-8) / grid_y
    y_idx = np.clip((y / res).astype(int), 0, grid_y - 1)
    x_idx = (x / res).astype(int)

    # 过滤超出X轴范围的点，累加深度值
    mask = x_idx < grid_x
    depth = np.zeros((grid_y, grid_x))
    counts = np.zeros((grid_y, grid_x))
    np.add.at(depth, (y_idx[mask], x_idx[mask]), z[mask])
    np.add.at(counts, (y_idx[mask], x_idx[mask]), 1)

    # 计算平均深度，转为行优先一维数组
    np.divide(depth, counts, out=depth, where=counts > 0)
    if visualize:
        plt.figure(figsize=(15, 3))
        plt.imshow(depth, cmap='jet', aspect='auto', origin='lower')
        plt.colorbar(label='Depth')
        plt.title("5. 深度图")
        plt.show()
    return depth.flatten().tolist()

if __name__ == "__main__":
    result = process_point_cloud("Global_Stitched_20240101.ply", visualize=True)
    print(f"Output length: {len(result)}")
