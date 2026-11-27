# -*- coding: utf-8 -*-
"""
graph_data.py  -  DỮ LIỆU ĐỒ THỊ GIAO THÔNG MÔ PHỎNG (Đề tài 9)
Người thực hiện: Thành viên 3

Định dạng dữ liệu dùng chung cho TV3 / TV4 / TV5:
  - Đỉnh được đánh số nguyên 0 .. N-1  (N = số đỉnh)
  - NODES[i] = (tên, loại, x_km, y_km)    loại: "BV" (bệnh viện) hoặc "DD" (địa điểm/giao lộ)
  - EDGES    = [(u, v, km, phút, một_chiều), ...]
        km      : chiều dài đoạn đường (chỉ dùng để minh họa bẫy khoảng cách)
        phút    : TRỌNG SỐ của cạnh = thời gian di chuyển của xe cứu thương
        một_chiều: True  -> chỉ đi được từ u đến v
                   False -> đi được cả hai chiều
  - build_adjacency() trả về danh sách kề:  adj[u] = [(v, phút), ...]
    (cạnh hai chiều được thêm vào cả adj[u] và adj[v]; cạnh một chiều chỉ thêm adj[u])

Toàn bộ trọng số dùng cho Dijkstra là THỜI GIAN (phút), không âm.
"""

# ---------------------------------------------------------------------------
# 1. DANH SÁCH ĐỈNH:  (tên, loại, x_km, y_km)
# ---------------------------------------------------------------------------
NODES = [
    # --- 4 bệnh viện (đỉnh 0..3) ---
    ("BV Đa khoa Trung tâm",   "BV", 5.0, 4.0),    # 0
    ("BV Nhân dân Đông",       "BV", 12.0, 4.5),   # 1
    ("BV Quốc tế Tây",         "BV", 0.8, 4.5),    # 2
    ("BV Cấp cứu Bắc",         "BV", 6.0, 9.0),    # 3
    # --- địa điểm / giao lộ (đỉnh 4..27) ---
    ("Ngã tư Trung tâm",       "DD", 5.0, 5.5),    # 4
    ("Chợ Trung tâm",          "DD", 4.0, 2.5),    # 5
    ("Cầu Cũ",                 "DD", 6.5, 3.5),    # 6
    ("KDC Sao Mai",            "DD", 7.5, 3.0),    # 7   <- hiện trường "bẫy khoảng cách"
    ("Ngã ba Sao Mai",         "DD", 9.0, 4.0),    # 8
    ("Nút giao Đông",          "DD", 10.5, 6.0),   # 9
    ("Bến xe Phía Đông",       "DD", 10.5, 2.5),   # 10
    ("KCN Phía Nam",           "DD", 8.0, 1.0),    # 11
    ("Ngã tư Công viên",       "DD", 7.0, 5.5),    # 12
    ("Công viên Trung tâm",    "DD", 7.0, 7.0),    # 13
    ("Trường ĐH Giao thông",   "DD", 8.5, 7.5),    # 14
    ("Ngã ba Bắc",             "DD", 3.5, 7.0),    # 15
    ("TTTM Phía Bắc",          "DD", 4.5, 8.0),    # 16
    ("Ga Đường sắt",           "DD", 8.5, 9.0),    # 17
    ("Chung cư Hòa Bình",      "DD", 2.5, 5.5),    # 18
    ("Trường THPT Nguyễn Trãi", "DD", 2.5, 3.0),   # 19
    ("Ngã tư Tây",             "DD", 2.0, 6.5),    # 20
    ("KĐT Tây Nam",            "DD", 1.5, 2.0),    # 21
    ("Cầu Mới",                "DD", 6.5, 1.8),    # 22
    ("Ngã ba Nam",             "DD", 5.0, 1.2),    # 23
    ("Cảng sông",              "DD", 11.5, 1.5),   # 24
    ("Ngã tư Phố Cổ",          "DD", 8.5, 5.5),    # 25
    ("Sân vận động",           "DD", 3.0, 8.5),    # 26
    ("Khu du lịch Hồ Xanh",    "DD", 11.5, 7.5),   # 27
]

