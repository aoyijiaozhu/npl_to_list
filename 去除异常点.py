#这个版本会把正常点染色成绿色
import open3d as o3d
import numpy as np


def remove_isolated_outliers(input_ply, output_ply):
    """
    加载点云，应用统计离群点移除，并将干净的点云保存到新文件。
    """
    # 1. 加载点云
    print(f"正在加载点云: {input_ply}...")
    pcd = o3d.io.read_point_cloud(input_ply)

    if pcd.is_empty():
        print(f"错误：无法读取或未找到文件: {input_ply}。")
        return

    print(f"原始点数: {len(pcd.points)}")

    # 2. 应用统计离群点移除 (SOR)
    # 这种方法对于去除图像中显示的稀疏噪点非常有效。
    print("\n正在应用统计离群点移除...")

    # nb_neighbors: 考虑每个点的邻居数量。
    # 对于稀疏噪点，nb_neighbors=20 是一个良好的起始值。
    nb_neighbors = 20

    # std_ratio: 移除平均距离大于平均值指定倍数标准差的点。
    # 更小的值会更彻底地移除噪点，但可能会误删除内点。
    # std_ratio=2.0 是一个标准的起始值。
    std_ratio = 14

    # 应用过滤器
    # remove_statistical_outlier 返回两个值：
    # inlier_cloud: 过滤后的干净点云
    # ind: 保留点的索引
    inlier_cloud, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)

    # 3. 提取离群点（仅用于可视化验证）
    outlier_cloud = pcd.select_by_index(ind, invert=True)
    num_outliers = len(outlier_cloud.points)

    print(f"检测并移除离群点数量: {num_outliers}")
    print(f"干净点云点数: {len(inlier_cloud.points)}")

    # 4. 可视化结果（证明离群点已移除）
    print("\n正在打开可视化窗口...")

    # 可视化1: 原始点云（带有明显的噪点）
    print("窗口 1: 原始点云（查看噪点）")
    o3d.visualization.draw_geometries([pcd], window_name="原始点云")

    # 可视化2: 移除的离群点（涂成红色，悬浮在空中）和内点（绿色）
    if num_outliers > 0:
        # 给点云上色以便区分
        inlier_cloud_color = inlier_cloud.paint_uniform_color([0, 1, 0])  # 绿色
        outlier_cloud_color = outlier_cloud.paint_uniform_color([1, 0, 0])  # 红色

        print("窗口 2: 移除的离群点（红色），内点（绿色）")
        o3d.visualization.draw_geometries([inlier_cloud_color, outlier_cloud_color], window_name="内点和离群点可视化")
    else:
        print("未检测到离群点。")

    # 可视化3: 干净的点云（最终结果）
    # 如果给内点上色，我们需要恢复其原始颜色（如果有）。
    # 对于只包含xyz的点云，它们将再次变为灰色。
    # 如果原始点云有颜色，我们需要重新加载内点云。
    pcd_final = inlier_cloud  # 如果原始点云只有xyz，这将显示干净的点云
    if pcd.has_colors():
        # 如果原始点云有颜色，我们根据索引提取内点，以保留颜色
        pcd_final = pcd.select_by_index(ind)

    print("窗口 3: 干净的点云（最终结果）")
    o3d.visualization.draw_geometries([pcd_final], window_name="干净点云")

    # 5. 保存干净的点云
    print(f"\n正在保存干净的点云: {output_ply}")
    o3d.io.write_point_cloud(output_ply, pcd_final)
    print("完成。")


if __name__ == "__main__":
    # 请确保将 'input.ply' 替换为您实际的文件名
    # 如果您的PLY文件只有xyz坐标，则可视化结果将是灰色的点云
    remove_isolated_outliers("Final_Processed_Batch.ply", "cleaned_cloud.ply")