# -*- coding: utf-8 -*-
"""
main.py  -  GIAO DIỆN ĐIỀU KHIỂN TRUNG TÂM VÀ LỰA CHỌN BỆNH VIỆN (Đề tài 9 - Nhóm 3)
Người thực hiện: Thành viên 5

Chương trình tích hợp toàn bộ module của nhóm:
    graph_data.py            (TV3) dữ liệu đồ thị 28 đỉnh - 50 cạnh - 4 bệnh viện
    dijkstra_mang.py         (TV3) Dijkstra mảng tuyến tính O(V^2) + kiểm tra dữ liệu
    dijkstra_heap.py         (TV4) Dijkstra Min-Heap O((V+E)logV) + chọn bệnh viện nhanh nhất
    visualize.py             vẽ lộ trình và biểu đồ benchmark
    save_and_export.py       xuất hình PNG và báo cáo CSV
    benchmark.py             so sánh hiệu năng mảng tuyến tính và Min-Heap
    multi_source_dijkstra.py hướng mở rộng Dijkstra đa nguồn
    negative_weight_demo.py  minh họa Dijkstra sai khi có cạnh âm
    draw_graph.py            vẽ hình 1 (đồ thị) và hình 2 (bẫy khoảng cách)

Chạy:   cd BTL.09
        python main.py           (menu tương tác)
        python main.py --demo    (chạy tự động các kịch bản chính, không cần nhập)
Cần đặt main.py chung thư mục với các file trên. Vẽ hình cần: pip install matplotlib networkx
"""
import sys

import graph_data as gd
import dijkstra_mang as dm
import dijkstra_heap as dh

INF = float("inf")
THUAT_TOAN = {"heap": "Min-Heap O((V+E)logV)", "mang": "Mảng tuyến tính O(V^2)"}


# ---------------------------------------------------------------------------
# 1. TIỆN ÍCH NHẬP / XUẤT
# ---------------------------------------------------------------------------
def doc_dong(thong_bao):
    """Đọc 1 dòng từ bàn phím; Ctrl+D / Ctrl+Z hoặc hết dữ liệu -> trả về None."""
    try:
        return input(thong_bao).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def tieu_de(noi_dung):
    print("\n" + "=" * 78)
    print(noi_dung)
    print("=" * 78)


def in_danh_sach_dia_diem():
    """In danh sách địa điểm có thể xảy ra tai nạn (đỉnh không phải bệnh viện)."""
    ds_bv = set(gd.danh_sach_benh_vien())
    muc = [f"[{i:>2}] {gd.ten(i)}" for i in range(gd.so_dinh()) if i not in ds_bv]
    for k in range(0, len(muc), 2):
        print("   " + "".join(f"{m:<40}" for m in muc[k:k + 2]))


def chon_hien_truong(chuoi):
    """Chuyển chuỗi người dùng nhập (số thứ tự hoặc tên địa điểm) thành chỉ số đỉnh, None nếu không có."""
    if chuoi.isdigit():
        i = int(chuoi)
        return i if 0 <= i < gd.so_dinh() else None
    return gd.tim_dinh(chuoi)


def nhap_hien_truong():
    """Hỏi người dùng địa điểm tai nạn. Trả về chỉ số đỉnh hoặc None (hủy / nhập sai)."""
    print("\nCác địa điểm có thể xảy ra tai nạn:")
    in_danh_sach_dia_diem()
    s = doc_dong("\nNhập TÊN hoặc SỐ THỨ TỰ địa điểm tai nạn (Enter để hủy): ")
    if not s:
        return None
    ht = chon_hien_truong(s)
    if ht is None:
        # dùng lại cách báo lỗi chuẩn của module dijkstra_mang (không làm dừng chương trình)
        dm.in_ket_qua(s)
        return None
    if ht in gd.danh_sach_benh_vien():
        print(f"[LƯU Ý] '{gd.ten(ht)}' là bệnh viện, hãy nhập địa điểm xảy ra tai nạn.")
        return None
    return ht


