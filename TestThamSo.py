import random
import tkinter as tk
from tkinter import ttk, messagebox

# Dữ liệu đầu vào
mon_hoc = []
giang_vien = []
phong_hoc = []
khoang_thoi_gian = []
ket_qua_chay = []

# Hàm tạo lịch học
def tao_lich():
    lich = []
    used_slots = set()
    for mh in mon_hoc:
        while True:
            gv = random.choice(giang_vien)
            phong = random.choice(phong_hoc)
            tg = random.choice(khoang_thoi_gian)
            key = (mh, phong, tg)
            if key not in used_slots:
                used_slots.add(key)
                lich.append((mh, gv, phong, tg))
                break
    return lich

# Hàm đánh giá lịch học
def danh_gia(lich):
    return len(set((mh, phong, tg) for mh, gv, phong, tg in lich))

# Chọn lọc các cá thể tốt nhất
def chon_loc(quan_the, so_luong):
    return sorted(quan_the, key=lambda x: danh_gia(x), reverse=True)[:so_luong]

# Lai ghép hai lịch học
def lai_ghep(bo_me1, bo_me2):
    diem_cat = len(bo_me1) // 2
    return bo_me1[:diem_cat] + bo_me2[diem_cat:]

# Đột biến ngẫu nhiên một phần của lịch học
def dot_bien(lich, xac_suat_dot_bien):
    if random.random() < xac_suat_dot_bien:
        i = random.randint(0, len(lich) - 1)
        lich[i] = (random.choice(mon_hoc), random.choice(giang_vien), random.choice(phong_hoc), random.choice(khoang_thoi_gian))
    return lich

