#显示3D点云
import open3d as o3d

# 1. 读取 PLY 文件
file_path = "Transformed_Batch.ply"
pcd = o3d.io.read_point_cloud(file_path)

# 2. 检查数据是否读取成功
if pcd.is_empty():
    print("读取失败，请检查文件路径或文件是否损坏。")
else:
    print(f"成功加载点云，包含 {len(pcd.points)} 个点。")

    # --- 新增部分：创建坐标轴 ---
    # size 表示坐标轴的长度（单位与你的点云一致，比如 1.0 米）
    # origin 表示坐标轴放置的位置，默认在 [0, 0, 0]
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(
        size=0.5, origin=[0, 0, 0]
    )

    # 3. 可视化
    # 将点云 [pcd] 改为列表 [pcd, mesh_frame]，同时显示两个几何体
    o3d.visualization.draw_geometries([pcd, mesh_frame],
                                      window_name="Open3D 点云 + 坐标轴",
                                      width=1024, height=768)