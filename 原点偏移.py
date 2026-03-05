#原点设置在左下角
import open3d as o3d
import numpy as np


def process_and_save_point_cloud():
    # 1. 读取 PLY 文件 (请确保文件名与你本地的一致)
    file_path = "Cropped_Y_axis.ply"
    print(f"正在读取文件: {file_path}...")
    pcd = o3d.io.read_point_cloud(file_path)

    # 2. 检查数据是否读取成功
    if pcd.is_empty():
        print("读取失败，请检查文件路径或文件是否损坏。")
        return  # 提前结束程序

    print(f"成功加载点云，包含 {len(pcd.points)} 个点。")

    # 3. --- 核心逻辑：重新定义原点 ---
    # 获取所有点的坐标数组
    points = np.asarray(pcd.points)

    # 计算 X 和 Y 的最小值
    min_x = np.min(points[:, 0])
    min_y = np.min(points[:, 1])
    # Z 轴保持不变，所以偏移量设为 0
    offset_z = 0

    print(f"平移前 -> 最小 X: {min_x:.4f}, 最小 Y: {min_y:.4f}")

    # 构造平移向量：把最小点移到原点，需要减去最小值
    translation = [-min_x, -min_y, -offset_z]

    # 执行平移操作
    pcd.translate(translation)

    print("坐标轴原点已重定义：现在的最小 X 和 Y 均为 0")

    # 4. --- 可视化验证 ---
    # 创建一个坐标轴，放在 [0,0,0]，用来观察点云是否对齐到了原点
    mesh_frame = o3d.geometry.TriangleMesh.create_coordinate_frame(size=0.2, origin=[0, 0, 0])

    print("\n正在打开可视化窗口...")
    print("注意：请在确认无误后，手动关闭弹出的可视化窗口，程序才会继续执行保存操作！")

    o3d.visualization.draw_geometries([pcd, mesh_frame],
                                      window_name="重定义原点后的点云 (关闭窗口以继续)",
                                      width=1024, height=768)

    # 5. --- 保存处理后的新文件 ---
    save_path = "Final_Processed_Batch.ply"

    # 保存为默认的二进制格式（体积小、读取快）
    #o3d.io.write_point_cloud(save_path, pcd)

    # 如果你需要用文本编辑器查看坐标，请注释掉上面那行，并取消下面这行的注释：
    o3d.io.write_point_cloud(save_path, pcd, write_ascii=True)

    print(f"\n太棒了，处理后的点云已成功保存至：{save_path}")


# 运行主函数
if __name__ == "__main__":
    process_and_save_point_cloud()