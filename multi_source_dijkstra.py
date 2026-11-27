import heapq

# ==============================================================================
# 1. DỮ LIỆU MẠNG LƯỚI GIAO THÔNG 28 ĐỈNH - 50 CẠNH - 4 BỆNH VIỆN (NHÓM 3)
#    (Tự động import từ graph_data.py nếu đặt chung thư mục)
#       Chạy độc lập thì dùng bộ dữ liệu 28 đỉnh đc tích hợp sẵn
# ==============================================================================

try:
    from graph_data import NODES, EDGES, HOSPITALS, build_adjacency
except ImportError:
    NODES = [
        ("BV Đa khoa Trung tâm", "BV", 5.0, 4.0),       # 0
        ("BV Nhân dân Đông", "BV", 12.0, 4.5),          # 1
        ("BV Quốc tế Tây", "BV", 0.8, 4.5),             # 2
        ("BV Cấp cứu Bắc", "BV", 6.0, 9.0),             # 3
        ("Ngã tư Trung tâm", "DD", 5.0, 5.5),           # 4
        ("Chợ Trung tâm", "DD", 4.0, 2.5),              # 5
        ("Cầu Cũ", "DD", 6.5, 3.5),                     # 6
        ("KDC Sao Mai", "DD", 7.5, 3.0),                # 7
        ("Ngã ba Sao Mai", "DD", 9.0, 4.0),             # 8
        ("Nút giao Đông", "DD", 10.5, 6.0),             # 9
        ("Bến xe Phía Đông", "DD", 10.5, 2.5),          # 10
        ("KCN Phía Nam", "DD", 8.0, 1.0),               # 11
        ("Ngã tư Công viên", "DD", 7.0, 5.5),           # 12
        ("Công viên Trung tâm", "DD", 7.0, 7.0),        # 13
        ("Trường ĐH Giao thông", "DD", 8.5, 7.5),       # 14
        ("Ngã ba Bắc", "DD", 3.5, 7.0),                 # 15
        ("TTTM Phía Bắc", "DD", 4.5, 8.0),              # 16
        ("Ga Đường sắt", "DD", 8.5, 9.0),               # 17
        ("Chung cư Hòa Bình", "DD", 2.5, 5.5),          # 18
        ("Trường THPT Nguyễn Trãi", "DD", 2.5, 3.0),    # 19
        ("Ngã tư Tây", "DD", 2.0, 6.5),                 # 20
        ("KĐT Tây Nam", "DD", 1.5, 2.0),                # 21
        ("Cầu Mới", "DD", 6.5, 1.8),                    # 22
        ("Ngã ba Nam", "DD", 5.0, 1.2),                 # 23
        ("Cảng sông", "DD", 11.5, 1.5),                 # 24
        ("Ngã tư Phố Cổ", "DD", 8.5, 5.5),              # 25
        ("Sân vận động", "DD", 3.0, 8.5),               # 26
        ("Khu du lịch Hồ Xanh", "DD", 11.5, 7.5),       # 27
    ]

    EDGES = [
        (0, 4, 1.5, 5, False), (0, 5, 2.0, 8, False), (0, 6, 1.6, 10, False),
        (6, 7, 1.2, 8, False), (6, 12, 2.3, 7, False), (6, 22, 1.9, 5, False),
        (4, 12, 2.2, 6, False), (4, 15, 2.2, 6, False), (4, 18, 2.5, 8, False),
        (12, 13, 1.5, 4, False), (12, 25, 1.5, 5, False), (7, 8, 2.0, 4, False),
        (8, 9, 2.8, 4, False), (9, 1, 2.8, 3, False), (8, 10, 2.4, 6, False),
        (10, 1, 2.8, 5, False), (10, 24, 1.6, 5, False), (24, 1, 3.3, 7, False),
        (25, 8, 1.7, 5, False), (25, 9, 2.2, 4, False), (25, 14, 2.1, 7, False),
        (9, 27, 2.0, 4, False), (27, 1, 3.1, 7, False), (17, 9, 4.0, 5, True),
        (7, 11, 2.3, 6, False), (11, 22, 1.8, 5, False), (22, 23, 1.7, 5, False),
        (5, 23, 1.8, 6, True), (23, 21, 3.8, 9, False), (11, 24, 3.8, 8, False),
        (2, 18, 2.2, 5, False), (2, 20, 2.6, 6, False), (2, 19, 2.3, 7, False),
        (2, 21, 2.9, 8, False), (18, 20, 1.2, 4, False), (18, 19, 2.7, 9, False),
        (19, 21, 1.6, 5, False), (19, 5, 1.7, 6, False), (19, 0, 2.7, 9, False),
        (20, 15, 1.7, 5, False), (3, 13, 2.4, 5, False), (3, 16, 1.9, 4, False),
        (3, 26, 3.3, 6, False), (3, 17, 2.7, 4, False), (13, 14, 1.6, 4, False),
        (13, 16, 2.9, 8, False), (14, 17, 1.6, 4, False), (15, 16, 1.5, 5, False),
        (15, 26, 1.7, 5, False), (5, 4, 3.3, 10, False),
    ]

    HOSPITALS = [0, 1, 2, 3]

    def build_adjacency():
        adj = [[] for _ in NODES]
        for u, v, km, phut, mot_chieu in EDGES:
            adj[u].append((v, phut))
            if not mot_chieu:
                adj[v].append((u, phut))
        return adj


