import networkx as nx
import matplotlib.pyplot as plt


def plot_ambulance_route(nodes, edges, hospitals, best_hospital, best_path, accident_node,
                         show_plot=True, save_path=None):
    #Vẽ mạng lưới giao thông 28 đỉnh - 50 cạnh theo tọa độ thực tế (x, y),
    #phân biệt đường 1 chiều / 2 chiều và tô đỏ lộ trình tối ưu của xe cứu thương.
    
    G = nx.DiGraph()
    for idx, (name, node_type, x, y) in enumerate(nodes):
        G.add_node(idx, name=name, node_type=node_type, pos=(x, y))

    two_way_edges = []
    one_way_edges = []
    edge_labels = {}

    for u, v, km, phut, mot_chieu in edges:
        G.add_edge(u, v, weight=phut)
        edge_labels[(u, v)] = f"{phut}p"
        if mot_chieu:
            one_way_edges.append((u, v))
        else:
            G.add_edge(v, u, weight=phut)
            two_way_edges.append((u, v))

    pos = {idx: (nodes[idx][2], nodes[idx][3]) for idx in range(len(nodes))}

    plt.figure(figsize=(15, 10))

    # 1. Phân loại màu sắc và kích thước các đỉnh
    node_colors = []
    node_sizes = []
    for idx in G.nodes():
        if idx == accident_node:
            node_colors.append("#FF3B30")  # Đỏ tươi: Hiện trường tai nạn
            node_sizes.append(950)
        elif idx == best_hospital:
            node_colors.append("#34C759")  # Xanh lá đậm: Bệnh viện tối ưu
            node_sizes.append(900)
        elif idx in hospitals:
            node_colors.append("#007AFF")  # Xanh dương: Các bệnh viện khác
            node_sizes.append(800)
        else:
            node_colors.append("#E5E5EA")  # Xám nhạt: Giao lộ / Địa điểm
            node_sizes.append(550)

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes,
                           edgecolors="black", linewidths=1.2)

    # Nhãn mã số bên trong đỉnh
    id_labels = {idx: str(idx) for idx in G.nodes()}
    nx.draw_networkx_labels(G, pos, labels=id_labels, font_size=9, font_weight="bold")

    # Nhãn tên địa điểm đặt lệch xuống dưới đỉnh
    name_pos = {idx: (x, y - 0.28) for idx, (x, y) in pos.items()}
    name_labels = {idx: nodes[idx][0] for idx in G.nodes()}
    nx.draw_networkx_labels(G, name_pos, labels=name_labels, font_size=7.5, font_color="#222222")

    # 2. Vẽ cạnh nền: đường 2 chiều (không mũi tên) và đường 1 chiều (có mũi tên đậm)
    nx.draw_networkx_edges(G, pos, edgelist=two_way_edges, edge_color="#B0B0B0",
                           arrows=False, width=1.3, alpha=0.75)
    nx.draw_networkx_edges(G, pos, edgelist=one_way_edges, edge_color="#555555",
                           arrows=True, arrowsize=16, arrowstyle="-|>", width=1.6, alpha=0.9)

    # 3. Tô đỏ đậm lộ trình cứu thương tối ưu (best_path)
    if best_path and len(best_path) > 1:
        path_edges = list(zip(best_path[:-1], best_path[1:]))
        nx.draw_networkx_edges(
            G, pos, edgelist=path_edges, edge_color="#FF2D55",
            arrows=True, arrowsize=20, arrowstyle="-|>", width=3.5
        )

    # 4. Hiển thị trọng số thời gian (phút) trên các tuyến đường
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, label_pos=0.45)

    # Chú thích trực quan (Legend)
    best_bv_name = nodes[best_hospital][0] if best_hospital is not None else "N/A"
    acc_name = nodes[accident_node][0]
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w',
                   label=f'Bệnh viện tối ưu: [{best_hospital}] {best_bv_name}',
                   markerfacecolor='#34C759', markeredgecolor='black', markersize=11),
        plt.Line2D([0], [0], marker='o', color='w', label='Bệnh viện khác',
                   markerfacecolor='#007AFF', markeredgecolor='black', markersize=10),
        plt.Line2D([0], [0], marker='o', color='w',
                   label=f'Hiện trường tai nạn: [{accident_node}] {acc_name}',
                   markerfacecolor='#FF3B30', markeredgecolor='black', markersize=11),
        plt.Line2D([0], [0], color='#FF2D55', lw=3.5, label='Lộ trình tối ưu'),
        plt.Line2D([0], [0], color='#555555', lw=1.6, linestyle='-', label='Đường một chiều (→)')
    ]
    plt.legend(handles=legend_elements, loc="upper left", fontsize=9, framealpha=0.92)
    plt.title(f"MÔ PHỎNG ĐIỀU PHỐI CẤP CỨU ĐẾN [{accident_node}] {acc_name.upper()}",
              fontsize=13.5, fontweight="bold", pad=12)
    plt.axis("off")
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    if show_plot:
        plt.show()
    plt.close()


def plot_benchmark_chart(benchmark_results, save_path="benchmark_comparison.png", show_plot=True):
    
    #Vẽ biểu đồ đường so sánh thời gian chạy trung bình (ms) từ kết quả
    #trả về của hàm run_benchmark() trong benchmark.py (TV2).
    
    sizes = [row["So_dinh_V"] for row in benchmark_results]
    array_times = [row["Mang_tuyen_tinh_ms"] for row in benchmark_results]
    heap_times = [row["Min_Heap_ms"] for row in benchmark_results]

    plt.figure(figsize=(9.5, 5.5))
    plt.plot(sizes, array_times, marker='o', linewidth=2.5, color='#FF3B30',
             label='Dijkstra Mảng tuyến tính O(V²)')
    plt.plot(sizes, heap_times, marker='s', linewidth=2.5, color='#007AFF',
             label='Dijkstra Min-Heap O((V + E) log V)')

    for x, y in zip(sizes, array_times):
        plt.annotate(f"{y:.2f} ms", (x, y), textcoords="offset points",
                     xytext=(0, 8), ha='center', fontsize=8.5, color='#FF3B30')
    for x, y in zip(sizes, heap_times):
        plt.annotate(f"{y:.2f} ms", (x, y), textcoords="offset points",
                     xytext=(0, -14), ha='center', fontsize=8.5, color='#007AFF')

    plt.title("SO SÁNH HIỆU NĂNG: DIJKSTRA MẢNG TUYẾN TÍNH VS MIN-HEAP",
              fontsize=12, fontweight="bold")
    plt.xlabel("Quy mô đồ thị (Số lượng đỉnh V)", fontsize=10.5)
    plt.ylabel("Thời gian thực thi trung bình (ms)", fontsize=10.5)
    plt.xticks(sizes)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(fontsize=10)
    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    if show_plot:
        plt.show()
    plt.close()