# Thuật toán di truyền với tham số tùy chỉnh
def thuat_toan_di_truyen(kich_thuoc_quan_the, so_the_he, xac_suat_dot_bien, so_luong_chon_loc):
    if not mon_hoc or not phong_hoc or not khoang_thoi_gian or not giang_vien:
        messagebox.showerror("Lỗi", "Vui lòng nhập đủ dữ liệu trước khi tạo lịch học.")
        return []

    quan_the = [tao_lich() for _ in range(kich_thuoc_quan_the)]
    
    for _ in range(so_the_he):
        quan_the = chon_loc(quan_the, so_luong_chon_loc)
        quan_the_moi = []
        for _ in range(len(quan_the) // 2):
            p1, p2 = random.sample(quan_the, 2)
            con = lai_ghep(p1, p2)
            con = dot_bien(con, xac_suat_dot_bien)
            quan_the_moi.append(con)
        quan_the.extend(quan_the_moi)

    lich_tot_nhat = chon_loc(quan_the, 1)[0]
    so_xung_dot = len(lich_tot_nhat) - danh_gia(lich_tot_nhat)
    chat_luong = (1 - so_xung_dot / len(lich_tot_nhat)) * 100 if len(lich_tot_nhat) > 0 else 0

    # Lưu kết quả
    lan_chay = len(ket_qua_chay) + 1
    ket_qua_chay.append((lan_chay, so_xung_dot, round(chat_luong, 2)))

    return lich_tot_nhat

# Giao diện người dùng
root = tk.Tk()
root.title("Lập Lịch Học Tự Động")

# Khung chính
khung = ttk.Frame(root, padding=10)
khung.grid(row=0, column=0, padx=10, pady=10)

# Ô nhập dữ liệu
entry_mon_hoc = ttk.Entry(khung, width=30)
entry_giang_vien = ttk.Entry(khung, width=30)
entry_phong_hoc = ttk.Entry(khung, width=30)
entry_thoi_gian = ttk.Entry(khung, width=30)

entry_mon_hoc.grid(row=0, column=1, padx=5, pady=5)
entry_giang_vien.grid(row=1, column=1, padx=5, pady=5)
entry_phong_hoc.grid(row=2, column=1, padx=5, pady=5)
entry_thoi_gian.grid(row=3, column=1, padx=5, pady=5)

# Nhãn
ttk.Label(khung, text="Môn học:").grid(row=0, column=0, sticky="w")
ttk.Label(khung, text="Giảng viên:").grid(row=1, column=0, sticky="w")
ttk.Label(khung, text="Phòng học:").grid(row=2, column=0, sticky="w")
ttk.Label(khung, text="Thời gian:").grid(row=3, column=0, sticky="w")

# Hàm thêm dữ liệu
def them_du_lieu():
    mon = entry_mon_hoc.get()
    gv = entry_giang_vien.get()
    phong = entry_phong_hoc.get()
    thoigian = entry_thoi_gian.get()
    
    if mon: mon_hoc.append(mon)
    if gv: giang_vien.append(gv)
    if phong: phong_hoc.append(phong)
    if thoigian: khoang_thoi_gian.append(thoigian)
    
    entry_mon_hoc.delete(0, tk.END)
    entry_giang_vien.delete(0, tk.END)
    entry_phong_hoc.delete(0, tk.END)
    entry_thoi_gian.delete(0, tk.END)

# Nút thêm dữ liệu
btn_them = ttk.Button(khung, text="Thêm dữ liệu", command=them_du_lieu)
btn_them.grid(row=4, column=0, columnspan=2, pady=10)

# Hiển thị lịch học
def hien_thi_lich(lich):
    tree.delete(*tree.get_children())
    for muc in lich:
        tree.insert("", "end", values=muc)

# Nút tạo lịch
def tao_lich_va_hien_thi():
    lich_tot_nhat = thuat_toan_di_truyen(20, 100, 0.1, 10)
    hien_thi_lich(lich_tot_nhat)

btn_tao_lich = ttk.Button(khung, text="Tạo Lịch Học", command=tao_lich_va_hien_thi)
btn_tao_lich.grid(row=5, column=0, columnspan=2, pady=10)

# Bảng hiển thị lịch học
cot = ("Môn học", "Giảng viên", "Phòng học", "Thời gian")
tree = ttk.Treeview(khung, columns=cot, show="headings")
for c in cot:
    tree.heading(c, text=c)
    tree.column(c, width=150)
tree.grid(row=6, column=0, columnspan=2)

# Bảng kết quả từng lần chạy
cot_kq_chay = ("Lần chạy", "Số xung đột", "Chất lượng lịch (%)")
tree_kq_chay = ttk.Treeview(khung, columns=cot_kq_chay, show="headings")
for c in cot_kq_chay:
    tree_kq_chay.heading(c, text=c)
    tree_kq_chay.column(c, width=120)
tree_kq_chay.grid(row=7, column=0, columnspan=2, pady=10)

# Hiển thị kết quả
def hien_thi_ket_qua_chay():
    tree_kq_chay.delete(*tree_kq_chay.get_children())
    for kq in ket_qua_chay:
        tree_kq_chay.insert("", "end", values=kq)

# Nút chạy thuật toán với các bộ tham số khác nhau
def chay_voi_tham_so(kich_thuoc_quan_the, so_the_he, xac_suat_dot_bien, so_luong_chon_loc):
    thuat_toan_di_truyen(kich_thuoc_quan_the, so_the_he, xac_suat_dot_bien, so_luong_chon_loc)
    hien_thi_ket_qua_chay()

# Tạo các nút để chạy với các bộ tham số khác nhau
btn_tham_so1 = ttk.Button(khung, text="Chạy với tham số 1", command=lambda: chay_voi_tham_so(20, 100, 0.1, 10))
btn_tham_so1.grid(row=8, column=0, pady=10)

btn_tham_so2 = ttk.Button(khung, text="Chạy với tham số 2", command=lambda: chay_voi_tham_so(30, 150, 0.2, 15))
btn_tham_so2.grid(row=8, column=1, pady=10)

btn_tham_so3 = ttk.Button(khung, text="Chạy với tham số 3", command=lambda: chay_voi_tham_so(40, 200, 0.3, 20))
btn_tham_so3.grid(row=9, column=0, columnspan=2, pady=10)

root.mainloop()