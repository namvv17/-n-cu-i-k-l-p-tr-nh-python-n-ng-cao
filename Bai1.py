import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def calculate():
    try:
        num1 = int(entry_num1.get())
        num2 = int(entry_num2.get())
        operator = operation.get()
        
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                messagebox.showerror("Error", "Không thể chia cho 0")
                return
            result = num1 / num2
        else:
            messagebox.showerror("Error", "Vui lòng chọn phép tính hợp lệ")
            return
            
        result_label.config(text=f"Kết quả: {result}")
    except ValueError:
        messagebox.showerror("Error", "Vui lòng nhập số hợp lệ")

# Thiết lập giao diện chính
root = tk.Tk()
root.title("Máy tính cơ bản")
root.geometry("400x300")
root.configure(bg="#f7f7f7")

# Căn giữa cửa sổ
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
window_width = 500
window_height = 300
position_top = (screen_height // 2) - (window_height // 2)
position_right = (screen_width // 2) - (window_width // 2)
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

# Khung tiêu đề
title_frame = tk.Frame(root, bg="#4CAF50")
title_frame.pack(fill="x")

title_label = tk.Label(
    title_frame,
    text="Máy tính cơ bản",
    font=("Arial", 20, "bold"),
    bg="#4CAF50",
    fg="white",
    pady=10
)
title_label.pack()

# Khung chính
main_frame = tk.Frame(root, bg="#f7f7f7", padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# Số thứ nhất
tk.Label(main_frame, text="Số thứ nhất:", font=("Arial", 12), bg="#f7f7f7").grid(row=0, column=0, sticky="e", pady=5)
entry_num1 = ttk.Entry(main_frame, font=("Arial", 12), width=15)
entry_num1.grid(row=0, column=1, padx=10, pady=5)

# Số thứ hai
tk.Label(main_frame, text="Số thứ hai:", font=("Arial", 12), bg="#f7f7f7").grid(row=1, column=0, sticky="e", pady=5)
entry_num2 = ttk.Entry(main_frame, font=("Arial", 12), width=15)
entry_num2.grid(row=1, column=1, padx=10, pady=5)

# Phép tính
tk.Label(main_frame, text="Phép tính:", font=("Arial", 12), bg="#f7f7f7").grid(row=2, column=0, sticky="e", pady=5)
operation = tk.StringVar(root)
operation.set("+")
operation_menu = ttk.Combobox(main_frame, textvariable=operation, font=("Arial", 12), width=13, state="readonly")
operation_menu["values"] = ["+", "-", "*", "/"]
operation_menu.grid(row=2, column=1, padx=10, pady=5)

# Nút tính toán
button_frame = tk.Frame(main_frame, bg="#f7f7f7")
button_frame.grid(row=3, column=0, columnspan=2, pady=10)
calc_button = ttk.Button(button_frame, text="Tính toán", command=calculate)
calc_button.pack(ipadx=20, ipady=5)

# Kết quả
result_label = tk.Label(root, text="Kết quả: ", font=("Arial", 14), bg="#f7f7f7", fg="#333")
result_label.pack(pady=10)

# Bổ sung viền cho giao diện
main_frame.config(highlightbackground="#ccc", highlightthickness=1)

# Chạy chương trình
root.mainloop()