# ---------------------------------------------------------------------------
# 2. DANH SÁCH CẠNH:  (u, v, km, phút, một_chiều)
#    Trọng số = cột "phút" (thời gian di chuyển thực tế, đã tính tắc đường,
#    cầu hẹp, đại lộ tốc độ cao...)
# ---------------------------------------------------------------------------
EDGES = [
    # ---- Khu trung tâm ----
    (0, 4,   1.5,  5, False),   # BV Đa khoa TT  - Ngã tư Trung tâm
    (0, 5,   2.0,  8, False),   # BV Đa khoa TT  - Chợ Trung tâm (đông đúc)
    (0, 6,   1.6, 10, False),   # BV Đa khoa TT  - Cầu Cũ (đường kẹt xe)   <- cạnh "bẫy"
    (6, 7,   1.2,  8, False),   # Cầu Cũ         - KDC Sao Mai (cầu hẹp)   <- cạnh "bẫy"
    (6, 12,  2.3,  7, False),   # Cầu Cũ         - Ngã tư Công viên
    (6, 22,  1.9,  5, False),   # Cầu Cũ         - Cầu Mới
    (4, 12,  2.2,  6, False),   # Ngã tư TT      - Ngã tư Công viên
    (4, 15,  2.2,  6, False),   # Ngã tư TT      - Ngã ba Bắc
    (4, 18,  2.5,  8, False),   # Ngã tư TT      - Chung cư Hòa Bình
    (12, 13, 1.5,  4, False),   # Ngã tư Công viên - Công viên TT
    (12, 25, 1.5,  5, False),   # Ngã tư Công viên - Ngã tư Phố Cổ
    # ---- Khu Đông (đại lộ tốc độ cao) ----
    (7, 8,   2.0,  4, False),   # KDC Sao Mai    - Ngã ba Sao Mai
    (8, 9,   2.8,  4, False),   # Ngã ba Sao Mai - Nút giao Đông (đại lộ)
    (9, 1,   2.8,  3, False),   # Nút giao Đông  - BV Nhân dân Đông (đại lộ)
    (8, 10,  2.4,  6, False),   # Ngã ba Sao Mai - Bến xe Phía Đông
    (10, 1,  2.8,  5, False),   # Bến xe Phía Đông - BV Nhân dân Đông
    (10, 24, 1.6,  5, False),   # Bến xe Phía Đông - Cảng sông
    (24, 1,  3.3,  7, False),   # Cảng sông      - BV Nhân dân Đông
    (25, 8,  1.7,  5, False),   # Ngã tư Phố Cổ - Ngã ba Sao Mai
    (25, 9,  2.2,  4, False),   # Ngã tư Phố Cổ - Nút giao Đông
    (25, 14, 2.1,  7, False),   # Ngã tư Phố Cổ - Trường ĐH Giao thông
    (9, 27,  2.0,  4, False),   # Nút giao Đông - Khu du lịch Hồ Xanh
    (27, 1,  3.1,  7, False),   # Khu du lịch Hồ Xanh - BV Nhân dân Đông
    (17, 9,  4.0,  5, True),    # Ga Đường sắt -> Nút giao Đông (ĐƯỜNG MỘT CHIỀU)
    # ---- Khu Nam ----
    (7, 11,  2.3,  6, False),   # KDC Sao Mai    - KCN Phía Nam
    (11, 22, 1.8,  5, False),   # KCN Phía Nam   - Cầu Mới
    (22, 23, 1.7,  5, False),   # Cầu Mới        - Ngã ba Nam
    (5, 23,  1.8,  6, True),    # Chợ Trung tâm -> Ngã ba Nam (PHỐ CHỢ MỘT CHIỀU)
    (23, 21, 3.8,  9, False),   # Ngã ba Nam     - KĐT Tây Nam
    (11, 24, 3.8,  8, False),   # KCN Phía Nam   - Cảng sông
    # ---- Khu Tây ----
    (2, 18,  2.2,  5, False),   # BV Quốc tế Tây - Chung cư Hòa Bình
    (2, 20,  2.6,  6, False),   # BV Quốc tế Tây - Ngã tư Tây
    (2, 19,  2.3,  7, False),   # BV Quốc tế Tây - THPT Nguyễn Trãi
    (2, 21,  2.9,  8, False),   # BV Quốc tế Tây - KĐT Tây Nam
    (18, 20, 1.2,  4, False),   # Chung cư HB    - Ngã tư Tây
    (18, 19, 2.7,  9, False),   # Chung cư HB    - THPT Nguyễn Trãi
    (19, 21, 1.6,  5, False),   # THPT Nguyễn Trãi - KĐT Tây Nam
    (19, 5,  1.7,  6, False),   # THPT Nguyễn Trãi - Chợ Trung tâm
    (19, 0,  2.7,  9, False),   # THPT Nguyễn Trãi - BV Đa khoa TT
    (20, 15, 1.7,  5, False),   # Ngã tư Tây     - Ngã ba Bắc
    # ---- Khu Bắc ----
    (3, 13,  2.4,  5, False),   # BV Cấp cứu Bắc - Công viên TT
    (3, 16,  1.9,  4, False),   # BV Cấp cứu Bắc - TTTM Phía Bắc
    (3, 26,  3.3,  6, False),   # BV Cấp cứu Bắc - Sân vận động
    (3, 17,  2.7,  4, False),   # BV Cấp cứu Bắc - Ga Đường sắt (đại lộ)
    (13, 14, 1.6,  4, False),   # Công viên TT   - Trường ĐH Giao thông
    (13, 16, 2.9,  8, False),   # Công viên TT   - TTTM Phía Bắc
    (14, 17, 1.6,  4, False),   # Trường ĐH GT   - Ga Đường sắt
    (15, 16, 1.5,  5, False),   # Ngã ba Bắc     - TTTM Phía Bắc
    (15, 26, 1.7,  5, False),   # Ngã ba Bắc     - Sân vận động
    (5, 4,   3.3, 10, False),   # Chợ Trung tâm  - Ngã tư Trung tâm (đường vòng)
]

