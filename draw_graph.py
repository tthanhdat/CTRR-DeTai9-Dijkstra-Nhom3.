# -*- coding: utf-8 -*-
"""
draw_graph.py - Vẽ đồ thị minh họa mạng lưới giao thông (dùng matplotlib)
Tạo 2 ảnh:  hinh1_do_thi.png  và  hinh2_bay_khoang_cach.png
Chạy:  python draw_graph.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D

import graph_data as gd
import dijkstra_mang as da

MAU_BV = "#C0392B"       # bệnh viện
MAU_DD = "#2E6DA4"       # địa điểm / giao lộ
MAU_BAY = "#E67E22"      # đường tới BV "gần" (bẫy)
MAU_NHANH = "#1E8449"    # đường tới BV nhanh nhất
MAU_HT = "#F1C40F"       # hiện trường

plt.rcParams["font.family"] = "DejaVu Sans"

# Vị trí đặt nhãn tên đỉnh (dx, dy, căn lề) để tránh chồng chéo
LABEL_OFFSET = {
    0: (0.3, 0.3, "left"), 1: (0.3, 0.0, "left"), 2: (-0.3, 0.0, "right"), 3: (0.0, 0.6, "center"),
    4: (0.2, 0.28, "left"), 5: (-0.2, -0.38, "center"), 6: (-0.2, -0.3, "right"), 7: (0.25, -0.18, "left"),
    8: (-0.2, 0.3, "right"), 9: (-0.25, 0.28, "right"), 10: (-0.25, -0.2, "right"), 11: (0.0, -0.42, "center"),
    12: (-0.2, -0.3, "right"), 13: (0.25, -0.3, "left"), 14: (-0.25, 0.3, "right"), 15: (-0.2, 0.25, "right"),
    16: (-0.1, 0.45, "center"), 17: (0.0, 0.38, "center"), 18: (0.15, 0.32, "left"), 19: (-0.25, 0.0, "right"),
    20: (-0.2, 0.25, "right"), 21: (0.0, -0.45, "center"), 22: (0.0, -0.42, "center"), 23: (0.0, -0.42, "center"),
    24: (0.0, -0.42, "center"), 25: (-0.12, -0.4, "right"), 26: (0.0, 0.45, "center"), 27: (0.0, 0.45, "center"),
}


def nhan(ten):
    """Ngắt dòng tên dài để nhãn gọn, đỡ chồng lên cạnh."""
    t = ten.split()
    if ten.startswith("BV "):
        return " ".join(t[:3]) + "\n" + " ".join(t[3:])
    if len(ten) > 14:
        k = len(t) // 2 if len(t) > 3 else 2
        return " ".join(t[:k]) + "\n" + " ".join(t[k:])
    return ten


def ve_nen(ax, lam_mo=False):
    """Vẽ cạnh + đỉnh. lam_mo=True: vẽ mờ để làm nổi bật đường đi."""
    alpha = 0.35 if lam_mo else 1.0
    for u, v, km, p, ot in gd.EDGES:
        x1, y1 = gd.NODES[u][2], gd.NODES[u][3]
        x2, y2 = gd.NODES[v][2], gd.NODES[v][3]
        if ot:
            ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=16,
                                         color="#555555", lw=1.6, alpha=alpha, shrinkA=9, shrinkB=9, zorder=1))
        else:
            ax.plot([x1, x2], [y1, y2], color="#9AA5B1", lw=1.4, alpha=alpha, zorder=1)
        if not lam_mo:
            ax.text((x1 + x2) / 2, (y1 + y2) / 2, str(p), fontsize=8, ha="center", va="center",
                    color="#222222", zorder=7,
                    bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="#C8CED6", lw=0.5))
    for i, (ten, loai, x, y) in enumerate(gd.NODES):
        if loai == "BV":
            ax.scatter([x], [y], s=520, c=MAU_BV, marker="s", edgecolors="white", linewidths=1.5, zorder=8)
        else:
            ax.scatter([x], [y], s=300, c=MAU_DD, marker="o", edgecolors="white", linewidths=1.2, zorder=8)
        ax.text(x, y, str(i), color="white", fontsize=8, fontweight="bold", ha="center", va="center", zorder=9)
        dx, dy, ha = LABEL_OFFSET[i]
        ax.text(x + dx, y + dy, nhan(ten), fontsize=8.6 if loai == "DD" else 9.2,
                fontweight="bold" if loai == "BV" else "normal", ha=ha, va="center", zorder=6,
                color=MAU_BV if loai == "BV" else "#1B2631",
                bbox=dict(boxstyle="round,pad=0.08", fc="white", ec="none", alpha=0.85))
    ax.set_xlim(-0.9, 13.9)
    ax.set_ylim(-1.45, 10.0)
    ax.set_aspect("equal")
    ax.axis("off")


def ve_duong(ax, duong, mau, lw, style="-", z=3.5):
    for a, b in zip(duong, duong[1:]):
        ax.plot([gd.NODES[a][2], gd.NODES[b][2]], [gd.NODES[a][3], gd.NODES[b][3]],
                color=mau, lw=lw, ls=style, solid_capstyle="round", zorder=z)


def hinh1():
    fig, ax = plt.subplots(figsize=(15, 10.2))
    ve_nen(ax)
    chu_thich = [
        Line2D([0], [0], marker="s", color="w", markerfacecolor=MAU_BV, markersize=13, label="Bệnh viện (4)"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor=MAU_DD, markersize=10, label="Địa điểm / giao lộ (24)"),
        Line2D([0], [0], color="#9AA5B1", lw=2, label="Đường hai chiều (số = thời gian, phút)"),
        Line2D([0], [0], color="#555555", lw=2, marker=">", markersize=7, label="Đường một chiều"),
    ]
    ax.legend(handles=chu_thich, loc="lower center", ncol=2, fontsize=10, frameon=True, framealpha=0.95)
    ax.set_title(f"Hình 1. Mạng lưới giao thông mô phỏng: {len(gd.NODES)} đỉnh, {len(gd.EDGES)} cạnh, "
                 f"{len(gd.danh_sach_benh_vien())} bệnh viện (trọng số = thời gian di chuyển, phút)",
                 fontsize=12, pad=8)
    fig.tight_layout()
    fig.savefig("hinh1_do_thi.png", dpi=170)
    plt.close(fig)


def hinh2(ten_ht="KDC Sao Mai"):
    ht = gd.tim_dinh(ten_ht)
    kq = da.so_sanh_benh_vien(ht)
    nhanh = kq[0]
    gan = min(kq, key=lambda t: da.tong_km(t[2]))      # bệnh viện gần nhất theo km của đường đi
    fig, ax = plt.subplots(figsize=(15, 10.2))
    ve_nen(ax, lam_mo=False)
    # làm mờ nền bằng lớp trắng trong suốt
    ax.add_patch(plt.Rectangle((-0.9, -1.45), 14.8, 11.45, fc="white", alpha=0.5, zorder=3.2))
    ve_duong(ax, gan[2], MAU_BAY, 5.5, "--", 3.6)
    ve_duong(ax, nhanh[2], MAU_NHANH, 6.5, "-", 3.7)
    x, y = gd.NODES[ht][2], gd.NODES[ht][3]
    ax.scatter([x], [y], s=1100, c=MAU_HT, marker="*", edgecolors="black", linewidths=1.2, zorder=10)
    ax.text(x + 0.25, y - 0.72, "HIỆN TRƯỜNG\nTAI NẠN", fontsize=9.5, fontweight="bold", ha="left", zorder=11,
            bbox=dict(boxstyle="round,pad=0.25", fc=MAU_HT, ec="black", lw=0.8))
    h_gan = f"{gd.ten(gan[0])}\n{len(gan[2])-1} chặng · {da.tong_km(gan[2])} km · {gan[1]} phút"
    h_nhanh = f"{gd.ten(nhanh[0])}\n{len(nhanh[2])-1} chặng · {da.tong_km(nhanh[2])} km · {nhanh[1]} phút  (NHANH NHẤT)"
    ax.text(0.0, -0.45, "Gần hơn (ít chặng, ít km) nhưng CHẬM HƠN:\n" + h_gan, fontsize=10, color="white",
            va="top", zorder=11, bbox=dict(boxstyle="round,pad=0.5", fc=MAU_BAY, ec="none"))
    ax.text(6.4, -0.45, "Xa hơn nhưng ĐẾN NHANH HƠN:\n" + h_nhanh, fontsize=10, color="white",
            va="top", zorder=11, bbox=dict(boxstyle="round,pad=0.5", fc=MAU_NHANH, ec="none"))
    ax.set_title(f"Hình 2. Tình huống bẫy khoảng cách tại «{ten_ht}»: bệnh viện gần hơn chưa chắc đến nhanh hơn",
                 fontsize=12, pad=8)
    fig.tight_layout()
    fig.savefig("hinh2_bay_khoang_cach.png", dpi=170)
    plt.close(fig)


if __name__ == "__main__":
    hinh1()
    hinh2()
    print("Đã tạo hinh1_do_thi.png và hinh2_bay_khoang_cach.png")
