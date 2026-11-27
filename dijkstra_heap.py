import heapq


def dijkstra_heap(adj, start, end=None):
    """
    Tìm đường đi ngắn nhất từ đỉnh start bằng Min-Heap (heapq).

    Tham số:
        adj: Danh sách kề adj[u] = [(v, phut), ...]
        start: Chỉ số đỉnh xuất phát (int)
        end: Chỉ số đỉnh đích (int). Nếu None, trả về toàn bộ mảng (dist, parent).

    Trả về:
        - Nếu end is None: (dist, parent)
        - Nếu có end: (thời_gian_ngắn_nhất, danh_sách_đỉnh_lộ_trình)
    """
    n = len(adj)
    if start < 0 or start >= n:
        raise ValueError(f"Đỉnh xuất phát {start} không hợp lệ!")
    if end is not None and (end < 0 or end >= n):
        raise ValueError(f"Đỉnh đích {end} không hợp lệ!")

    INF = float('inf')
    dist = [INF] * n
    parent = [-1] * n
    dist[start] = 0

    # Hàng đợi ưu tiên lưu cặp (thời_gian_tích_lũy, đỉnh_hiện_tại)
    pq = [(0, start)]

    while pq:
        current_time, u = heapq.heappop(pq)

        # Kỹ thuật xóa lười (Lazy Deletion): bỏ qua bản ghi cũ lỗi thời
        if current_time > dist[u]:
            continue

        # Tối ưu dừng sớm (Early Exit) khi đã chốt xong đỉnh hiện trường
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

    # Truy vết ngược đường đi từ hiện trường (end) về bệnh viện (start)
    path = []
    curr = end
    while curr != -1:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    return dist[end], path


def tim_benh_vien_nhanh_nhat(adj, hospitals, accident_node):
    """
    Chạy Dijkstra từ tất cả các bệnh viện đến hiện trường tai nạn
    (đảm bảo đúng chiều đường một chiều) và đề xuất bệnh viện nhanh nhất.
    """
    n = len(adj)
    if accident_node < 0 or accident_node >= n:
        raise ValueError(f"Mã địa điểm tai nạn '{accident_node}' không tồn tại!")

    ket_qua = []
    for h in hospitals:
        time_h, path_h = dijkstra_heap(adj, h, accident_node)
        ket_qua.append({
            "hospital_id": h,
            "time": time_h,
            "path": path_h
        })

    # Sắp xếp danh sách bệnh viện theo thời gian tiếp cận tăng dần
    ket_qua.sort(key=lambda item: item["time"])
    best = ket_qua[0]

    return {
        "best_hospital": best["hospital_id"],
        "min_time": best["time"],
        "best_path": best["path"],
        "all_hospitals": ket_qua
    }


if __name__ == "__main__":
    # Kiểm thử nhanh trên đồ thị mẫu 5 đỉnh (có đường 1 chiều 1 -> 3)
    sample_adj = [
        [(1, 4), (2, 2)],   # 0: BV Trung tâm
        [(3, 10)],          # 1: BV Đông (1 chiều tới 3 mất 10p)
        [(1, 1), (3, 5)],   # 2: Ngã tư
        [(4, 3)],           # 3: Nút giao
        []                  # 4: Hiện trường tai nạn
    ]
    kq = tim_benh_vien_nhanh_nhat(sample_adj, hospitals=[0, 1], accident_node=4)
    print("Bệnh viện nhanh nhất:", kq["best_hospital"])
    print("Thời gian (phút):", kq["min_time"])
    print("Lộ trình:", kq["best_path"])

    # kiểm thử nên ko bị ảnh hưởng khi ghép code