# ---------------------------------------------------------------------------
# 2. ĐIỀU PHỐI: TÍNH TOÁN BẰNG MIN-HEAP HOẶC MẢNG TUYẾN TÍNH
# ---------------------------------------------------------------------------
def tinh_dieu_phoi(ht, thuat_toan="heap"):
    """
    Trả về dict cùng khuôn với dijkstra_heap.tim_benh_vien_nhanh_nhat():
        best_hospital, min_time, best_path, all_hospitals=[{hospital_id, time, path}, ...]
    Với thuat_toan = "mang" dùng dijkstra_mang (TV3), "heap" dùng dijkstra_heap (TV4).
    """
    adj = gd.build_adjacency()
    ds_bv = gd.danh_sach_benh_vien()
    if thuat_toan == "heap":
        return dh.tim_benh_vien_nhanh_nhat(adj, ds_bv, ht)
    ket_qua = []
    for bv, phut, duong in dm.so_sanh_benh_vien(ht, adj):
        ket_qua.append({"hospital_id": bv, "time": phut, "path": duong})
    ket_qua.sort(key=lambda r: r["time"])
    best = ket_qua[0]
    return {"best_hospital": best["hospital_id"], "min_time": best["time"],
            "best_path": best["path"], "all_hospitals": ket_qua}


def in_bang_dieu_phoi(ht, kq):
    print(f"\n=== Hiện trường: [{ht}] {gd.ten(ht)} ===")
    print(f"{'Bệnh viện':<24}{'Thời gian':>11}{'Chặng':>7}{'Quãng đường':>13}   Lộ trình")
    for it in kq["all_hospitals"]:
        if it["time"] == INF or not it["path"]:
            print(f"{gd.ten(it['hospital_id']):<24}{'-':>11}   Không có đường đi")
            continue
        print(f"{gd.ten(it['hospital_id']):<24}{str(it['time']) + ' phút':>11}"
              f"{len(it['path']) - 1:>7}{dm.tong_km(it['path']):>10} km   {dm.chuoi_duong_di(it['path'])}")
    print(f"\n=> ĐỀ XUẤT: {gd.ten(kq['best_hospital'])} - {kq['min_time']} phút")


def phan_tich_bay(ht):
    """Cảnh báo nếu BV gần nhất theo km khác BV nhanh nhất theo phút (bẫy khoảng cách)."""
    ds_bv = gd.danh_sach_benh_vien()
    adj_t, adj_km = gd.build_adjacency(), gd.build_adjacency_km()
    dt = {b: dh.dijkstra_heap(adj_t, b)[0][ht] for b in ds_bv}
    dk = {b: dh.dijkstra_heap(adj_km, b)[0][ht] for b in ds_bv}
    nhanh = min(ds_bv, key=lambda b: dt[b])
    gan = min(ds_bv, key=lambda b: dk[b])
    if nhanh != gan:
        print(f"[CẢNH BÁO BẪY KHOẢNG CÁCH] {gd.ten(gan)} gần hơn ({dk[gan]:.1f} km) nhưng "
              f"chậm hơn {int(dt[gan] - dt[nhanh])} phút so với {gd.ten(nhanh)} ({dk[nhanh]:.1f} km).")
    else:
        print("[OK] Không có bẫy khoảng cách: bệnh viện gần nhất cũng là bệnh viện nhanh nhất.")


def xuat_ket_qua(ht, kq, bv_chon):
    """Xuất hình PNG và báo cáo CSV cho bệnh viện mà người điều phối đã chọn."""
    chon = next(it for it in kq["all_hospitals"] if it["hospital_id"] == bv_chon)
    # báo cáo CSV: đánh dấu bệnh viện được chọn là "TỐI ƯU NHẤT (ĐƯỢC CHỌN)"
    kq_xuat = dict(kq, best_hospital=bv_chon)
    try:
        from save_and_export import export_comparison_csv, save_route_image
    except ImportError as e:
        print(f"[LỖI] Không nạp được save_and_export/visualize ({e}). Cài: pip install matplotlib networkx")
        return
    export_comparison_csv(gd.NODES, kq_xuat, ht)
    save_route_image(gd.NODES, gd.EDGES, gd.danh_sach_benh_vien(), bv_chon, chon["path"], ht)