# ---------------------------------------------------------------------------
# 3. CÁC HÀM TIỆN ÍCH DÙNG CHUNG
# ---------------------------------------------------------------------------
def so_dinh():
    return len(NODES)


def ten(i):
    return NODES[i][0]


def danh_sach_benh_vien():
    """Trả về danh sách chỉ số các đỉnh là bệnh viện."""
    return [i for i, n in enumerate(NODES) if n[1] == "BV"]


def tim_dinh(ten_dia_diem):
    """Tìm chỉ số đỉnh theo tên (không phân biệt hoa/thường, bỏ khoảng trắng thừa).
    Trả về None nếu địa điểm không tồn tại (để chương trình báo lỗi thay vì bị dừng)."""
    key = " ".join(str(ten_dia_diem).split()).lower()
    for i, n in enumerate(NODES):
        if n[0].lower() == key:
            return i
    return None


def build_adjacency():
    """Danh sách kề: adj[u] = [(v, thời_gian_phút), ...] -- có tính đường một chiều."""
    adj = [[] for _ in NODES]
    for u, v, km, phut, mot_chieu in EDGES:
        adj[u].append((v, phut))
        if not mot_chieu:
            adj[v].append((u, phut))
    return adj


def build_adjacency_km():
    """Danh sách kề với trọng số là KM (chỉ dùng để minh họa bẫy khoảng cách)."""
    adj = [[] for _ in NODES]
    for u, v, km, phut, mot_chieu in EDGES:
        adj[u].append((v, km))
        if not mot_chieu:
            adj[v].append((u, km))
    return adj


def build_adjacency_hops():
    """Danh sách kề với mọi trọng số = 1 (đếm số chặng đường)."""
    adj = [[] for _ in NODES]
    for u, v, km, phut, mot_chieu in EDGES:
        adj[u].append((v, 1))
        if not mot_chieu:
            adj[v].append((u, 1))
    return adj


def build_adjacency_matrix(inf=float("inf")):
    """Ma trận kề (nếu cần): m[u][v] = phút hoặc inf nếu không có đường."""
    n = len(NODES)
    m = [[inf] * n for _ in range(n)]
    for u, v, km, phut, mot_chieu in EDGES:
        m[u][v] = phut
        if not mot_chieu:
            m[v][u] = phut
    return m


def xuat_json(duong_dan="graph_data.json"):
    import json
    data = {
        "nodes": [{"id": i, "name": n[0], "type": n[1], "x": n[2], "y": n[3]}
                  for i, n in enumerate(NODES)],
        "edges": [{"u": u, "v": v, "km": km, "minutes": p, "oneway": ot}
                  for u, v, km, p, ot in EDGES],
    }
    with open(duong_dan, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def xuat_csv(thu_muc="."):
    import csv, os
    with open(os.path.join(thu_muc, "nodes.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["id", "ten_dinh", "loai", "x_km", "y_km"])
        for i, n in enumerate(NODES):
            w.writerow([i, n[0], n[1], n[2], n[3]])
    with open(os.path.join(thu_muc, "edges.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["u", "v", "ten_u", "ten_v", "km", "phut", "mot_chieu"])
        for u, v, km, p, ot in EDGES:
            w.writerow([u, v, NODES[u][0], NODES[v][0], km, p, "x" if ot else ""])


if __name__ == "__main__":
    xuat_json()
    xuat_csv()
    print(f"Số đỉnh: {len(NODES)} | số cạnh: {len(EDGES)} | số bệnh viện: {len(danh_sach_benh_vien())}")
