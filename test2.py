import open3d as o3d
import numpy as np

pcd = o3d.io.read_point_cloud("Full_Storage_Batch_20240101.ply")

print(f"1. 点的总数: {len(pcd.points)}")
if len(pcd.points) > 0:
    bounds = pcd.get_axis_aligned_bounding_box()
    print(f"2. 包围盒范围:\n{bounds}")
    print(f"3. 点的前5行数据:\n{np.asarray(pcd.points)[:5]}")