def chuc_nang_dieu_phoi(thuat_toan):
    ht = nhap_hien_truong()
    if ht is None:
        return
    kq = tinh_dieu_phoi(ht, thuat_toan)
    print(f"(Thuật toán: Dijkstra {THUAT_TOAN[thuat_toan]})")
    in_bang_dieu_phoi(ht, kq)
    phan_tich_bay(ht)

    # --- LỰA CHỌN BỆNH VIỆN ---
    ds = [it for it in kq["all_hospitals"] if it["time"] != INF and it["path"]]
    print("\nLỰA CHỌN BỆNH VIỆN ĐIỀU XE (Enter = chọn bệnh viện đề xuất):")
    for k, it in enumerate(ds, 1):
        ghi_chu = "  <- đề xuất" if it["hospital_id"] == kq["best_hospital"] else ""
        print(f"   {k}. {gd.ten(it['hospital_id'])} ({it['time']} phút){ghi_chu}")
    s = doc_dong("Chọn số thứ tự (0 = không điều xe): ")
    if s is None or s == "0":
        print("Đã hủy điều xe.")
        return
    if s == "":
        bv_chon = kq["best_hospital"]
    elif s.isdigit() and 1 <= int(s) <= len(ds):
        bv_chon = ds[int(s) - 1]["hospital_id"]
    else:
        print("[LỖI] Lựa chọn không hợp lệ.")
        return
    it = next(x for x in ds if x["hospital_id"] == bv_chon)
    cham = it["time"] - kq["min_time"]
    print(f"\n>> ĐIỀU XE từ {gd.ten(bv_chon)}: {it['time']} phút")
    print(f"   Lộ trình: {dm.chuoi_duong_di(it['path'])}")
    if cham > 0:
        print(f"   [LƯU Ý] Chậm hơn phương án tối ưu {cham} phút.")
    ans = doc_dong("Xuất báo cáo CSV và hình lộ trình PNG? (c/k, mặc định c): ")
    if ans is None or ans.lower() in ("", "c", "co", "có", "y", "yes"):
        xuat_ket_qua(ht, kq, bv_chon)


# ---------------------------------------------------------------------------
# 3. CÁC CHỨC NĂNG KIỂM THỬ / THỰC NGHIỆM (gọi lại module của nhóm)
# ---------------------------------------------------------------------------
def chuc_nang_kiem_tra_du_lieu():
    tieu_de("KIỂM TRA DỮ LIỆU ĐỒ THỊ")
    loi = dm.kiem_tra_du_lieu()
    print(f"Số đỉnh: {len(gd.NODES)} | Số cạnh: {len(gd.EDGES)} | Số bệnh viện: {len(gd.danh_sach_benh_vien())}"
          f" | Cạnh một chiều: {sum(1 for e in gd.EDGES if e[4])}")
    print("-> Dữ liệu HỢP LỆ" if not loi else "-> LỖI:\n   " + "\n   ".join(loi))


def chuc_nang_bay_khoang_cach():
    tieu_de("KỊCH BẢN BẪY KHOẢNG CÁCH (KDC Sao Mai)")
    dm.demo_bay_khoang_cach("KDC Sao Mai")
    dm.in_ket_qua("KDC Sao Mai")


def chuc_nang_bang_tong_hop():
    tieu_de("BẢNG TỔNG HỢP CHO MỌI ĐỊA ĐIỂM")
    dm.bang_tat_ca_hien_truong()


def chuc_nang_mot_chieu():
    tieu_de("KIỂM TRA ĐƯỜNG MỘT CHIỀU (Chợ Trung tâm -> Ngã ba Nam)")
    adj = gd.build_adjacency()
    a, b = gd.tim_dinh("Chợ Trung tâm"), gd.tim_dinh("Ngã ba Nam")
    for x, y in ((a, b), (b, a)):
        t, duong = dh.dijkstra_heap(adj, x, y)
        print(f"   {gd.ten(x)} -> {gd.ten(y)}: {t} phút | {dm.chuoi_duong_di(duong)}")


def chuc_nang_loi():
    tieu_de("KỊCH BẢN LỖI (địa điểm không tồn tại)")
    dm.in_ket_qua("Quảng trường Không Tồn Tại")
    try:
        dh.tim_benh_vien_nhanh_nhat(gd.build_adjacency(), gd.danh_sach_benh_vien(), 999)
    except ValueError as e:
        print(f"[LỖI bắt được ở tầng thuật toán] {e}")


def chuc_nang_benchmark():
    tieu_de("SO SÁNH HIỆU NĂNG: MẢNG TUYẾN TÍNH vs MIN-HEAP")
    print("(Đồ thị 5.000 đỉnh chạy mảng tuyến tính khá lâu, vui lòng chờ...)")
    import benchmark
    ket_qua = benchmark.run_benchmark()
    try:
        from visualize import plot_benchmark_chart
        plot_benchmark_chart(ket_qua, save_path="benchmark_comparison.png", show_plot=False)
        print("[OK] Đã lưu biểu đồ: benchmark_comparison.png")
    except ImportError as e:
        print(f"[LƯU Ý] Bỏ qua vẽ biểu đồ ({e}). Cài: pip install matplotlib networkx")


def chuc_nang_multi_source():
    tieu_de("HƯỚNG MỞ RỘNG: MULTI-SOURCE DIJKSTRA")
    import multi_source_dijkstra as ms
    ms.main()


def chuc_nang_ve_hinh():
    tieu_de("VẼ HÌNH MINH HỌA (draw_graph.py)")
    try:
        import draw_graph
        draw_graph.hinh1()
        draw_graph.hinh2("KDC Sao Mai")
    except ImportError as e:
        print(f"[LỖI] Không vẽ được hình ({e}). Cài: pip install matplotlib networkx")


