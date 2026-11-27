import csv
import random
import time
from dijkstra_heap import dijkstra_heap

# ==============================================================================
# 1. HAI PHIÊN BẢN CÀI ĐẶT DIJKSTRA (Dùng chung dữ liệu đồ thị danh sách kề)
# ==============================================================================

def dijkstra_array(graph, start):
    """Cài đặt thuật toán Dijkstra sử dụng mảng tuyến tính - Độ phức tạp O(V^2)."""
    n = len(graph)
    dist = [float('inf')] * n
    prev = [-1] * n
    visited = [False] * n
    dist[start] = 0

    for _ in range(n):
        u = -1
        min_d = float('inf')
        for i in range(n):
            if not visited[i] and dist[i] < min_d:
                min_d = dist[i]
                u = i

        if u == -1:
            break

        visited[u] = True
        for v, weight in graph[u]:
            if not visited[v]:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u

    return dist, prev



# ==============================================================================
# 2. HÀM SINH ĐỒ THỊ NGẪU NHIÊN THEO ĐÚNG SỐ ĐỈNH (V) VÀ SỐ CẠNH (E)
# ==============================================================================

def generate_random_graph(num_vertices, num_edges, seed=42):
    """
    Sinh đồ thị có hướng ngẫu nhiên gồm đúng num_vertices đỉnh và num_edges cạnh,
    trọng số dương (1..30 phút), không trùng lặp cạnh.
    """
    max_edges = num_vertices * (num_vertices - 1)
    if num_edges < num_vertices or num_edges > max_edges:
        raise ValueError(f"Số cạnh E phải nằm trong khoảng [{num_vertices}, {max_edges}]")

    rng = random.Random(seed)
    graph = {i: [] for i in range(num_vertices)}
    existing_edges = set()

    # Tạo chu trình liên thông qua tất cả các đỉnh (num_vertices cạnh)
    for i in range(num_vertices):
        nxt = (i + 1) % num_vertices
        w = rng.randint(1, 30)
        graph[i].append((nxt, w))
        existing_edges.add((i, nxt))

    # Thêm ngẫu nhiên các cạnh còn lại cho đủ đúng num_edges cạnh
    while len(existing_edges) < num_edges:
        u = rng.randrange(num_vertices)
        v = rng.randrange(num_vertices)
        if u != v and (u, v) not in existing_edges:
            w = rng.randint(1, 30)
            graph[u].append((v, w))
            existing_edges.add((u, v))

    return graph, len(existing_edges)


# ==============================================================================
# 3. CHƯƠNG TRÌNH BENCHMARK VÀ XUẤT KẾT QUẢ CSV
# ==============================================================================

def run_benchmark(test_cases=((28, 50), (1000, 4000), (2000, 8000), (5000, 20000)), num_runs=10):
    results = []

    print("=" * 82)
    print(f"{'Số đỉnh (V)':<14} | {'Số cạnh (E)':<13} | {'Mảng tuyến tính (ms)':<22} | {'Min-Heap (ms)':<16} | {'Nhanh hơn':<10}")
    print("=" * 82)

    for v_count, e_target in test_cases:
        graph, e_count = generate_random_graph(v_count, e_target, seed=100 + v_count)

        array_times = []
        heap_times = []

        for run in range(num_runs):
            start_node = run % v_count

            # Đo thời gian Dijkstra Mảng tuyến tính
            t0 = time.perf_counter()
            dist_arr, _ = dijkstra_array(graph, start_node)
            t1 = time.perf_counter()
            array_times.append((t1 - t0) * 1000.0)

            # Đo thời gian Dijkstra Min-Heap
            t2 = time.perf_counter()
            dist_hp, _ = dijkstra_heap(graph, start_node)
            t3 = time.perf_counter()
            heap_times.append((t3 - t2) * 1000.0)

            assert dist_arr == dist_hp, f"Sai lệch kết quả ở V={v_count}, run={run}"

        avg_array_ms = sum(array_times) / num_runs
        avg_heap_ms = sum(heap_times) / num_runs
        speedup = avg_array_ms / avg_heap_ms if avg_heap_ms > 0 else 0

        results.append({
            "So_dinh_V": v_count,
            "So_canh_E": e_count,
            "So_lan_chay": num_runs,
            "Mang_tuyen_tinh_ms": round(avg_array_ms, 4),
            "Min_Heap_ms": round(avg_heap_ms, 4),
            "Ty_le_nhanh_hon": round(speedup, 2)
        })

        print(f"{v_count:<14,} | {e_count:<13,} | {avg_array_ms:<22.4f} | {avg_heap_ms:<16.4f} | {speedup:<8.2f}x")

    print("=" * 82)

    csv_filename = "benchmark_results.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["So_dinh_V", "So_canh_E", "So_lan_chay", "Mang_tuyen_tinh_ms", "Min_Heap_ms", "Ty_le_nhanh_hon"]
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"Đã xuất bảng số liệu thực nghiệm ra file: {csv_filename}")
    return results


if __name__ == "__main__":
    # Gồm mốc đồ thị thực tế của nhóm (28 đỉnh, 50 cạnh) và các đồ thị lớn theo yêu cầu đề tài
    run_benchmark(
        test_cases=((28, 50), (1000, 4000), (2000, 8000), (5000, 20000)),
        num_runs=10
    )
