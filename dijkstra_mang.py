# -*- coding: utf-8 -*-
"""
dijkstra_mang.py  -  Dijkstra dùng MẢNG TUYẾN TÍNH (độ phức tạp O(V^2))
Người thực hiện: Thành viên 3

Ý tưởng: ở mỗi bước, DUYỆT TUYẾN TÍNH mảng dist[] để chọn đỉnh chưa xét có
khoảng cách nhỏ nhất, rồi "nới lỏng" (relax) các cạnh đi ra từ đỉnh đó.
Dữ liệu đồ thị lấy từ graph_data.py (dùng chung với TV4, TV5).

Chạy:  python dijkstra_mang.py
"""
import sys
import graph_data as gd

INF = float("inf")


# ---------------------------------------------------------------------------
# 1. KIỂM TRA DỮ LIỆU ĐỒ THỊ (đủ số lượng, trọng số không âm, liên thông...)
# ---------------------------------------------------------------------------
def kiem_tra_du_lieu(min_dinh=25, min_canh=35, min_bv=4):
    loi = []
    n, m, bv = len(gd.NODES), len(gd.EDGES), gd.danh_sach_benh_vien()
    if n < min_dinh:
        loi.append(f"Thiếu đỉnh: {n} < {min_dinh}")
    if m < min_canh:
        loi.append(f"Thiếu cạnh: {m} < {min_canh}")
    if len(bv) < min_bv:
        loi.append(f"Thiếu bệnh viện: {len(bv)} < {min_bv}")
    seen = set()
    for u, v, km, p, ot in gd.EDGES:
        if not (0 <= u < n and 0 <= v < n):
            loi.append(f"Cạnh ({u},{v}) có đỉnh không tồn tại")
        if u == v:
            loi.append(f"Cạnh ({u},{v}) là khuyên")
        if p < 0:
            loi.append(f"Cạnh ({u},{v}) có trọng số âm: {p}")
        if p <= 0:
            loi.append(f"Cạnh ({u},{v}) có thời gian <= 0")
        key = (min(u, v), max(u, v))
        if key in seen:
            loi.append(f"Cạnh {key} bị trùng")
        seen.add(key)
        # km phải >= khoảng cách đường chim bay giữa 2 đỉnh (cho hợp lý)
        dx = gd.NODES[u][2] - gd.NODES[v][2]
        dy = gd.NODES[u][3] - gd.NODES[v][3]
        if km + 1e-9 < (dx * dx + dy * dy) ** 0.5 - 0.05:
            loi.append(f"Cạnh ({u},{v}): {km} km < khoảng cách đường chim bay")
    # liên thông: từ mỗi bệnh viện phải đến được mọi đỉnh
    adj = gd.build_adjacency()
    for b in bv:
        dist, _ = dijkstra_mang(adj, b)
        chua_den = [gd.ten(i) for i in range(n) if dist[i] == INF]
        if chua_den:
            loi.append(f"Từ {gd.ten(b)} không đến được: {chua_den}")
    return loi


# ---------------------------------------------------------------------------
# 2. DIJKSTRA BẰNG MẢNG TUYẾN TÍNH
# ---------------------------------------------------------------------------
def dijkstra_mang(ke, nguon, dich=None):
    """
    ke    : danh sách kề, ke[u] = [(v, w), ...] nghĩa là đi được u -> v mất w
            (đường một chiều chỉ xuất hiện ở ke[u], không xuất hiện ở ke[v])
    nguon : chỉ số đỉnh xuất phát (bệnh viện)
    dich  : (tuỳ chọn) nếu có thì dừng sớm ngay khi đỉnh dich được chốt
    Trả về (dist, truoc):
        dist[v]  = thời gian ngắn nhất nguon -> v (INF nếu không có đường)
        truoc[v] = đỉnh đứng trước v trên đường ngắn nhất (-1 nếu không có)
    """
    n = len(ke)
    dist = [INF] * n
    truoc = [-1] * n
    da_xet = [False] * n
    dist[nguon] = 0

    for _ in range(n):
        # 1) tìm đỉnh u chưa chốt có dist nhỏ nhất bằng cách quét tuyến tính
        u = -1
        for i in range(n):
            if not da_xet[i] and (u == -1 or dist[i] < dist[u]):
                u = i
        if u == -1 or dist[u] == INF:     # hết đỉnh, hoặc phần còn lại không tới được
            break
        # 2) chốt u
        da_xet[u] = True
        if u == dich:
            break
        # 3) nới lỏng các cạnh đi ra từ u
        for v, w in ke[u]:
            if not da_xet[v] and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                truoc[v] = u
    return dist, truoc


