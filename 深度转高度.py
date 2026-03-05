#把深度数据转化为高度数据
import open3d as o3d
import numpy as np

# 1. 读取 PLY 文件
file_path = "Full_Batch_20240101.ply"
pcd = o3d.io.read_point_cloud(file_path)

if pcd.is_empty():
    print("读取失败，请检查文件路径。")
else:
    # --- 核心数据操作 ---

    # 将点云转为 numpy 数组进行数学运算
    points = np.asarray(pcd.points)

    # 获取原始数据的最小值
    min_x = np.min(points[:, 0])
    min_y = np.min(points[:, 1])

    print(f"原始范围: X[{min_x:.3f}], Y[{min_y:.3f}], Z[{np.min(points[:, 2]):.3f} ~ {np.max(points[:, 2]):.3f}]")

    # 执行变换：
    # X = X - min_x (归零)
    # Y = Y - min_y (归零)
    # Z = 2.7 - Z   (反转并偏移)

    points[:, 0] = points[:, 0] - min_x
    points[:, 1] = points[:, 1] - min_y
    points[:, 2] = 2.7 - points[:, 2]

    # 将修改后的数据写回点云对象
    pcd.points = o3d.utility.Vector3dVector(points)

    print(
        f"变换后范围: X[{np.min(points[:, 0]):.3f}], Y[{np.min(points[:, 1]):.3f}], Z[{np.min(points[:, 2]):.3f} ~ {np.max(points[:, 2]):.3f}]")

    # --- 可视化验证 ---
    # 创建原点坐标轴 (RGB: XYZ)
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.5, origin=[0, 0, 0])

    print("\n正在打开可视化窗口...")
    o3d.visualization.draw_geometries([pcd, mesh_frame],
                                      window_name="坐标变换后的点云",
                                      width=1200, height=800)


    o3d.io.write_point_cloud("Transformed_Batch.ply", pcd, write_ascii=True)