import csv
from datetime import datetime
from visualize import plot_ambulance_route


def save_route_image(nodes, edges, hospitals, best_hospital, best_path, accident_node,
                     filename="ket_qua_lo_trinh.png"):
    #Xuất hình ảnh sơ đồ mạng lưới và lộ trình cứu thương tối ưu ra file PNG (300 DPI).
    
    plot_ambulance_route(
        nodes=nodes,
        edges=edges,
        hospitals=hospitals,
        best_hospital=best_hospital,
        best_path=best_path,
        accident_node=accident_node,
        show_plot=False,
        save_path=filename
    )
    print(f"[OK] Đã lưu hình ảnh lộ trình tối ưu tại: {filename}")


def export_comparison_csv(nodes, result_dict, accident_node, filename="bao_cao_dieu_phoi.csv"):
    
    #Xuất bảng so sánh thời gian và lộ trình chi tiết của 4 bệnh viện ra file CSV.
    #result_dict: kết quả trả về từ hàm tim_benh_vien_nhanh_nhat() của TV4.
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    best_hospital = result_dict["best_hospital"]
    all_hospitals = result_dict["all_hospitals"]
    acc_name = nodes[accident_node][0]

    with open(filename, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["BÁO CÁO KẾT QUẢ ĐIỀU PHỐI XE CỨU THƯƠNG"])
        writer.writerow(["Thời gian truy vấn:", timestamp,
                         "Hiện trường tai nạn:", f"[{accident_node}] {acc_name}"])
        writer.writerow([])
        writer.writerow([
            "STT", "Mã BV", "Tên bệnh viện", "Thời gian dự kiến (phút)",
            "Số chặng đi qua", "Lộ trình chi tiết", "Đánh giá"
        ])

        for idx, item in enumerate(all_hospitals, start=1):
            h_id = item["hospital_id"]
            h_name = nodes[h_id][0]
            total_time = item["time"]
            path = item["path"]

            if total_time == float("inf") or not path:
                time_str = "Không có đường đi"
                steps = 0
                path_str = "N/A"
                status = "Không khả dụng"
            else:
                time_str = f"{total_time}"
                steps = len(path) - 1
                path_str = " -> ".join(f"[{p}] {nodes[p][0]}" for p in path)
                status = "TỐI ƯU NHẤT (ĐƯỢC CHỌN)" if h_id == best_hospital else "Dự phòng"

            writer.writerow([idx, h_id, h_name, time_str, steps, path_str, status])

    print(f"[OK] Đã xuất báo cáo điều phối chi tiết ra file: {filename}")
