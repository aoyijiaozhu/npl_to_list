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
    print("\n正在应用统计离群点移除...")
    nb_neighbors = 20
    std_ratio = 14

    # 核心：ind 是保留下来的点的索引
    _, ind = pcd.remove_statistical_outlier(nb_neighbors=nb_neighbors, std_ratio=std_ratio)

    # 🌟 关键修改：直接从原始 pcd 中按索引提取最终点云
    # 这样能100%继承原有的所有属性（坐标、颜色、法线等），绝不被后续操作污染
    pcd_final = pcd.select_by_index(ind)

    # 提取离群点
    outlier_cloud = pcd.select_by_index(ind, invert=True)
    num_outliers = len(outlier_cloud.points)

    print(f"检测并移除离群点数量: {num_outliers}")
    print(f"干净点云点数: {len(pcd_final.points)}")

    # 4. 可视化结果
    print("\n正在打开可视化窗口...")

    # 可视化1: 原始点云
    print("窗口 1: 原始点云（查看噪点）")
    o3d.visualization.draw_geometries([pcd], window_name="原始点云")

    # 可视化2: 移除的离群点（涂成红色）和内点（绿色）
    if num_outliers > 0:
        # 重新提取一次生成新的独立对象，专门用来涂色显示
        inlier_vis = pcd.select_by_index(ind)
        inlier_vis.paint_uniform_color([0, 1, 0])  # 临时涂成绿色

        outlier_vis = pcd.select_by_index(ind, invert=True)
        outlier_vis.paint_uniform_color([1, 0, 0])  # 临时涂成红色

        print("窗口 2: 移除的离群点（红色），内点（绿色）")
        o3d.visualization.draw_geometries([inlier_vis, outlier_vis], window_name="内点和离群点可视化")
    else:
        print("未检测到离群点。")

    # 可视化3: 干净的点云（最终结果）
    print("窗口 3: 干净的点云（最终结果，保持原有颜色/灰度）")
    o3d.visualization.draw_geometries([pcd_final], window_name="干净点云")

    # 5. 保存干净的点云
    print(f"\n正在保存干净的点云: {output_ply}")
    # 这里保存的就是没有被染色的纯净数据
    o3d.io.write_point_cloud(output_ply, pcd_final)
    print("完成。")


if __name__ == "__main__":
    remove_isolated_outliers("Final_Processed_Batch.ply", "cleaned_cloud.ply")