# ==============================================================================
# 2. THUẬT TOÁN DIJKSTRA MIN-HEAP HIỆN TẠI (CHẠY TỪNG BỆNH VIỆN)
# ==============================================================================

try:
    from dijkstra_heap import dijkstra_heap, tim_benh_vien_nhanh_nhat
    # Tự động import file dijkstra_heap.py nếu đặt chung thư mục
except ImportError:
    def dijkstra_heap(adj, start, end=None):
        n = len(adj)
        INF = float('inf')
        dist = [INF] * n
        parent = [-1] * n
        dist[start] = 0
        pq = [(0, start)]

        while pq:
            current_time, u = heapq.heappop(pq)
            if current_time > dist[u]:
                continue
            if end is not None and u == end:
                break
            for v, weight in adj[u]:
                new_time = current_time + weight
                if new_time < dist[v]:
                    dist[v] = new_time
                    parent[v] = u
                    heapq.heappush(pq, (new_time, v))

        if end is None:
            return dist, parent
        if dist[end] == INF:
            return INF, []

        path = []
        curr = end
        while curr != -1:
            path.append(curr)
            curr = parent[curr]
        path.reverse()
        return dist[end], path

    def tim_benh_vien_nhanh_nhat(adj, hospitals, accident_node):
        ket_qua = []
        for h in hospitals:
            time_h, path_h = dijkstra_heap(adj, h, accident_node)
            ket_qua.append({"hospital_id": h, "time": time_h, "path": path_h})
        ket_qua.sort(key=lambda item: item["time"])
        best = ket_qua[0]
        return {
            "best_hospital": best["hospital_id"],
            "min_time": best["time"],
            "best_path": best["path"],
            "all_hospitals": ket_qua
        }


# ==============================================================================
# 3. HƯỚNG MỞ RỘNG: DIJKSTRA ĐA NGUỒN (MULTI-SOURCE DIJKSTRA)
# ==============================================================================

def multi_source_dijkstra(adj, hospitals):
    """
    Chạy Dijkstra đúng 1 lần duy nhất từ đồng thời tất cả K bệnh viện
    để xác định bệnh viện nhanh nhất (origin) và lộ trình tối ưu cho mọi điểm.
    """
    n = len(adj)
    INF = float('inf')
    dist = [INF] * n
    parent = [-1] * n
    origin = [-1] * n
    pq = []

    for h in hospitals:
        dist[h] = 0
        origin[h] = h
        heapq.heappush(pq, (0, h))

    while pq:
        current_time, u = heapq.heappop(pq)
        if current_time > dist[u]:
            continue
        for v, weight in adj[u]:
            new_time = current_time + weight
            if new_time < dist[v]:
                dist[v] = new_time
                parent[v] = u
                origin[v] = origin[u]
                heapq.heappush(pq, (new_time, v))

    return dist, parent, origin


def truy_vet_tu_multi_source(dist, parent, origin, accident_node):
    """Tra cứu ngay bệnh viện tối ưu và lộ trình cho một điểm tai nạn bất kỳ."""
    if dist[accident_node] == float('inf'):
        return None, float('inf'), []
    path = []
    curr = accident_node
    while curr != -1:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return origin[accident_node], dist[accident_node], path


# ==============================================================================
# 4. CHẠY KIỂM THỬ ĐỐI CHIẾU TRÊN 4 ĐIỂM BẪY KHOẢNG CÁCH & TOÀN BỘ 24 ĐỊA ĐIỂM
# ==============================================================================

def format_path(path):
    return " -> ".join(f"{idx}.{NODES[idx][0]}" for idx in path)


