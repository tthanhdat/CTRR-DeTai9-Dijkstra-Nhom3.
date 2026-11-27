import heapq


def dijkstra_with_trace(graph, start, target):
    """Chạy thuật toán Dijkstra chuẩn (đánh dấu đỉnh đã chốt) và in chi tiết từng bước."""
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    visited = set()
    dist[start] = 0

    print("=== QUÁ TRÌNH CHẠY THUẬT TOÁN DIJKSTRA ===")
    step = 1
    while len(visited) < len(graph):
        # Chọn đỉnh chưa thăm có dist nhỏ nhất
        u = None
        min_d = float('inf')
        for node in graph:
            if node not in visited and dist[node] < min_d:
                min_d = dist[node]
                u = node

        if u is None:
            break

        visited.add(u)
        print(f"Bước {step}: Chọn và CHỐT đỉnh '{u}' (dist[{u}] = {dist[u]})")

        for v, weight in graph[u]:
            if v in visited:
                print(f"   -> Xét cạnh {u} -> {v} (w = {weight}): BỎ QUA vì '{v}' đã bị chốt!")
            else:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    old_dist = dist[v]
                    dist[v] = new_dist
                    prev[v] = u
                    print(f"   -> Cập nhật dist[{v}]: {old_dist} -> {new_dist} (qua {u})")
                else:
                    print(f"   -> Giữ nguyên dist[{v}] = {dist[v]} (không cải thiện)")

        print(f"   Trạng thái dist hiện tại: {dist}")
        print(f"   Tập đỉnh đã chốt (visited): {sorted(list(visited))}\n")
        step += 1

    # Truy vết đường đi
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    path.reverse()

    return dist[target], path


def bellman_ford(graph, start, target):
    """Chạy thuật toán Bellman-Ford để tìm đường đi ngắn nhất chính xác trên đồ thị có cạnh âm."""
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[start] = 0

    vertices = list(graph.keys())
    for _ in range(len(vertices) - 1):
        for u in vertices:
            for v, weight in graph[u]:
                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    prev[v] = u

    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    path.reverse()

    return dist[target], path


def main():
    # Đồ thị có hướng 4 đỉnh A, B, C, D với cạnh âm C -> B = -3
    graph = {
        'A': [('B', 4), ('C', 5)],
        'B': [('D', 2)],
        'C': [('B', -3)],
        'D': []
    }

    start_node = 'A'
    target_node = 'D'

    print("ĐỒ THỊ MẪU 4 ĐỈNH CÓ TRỌNG SỐ ÂM:")
    for u, edges in graph.items():
        for v, w in edges:
            print(f"  {u} -> {v} : trọng số = {w}")
    print("-" * 55)

    dijkstra_cost, dijkstra_path = dijkstra_with_trace(graph, start_node, target_node)
    actual_cost, actual_path = bellman_ford(graph, start_node, target_node)

    print("=== SO SÁNH KẾT QUẢ CUỐI CÙNG ===")
    print(f"1. Kết quả của Dijkstra (SAI) : {' -> '.join(dijkstra_path)} | Tổng chi phí = {dijkstra_cost}")
    print(f"2. Đường đi ngắn nhất thực tế : {' -> '.join(actual_path)} | Tổng chi phí = {actual_cost}")
    print("\nGIẢI THÍCH NGUYÊN NHÂN:")
    print("- Ở Bước 2, vì dist[B] = 4 < dist[C] = 5, Dijkstra chọn và 'chốt' đỉnh B quá sớm.")
    print("- Ở Bước 3, khi xét từ C (dist[C] = 5) qua cạnh âm C -> B (-3), chi phí tới B giảm còn 2.")
    print("- Tuy nhiên, do B đã bị đánh dấu 'đã chốt' (visited), Dijkstra không cập nhật lại B và D,")
    print("  bỏ lỡ lộ trình tối ưu A -> C -> B -> D (chi phí = 4).")


if __name__ == "__main__":
    main()
