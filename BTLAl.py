import random
import tkinter as tk
from tkinter import ttk, messagebox

# Dữ liệu đầu vào
mon_hoc = []
giang_vien = []
sinh_vien = {}
phong_hoc = []
khoang_thoi_gian = []

# Mã hóa cá thể
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

# Hàm đánh giá chất lượng lịch học
def danh_gia(lich):
    return len(set((mh, phong, tg) for mh, gv, phong, tg in lich))

# Chọn lọc các cá thể tốt nhất
def chon_loc(quan_the):
    return sorted(quan_the, key=lambda x: danh_gia(x), reverse=True)[:10]

# Lai ghép 
def lai_ghep(bo_me1, bo_me2):
    diem_cat = len(bo_me1) // 2
    return bo_me1[:diem_cat] + bo_me2[diem_cat:]

# Đột biến ngẫu nhiên một phần của lịch học 
def dot_bien(lich):
    if random.random() < 0.1:  # Xác suất đột biến 10%
        i = random.randint(0, len(lich) - 1)
        lich[i] = (random.choice(mon_hoc), random.choice(giang_vien), random.choice(phong_hoc), random.choice(khoang_thoi_gian))
    return lich

# Thuật toán di truyền
def thuat_toan_di_truyen():
    if not mon_hoc or not phong_hoc or not khoang_thoi_gian or not giang_vien:
        messagebox.showerror("Lỗi", "Vui lòng nhập đủ dữ liệu trước khi tạo lịch học.")
        return []
    
    quan_the = [tao_lich() for _ in range(20)]
    
    for _ in range(100):  # 100 thế hệ
        quan_the = chon_loc(quan_the)
        quan_the_moi = []
        for _ in range(len(quan_the) // 2):
            p1, p2 = random.sample(quan_the, 2)
            con = lai_ghep(p1, p2)
            con = dot_bien(con)
            quan_the_moi.append(con)
        quan_the.extend(quan_the_moi)
    
    return chon_loc(quan_the)[0]

# Thêm dữ liệu từ giao diện
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

# Hiển thị lịch học
def hien_thi_lich():
    tree.delete(*tree.get_children())
    lich_tot_nhat = thuat_toan_di_truyen()
    unique_schedule = set()
    for muc in lich_tot_nhat:
        if muc not in unique_schedule:
            unique_schedule.add(muc)
            tree.insert("", "end", values=muc)

# Giao diện người dùng
root = tk.Tk()
root.title("Lập Lịch Học Tự Động")
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

# Nút thêm dữ liệu
btn_them = ttk.Button(khung, text="Thêm dữ liệu", command=them_du_lieu)
btn_them.grid(row=4, column=0, columnspan=2, pady=10)

# Nút tạo lịch
btn_tao_lich = ttk.Button(khung, text="Tạo Lịch Học", command=hien_thi_lich)
btn_tao_lich.grid(row=5, column=0, columnspan=2, pady=10)

# Bảng hiển thị lịch học
cot = ("Môn học", "Giảng viên", "Phòng học", "Thời gian")
tree = ttk.Treeview(khung, columns=cot, show="headings")
for c in cot:
    tree.heading(c, text=c)
    tree.column(c, width=150)
tree.grid(row=6, column=0, columnspan=2)

root.mainloop()
