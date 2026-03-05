#通过裁剪y轴，把柜体裁去
import open3d as o3d
import numpy as np

# 1. 读取点云文件
file_path = "Transformed_Batch.ply"  # 替换为你的文件路径
pcd = o3d.io.read_point_cloud(file_path)

if pcd.is_empty():
    print("读取失败，请检查文件路径。")
else:
    # --- 请在这里填入你需要的 Y 轴范围 ---
    y1 = 0.4 # 最小 Y 值 (例如左侧柜壁的内侧)
    y2 = 1.3 # 最大 Y 值 (例如右侧柜壁的内侧)
    # ------------------------------------

    print(f"正在裁剪 Y 轴，保留 [{y1}, {y2}] 范围内的点...")

    # 2. 获取点的坐标数组
    points = np.asarray(pcd.points)

    # 3. 找到所有 Y 坐标在 y1 和 y2 之间的点的【索引】
    # points[:, 1] 代表提取所有点的 Y 坐标
    valid_indices = np.where((points[:, 1] >= y1) & (points[:, 1] <= y2))[0]

    # 4. 根据索引直接提取子点云 (Open3D 的内置高效方法)
    pcd_cropped = pcd.select_by_index(valid_indices)

    print(f"裁剪完成！剩余 {len(pcd_cropped.points)} 个点 (原始 {len(pcd.points)} 个点)。")

    # 5. 可视化查看结果
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.5, origin=[0, 0, 0])
    o3d.visualization.draw_geometries([pcd_cropped, mesh_frame],
                                      window_name=f"Y轴裁剪结果 [{y1} 到 {y2}]",
                                      width=1200, height=800)

    # 6. 保存裁剪后的点云 (取消下一行的注释即可保存)
    o3d.io.write_point_cloud("Cropped_Y_axis.ply", pcd_cropped, write_ascii=True)