def chuc_nang_trong_so_am():
    tieu_de("MINH HỌA: DIJKSTRA SAI KHI CÓ TRỌNG SỐ ÂM")
    import negative_weight_demo
    negative_weight_demo.main()


def chuc_nang_xuat_du_lieu():
    tieu_de("XUẤT DỮ LIỆU ĐỒ THỊ RA JSON / CSV")
    gd.xuat_json()
    gd.xuat_csv()
    print("[OK] Đã xuất graph_data.json, nodes.csv, edges.csv")


# ---------------------------------------------------------------------------
# 4. MENU CHÍNH
# ---------------------------------------------------------------------------
def in_menu(thuat_toan):
    print("\n" + "#" * 78)
    print("   HỆ THỐNG ĐIỀU PHỐI XE CỨU THƯƠNG - NHÓM 3 (ĐỀ TÀI 9)")
    print(f"   Thuật toán đang dùng: Dijkstra {THUAT_TOAN[thuat_toan]}")
    print("#" * 78)
    print("  1. Điều phối xe cứu thương (nhập hiện trường -> chọn bệnh viện)")
    print("  2. Đổi thuật toán (Min-Heap <-> Mảng tuyến tính)")
    print("  3. Kiểm tra dữ liệu đồ thị")
    print("  4. Kịch bản bẫy khoảng cách")
    print("  5. Bảng tổng hợp cho mọi địa điểm")
    print("  6. Kiểm tra đường một chiều")
    print("  7. Kịch bản lỗi (địa điểm không tồn tại)")
    print("  8. So sánh hiệu năng (benchmark)")
    print("  9. Multi-source Dijkstra (hướng mở rộng)")
    print(" 10. Vẽ hình minh họa đồ thị")
    print(" 11. Minh họa trọng số âm làm Dijkstra sai")
    print(" 12. Xuất dữ liệu đồ thị (JSON/CSV)")
    print("  0. Thoát")


def chay_demo():
    """Chạy tự động các kịch bản chính, không cần nhập liệu (dùng cho báo cáo / kiểm thử)."""
    chuc_nang_kiem_tra_du_lieu()
    tieu_de("TÌNH HUỐNG BÌNH THƯỜNG (Trường ĐH Giao thông) - Min-Heap")
    ht = gd.tim_dinh("Trường ĐH Giao thông")
    in_bang_dieu_phoi(ht, tinh_dieu_phoi(ht, "heap"))
    phan_tich_bay(ht)
    tieu_de("TÌNH HUỐNG BẪY KHOẢNG CÁCH (KDC Sao Mai) - Min-Heap và Mảng phải cho cùng kết quả")
    ht = gd.tim_dinh("KDC Sao Mai")
    k1, k2 = tinh_dieu_phoi(ht, "heap"), tinh_dieu_phoi(ht, "mang")
    in_bang_dieu_phoi(ht, k1)
    phan_tich_bay(ht)
    khop = k1["best_hospital"] == k2["best_hospital"] and k1["min_time"] == k2["min_time"]
    print("Đối chiếu 2 thuật toán:", "KHỚP" if khop else "LỆCH")
    chuc_nang_mot_chieu()
    chuc_nang_loi()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "--demo" in sys.argv:
        chay_demo()
        return

    thuat_toan = "heap"
    hanh_dong = {
        "3": chuc_nang_kiem_tra_du_lieu, "4": chuc_nang_bay_khoang_cach,
        "5": chuc_nang_bang_tong_hop, "6": chuc_nang_mot_chieu, "7": chuc_nang_loi,
        "8": chuc_nang_benchmark, "9": chuc_nang_multi_source, "10": chuc_nang_ve_hinh,
        "11": chuc_nang_trong_so_am, "12": chuc_nang_xuat_du_lieu,
    }
    while True:
        in_menu(thuat_toan)
        lc = doc_dong("Chọn chức năng: ")
        if lc is None or lc == "0":
            print("Tạm biệt!")
            break
        if lc == "1":
            chuc_nang_dieu_phoi(thuat_toan)
        elif lc == "2":
            thuat_toan = "mang" if thuat_toan == "heap" else "heap"
            print(f"Đã chuyển sang Dijkstra {THUAT_TOAN[thuat_toan]}")
        elif lc in hanh_dong:
            hanh_dong[lc]()
        else:
            print("[LỖI] Lựa chọn không hợp lệ, hãy nhập số từ 0 đến 12.")


if __name__ == "__main__":
    main()