def main():
    adj = build_adjacency()
    so_cung = sum(len(ds) for ds in adj)
    print(
        f"Đồ thị hệ thống: {len(NODES)} đỉnh, {len(EDGES)} cạnh ({so_cung} cung có hướng), {len(HOSPITALS)} bệnh viện")
    print("=" * 95)

    # Chạy Multi-source Dijkstra ĐÚNG 1 LẦN cho toàn bản đồ
    dist_ms, parent_ms, origin_ms = multi_source_dijkstra(adj, HOSPITALS)

    # 1. Kiểm thử 4 điểm "bẫy khoảng cách"
    bay_khoang_cach = [
        (7, "BV Đa khoa Trung tâm (2,8 km - 18 phút)"),
        (8, "BV Đa khoa Trung tâm (4,8 km - 21 phút)"),
        (11, "BV Đa khoa Trung tâm (5,1 km - 20 phút)"),
        (12, "BV Đa khoa Trung tâm (3,7 km - 11 phút)"),
    ]

    print("1. ĐỐI CHIẾU KẾT QUẢ TẠI 4 ĐIỂM 'BẪY KHOẢNG CÁCH':")
    for node_id, bv_gan_nhat_km in bay_khoang_cach:
        # Cách 1: Chạy lặp K=4 lần từ từng bệnh viện
        kq_single = tim_benh_vien_nhanh_nhat(adj, HOSPITALS, node_id)

        # Cách 2: Tra cứu từ 1 lần chạy Multi-source Dijkstra
        bv_ms, time_ms, path_ms = truy_vet_tu_multi_source(
            dist_ms, parent_ms, origin_ms, node_id)

        assert kq_single["best_hospital"] == bv_ms, f"Lệch bệnh viện tại đỉnh {node_id}"
        assert kq_single["min_time"] == time_ms, f"Lệch thời gian tại đỉnh {node_id}"
        assert kq_single["best_path"] == path_ms, f"Lệch lộ trình tại đỉnh {node_id}"

        print(f"\n* Hiện trường [{node_id}] {NODES[node_id][0]}:")
        print(f"  - Nếu chọn nhầm theo km : {bv_gan_nhat_km}")
        print(
            f"  - tim_benh_vien_nhanh_nhat (chạy 4 lần): [{kq_single['best_hospital']}] {NODES[kq_single['best_hospital']][0]} ({kq_single['min_time']} phút)")
        print(
            f"  - multi_source_dijkstra    (chạy 1 lần): [{bv_ms}] {NODES[bv_ms][0]} ({time_ms} phút) -> KHỚP 100%")
        print(f"  - Lộ trình tối ưu: {format_path(path_ms)}")

    # 2. Kiểm thử toàn bộ 24 địa điểm tai nạn (đỉnh 4 -> 27)
    print("\n" + "=" * 95)
    print("2. KIỂM TRA CHÉO TOÀN BỘ 24 ĐỊA ĐIỂM TAI NẠN (ĐỈNH 4 -> 27):")
    dem_theo_bv = {h: 0 for h in HOSPITALS}
    for acc_node in range(4, len(NODES)):
        kq_single = tim_benh_vien_nhanh_nhat(adj, HOSPITALS, acc_node)
        bv_ms, time_ms, path_ms = truy_vet_tu_multi_source(
            dist_ms, parent_ms, origin_ms, acc_node)
        assert kq_single["best_hospital"] == bv_ms
        assert kq_single["min_time"] == time_ms
        assert kq_single["best_path"] == path_ms
        dem_theo_bv[bv_ms] += 1

    print("  -> Tất cả 24/24 địa điểm đều khớp tuyệt đối giữa 2 thuật toán!")
    for h in HOSPITALS:
        print(
            f"  -> [{h}] {NODES[h][0]}: nhanh nhất cho {dem_theo_bv[h]} địa điểm")

    # 3. Kiểm tra đường một chiều (Chợ Trung tâm 5 <-> Ngã ba Nam 23)
    t_di, p_di = dijkstra_heap(adj, 5, 23)
    t_ve, p_ve = dijkstra_heap(adj, 23, 5)
    print("\n" + "=" * 95)
    print("3. KIỂM TRA ĐƯỜNG MỘT CHIỀU (5. Chợ Trung tâm <-> 23. Ngã ba Nam):")
    print(f"  - Chiều đi  (5 -> 23): {t_di} phút | {format_path(p_di)}")
    print(f"  - Chiều về (23 -> 5) : {t_ve} phút | {format_path(p_ve)}")


if __name__ == "__main__":
    main()