def truy_vet(truoc, nguon, dich):
    """Dựng lại đường đi nguon -> dich từ mảng truoc. Trả về [] nếu không có đường."""
    duong = []
    v = dich
    while v != -1:
        duong.append(v)
        if v == nguon:
            break
        v = truoc[v]
    duong.reverse()
    return duong if duong and duong[0] == nguon else []


# ---------------------------------------------------------------------------
# 3. CHỌN BỆNH VIỆN CÓ THỜI GIAN ĐẾN NHANH NHẤT
# ---------------------------------------------------------------------------
def so_sanh_benh_vien(hien_truong, adj=None):
    """
    Chạy Dijkstra từ MỖI bệnh viện (đồ thị có đường một chiều nên phải xuất phát
    từ bệnh viện -> hiện trường, không đảo chiều). Trả về danh sách
    [(bv, phút, đường_đi)] đã sắp xếp theo thời gian tăng dần.
    """
    adj = adj or gd.build_adjacency()
    kq = []
    for bv in gd.danh_sach_benh_vien():
        dist, parent = dijkstra_mang(adj, bv)
        kq.append((bv, dist[hien_truong], truy_vet(parent, bv, hien_truong)))
    kq.sort(key=lambda t: t[1])
    return kq


def chuoi_duong_di(duong):
    return " -> ".join(gd.ten(i) for i in duong)


def in_ket_qua(ten_hien_truong):
    """In kết quả cho 1 địa điểm tai nạn. Địa điểm không tồn tại -> báo lỗi, KHÔNG dừng chương trình."""
    ht = gd.tim_dinh(ten_hien_truong)
    if ht is None:
        print(f"[LỖI] Địa điểm '{ten_hien_truong}' không tồn tại trong mạng lưới giao thông.")
        return None
    if ht in gd.danh_sach_benh_vien():
        print(f"[LƯU Ý] '{gd.ten(ht)}' là bệnh viện, hãy nhập địa điểm xảy ra tai nạn.")
        return None
    kq = so_sanh_benh_vien(ht)
    print(f"\n=== Hiện trường: {gd.ten(ht)} ===")
    for bv, phut, duong in kq:
        print(f"  {gd.ten(bv):<22} {phut:>3} phút | {len(duong)-1} chặng | {tong_km(duong):>4} km | {chuoi_duong_di(duong)}")
    best = kq[0]
    print(f"  => ĐỀ XUẤT: {gd.ten(best[0])} - {best[1]} phút")
    return kq


# ---------------------------------------------------------------------------
# 4. CHẠY THỬ
# ---------------------------------------------------------------------------
def tong_km(duong):
    d = 0
    cap = {}
    for u, v, km, p, ot in gd.EDGES:
        cap[(u, v)] = km
        if not ot:
            cap[(v, u)] = km
    for a, b in zip(duong, duong[1:]):
        d += cap[(a, b)]
    return round(d, 1)


def demo_bay_khoang_cach(ten_hien_truong="KDC Sao Mai"):
    ht = gd.tim_dinh(ten_hien_truong)
    adj_t, adj_km, adj_h = gd.build_adjacency(), gd.build_adjacency_km(), gd.build_adjacency_hops()
    print(f"\n######## TÌNH HUỐNG BẪY KHOẢNG CÁCH: hiện trường = {gd.ten(ht)} ########")
    print(f"{'Bệnh viện':<22}{'Chim bay (km)':>14}{'Số chặng':>10}{'Đường ngắn nhất (km)':>22}{'THỜI GIAN (phút)':>18}")
    hang = []
    for bv in gd.danh_sach_benh_vien():
        dt, pt = dijkstra_mang(adj_t, bv)
        dk, _ = dijkstra_mang(adj_km, bv)
        dh, _ = dijkstra_mang(adj_h, bv)
        dx = gd.NODES[bv][2] - gd.NODES[ht][2]
        dy = gd.NODES[bv][3] - gd.NODES[ht][3]
        chim_bay = (dx * dx + dy * dy) ** 0.5
        hang.append((gd.ten(bv), chim_bay, dh[ht], dk[ht], dt[ht], truy_vet(pt, bv, ht)))
    for ten_bv, cb, h, k, t, _ in sorted(hang, key=lambda r: r[4]):
        print(f"{ten_bv:<22}{cb:>14.1f}{int(h):>10}{k:>22.1f}{int(t):>18}")
    gan_nhat = min(hang, key=lambda r: r[3])
    nhanh_nhat = min(hang, key=lambda r: r[4])
    print(f"\n-> Bệnh viện GẦN nhất (theo km đường đi): {gan_nhat[0]} ({gan_nhat[3]:.1f} km, {int(gan_nhat[4])} phút)")
    print(f"-> Bệnh viện ĐẾN NHANH nhất (theo phút)   : {nhanh_nhat[0]} ({nhanh_nhat[3]:.1f} km, {int(nhanh_nhat[4])} phút)")
    if gan_nhat[0] != nhanh_nhat[0]:
        print(f"=> BẪY KHOẢNG CÁCH XẢY RA: gần hơn nhưng chậm hơn {int(gan_nhat[4] - nhanh_nhat[4])} phút.")
    return hang


def bang_tat_ca_hien_truong():
    """Với mọi địa điểm (không phải bệnh viện): BV nhanh nhất theo phút, BV gần nhất theo km, có bẫy không."""
    adj_t, adj_km = gd.build_adjacency(), gd.build_adjacency_km()
    ds_bv = gd.danh_sach_benh_vien()
    dt = {b: dijkstra_mang(adj_t, b)[0] for b in ds_bv}
    dk = {b: dijkstra_mang(adj_km, b)[0] for b in ds_bv}
    print("\n######## BẢNG TỔNG HỢP CHO MỌI ĐỊA ĐIỂM ########")
    print(f"{'Hiện trường':<26}{'BV nhanh nhất (phút)':<30}{'BV gần nhất (km)':<30}{'Bẫy?'}")
    so_bay = 0
    for i in range(len(gd.NODES)):
        if i in ds_bv:
            continue
        nhanh = min(ds_bv, key=lambda b: dt[b][i])
        gan = min(ds_bv, key=lambda b: dk[b][i])
        bay = "CÓ" if nhanh != gan else ""
        so_bay += bool(bay)
        print(f"{gd.ten(i):<26}{gd.ten(nhanh) + f' ({int(dt[nhanh][i])}p)':<30}"
              f"{gd.ten(gan) + f' ({dk[gan][i]:.1f}km)':<30}{bay}")
    print(f"Số địa điểm xảy ra bẫy khoảng cách: {so_bay}")


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    print("1) KIỂM TRA DỮ LIỆU")
    loi = kiem_tra_du_lieu()
    print(f"   Số đỉnh: {len(gd.NODES)} | Số cạnh: {len(gd.EDGES)} | Số bệnh viện: {len(gd.danh_sach_benh_vien())}"
          f" | Cạnh một chiều: {sum(1 for e in gd.EDGES if e[4])}")
    print("   -> Dữ liệu HỢP LỆ" if not loi else "   -> LỖI:\n   " + "\n   ".join(loi))

    print("\n2) TÌNH HUỐNG BÌNH THƯỜNG")
    in_ket_qua("Trường ĐH Giao thông")

    print("\n3) TÌNH HUỐNG BẪY KHOẢNG CÁCH")
    demo_bay_khoang_cach("KDC Sao Mai")
    in_ket_qua("KDC Sao Mai")

    print("\n4) KIỂM TRA ĐƯỜNG MỘT CHIỀU (phố chợ: Chợ Trung tâm -> Ngã ba Nam chỉ đi một hướng)")
    adj = gd.build_adjacency()
    a, b = gd.tim_dinh("Chợ Trung tâm"), gd.tim_dinh("Ngã ba Nam")
    for x, y in ((a, b), (b, a)):
        d, par = dijkstra_mang(adj, x)
        print(f"   {gd.ten(x)} -> {gd.ten(y)}: {d[y]} phút | {chuoi_duong_di(truy_vet(par, x, y))}")

    print("\n5) TÌNH HUỐNG LỖI (địa điểm không tồn tại)")
    in_ket_qua("Quảng trường Không Tồn Tại")

    bang_tat_ca_hien_truong()


if __name__ == "__main__":
    main()
