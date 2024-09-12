import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle


class CantileverBeamPlotter:
    def __init__(self, master):
        self.master = master
        master.title("Cantilever Beam Plotter")

        # 創建上方框架用於輸入
        top_frame = ttk.Frame(master)
        top_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # 創建下方框架
        bottom_frame = ttk.Frame(master)
        bottom_frame.grid(
            row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

        # 在上方框架中添加輸入框和標籤
        ttk.Label(top_frame, text="Beam Length:").grid(row=0, column=0, padx=5, pady=5)
        self.length_entry = ttk.Entry(top_frame)
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)
        self.length_entry.insert(0, "10")

        ttk.Label(top_frame, text="Load:").grid(row=0, column=2, padx=5, pady=5)
        self.load_entry = ttk.Entry(top_frame)
        self.load_entry.grid(row=0, column=3, padx=5, pady=5)
        self.load_entry.insert(0, "100")

        ttk.Label(top_frame, text="Radius:").grid(row=0, column=4, padx=5, pady=5)
        self.radius_entry = ttk.Entry(top_frame)
        self.radius_entry.grid(row=0, column=5, padx=5, pady=5)
        self.radius_entry.insert(0, "0.05")

        # 創建按鈕
        self.plot_button = ttk.Button(top_frame, text="Solve", command=self.plot)
        self.plot_button.grid(row=0, column=6, padx=5, pady=5)

        # 在下方框架中創建左側區域用於梁變形圖
        left_frame = ttk.Frame(bottom_frame)
        left_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # 在下方框架中創建右側區域用於斷面圖
        right_frame = ttk.Frame(bottom_frame)
        right_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

        # 創建梁變形圖形和畫布
        self.figure = plt.Figure(figsize=(6, 4))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=left_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 創建截面圖形和畫布
        self.section_figure = plt.Figure(figsize=(4, 4))
        self.section_ax = self.section_figure.add_subplot(111)
        self.section_canvas = FigureCanvasTkAgg(self.section_figure, master=right_frame)
        self.section_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # 設置網格權重
        master.grid_rowconfigure(1, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)
        bottom_frame.grid_rowconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(0, weight=2)
        bottom_frame.grid_columnconfigure(1, weight=1)

        # 綁定調整大小事件
        self.canvas.get_tk_widget().bind("<Configure>", self.on_resize)
        self.section_canvas.get_tk_widget().bind("<Configure>", self.on_section_resize)

        # 初始繪製未變形的梁和截面
        self.plot_undeformed_beam()
        self.plot_section()

    def plot_section(self):
        self.section_ax.clear()
        radius = float(self.radius_entry.get())

        # 繪製圓形截面
        circle = Circle((0, 0), radius, fill=False)
        self.section_ax.add_artist(circle)

        # 設置軸範圍和標籤
        self.section_ax.set_xlim(-radius * 1.2, radius * 1.2)
        self.section_ax.set_ylim(-radius * 1.2, radius * 1.2)
        self.section_ax.set_aspect("equal")
        self.section_ax.set_title("Beam Cross Section")
        self.section_ax.set_xlabel("Width (m)")
        self.section_ax.set_ylabel("Height (m)")

        # 更新畫布
        self.section_canvas.draw()

    def on_section_resize(self, event):
        # 重新繪製截面圖
        self.plot_section()

    def on_resize(self, event):
        # 重新繪製圖形
        self.plot_undeformed_beam()

    def plot_undeformed_beam(self):
        self.ax.clear()
        length = float(self.length_entry.get())

        # 繪製未變形的梁
        self.ax.plot([0, length], [0, 0], "b-", linewidth=2)

        # 繪製固定端
        self.ax.plot([0, 0], [-0.5, 0.5], "k-", linewidth=4)

        # 設置軸標籤和標題
        self.ax.set_xlabel("Length (m)")
        self.ax.set_ylabel("Displacement (m)")
        self.ax.set_title("Cantilever Beam (Undeformed)")

        # 調整圖形範圍
        self.adjust_plot_limits()

        # 更新畫布
        self.canvas.draw()

    def plot(self):
        try:
            length = float(self.length_entry.get())
            load = -abs(float(self.load_entry.get()))  # 確保 load 為負值
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numbers")
            return

        # 清除之前的圖形
        self.ax.clear()

        # 計算變形
        x = np.linspace(0, length, 100)
        y = (load * x**2 * (3 * length - x)) / (
            6 * 200e9 * 30e-6
        )  # 假設 EI = 200e9 * 30e-6

        # 繪製變形後的梁
        self.ax.plot(x, y, "r-", linewidth=2)

        # 繪製固定端
        self.ax.plot([0, 0], [-0.5, 0.5], "k-", linewidth=4)

        # 繪製載荷箭頭
        arrow_length = 0.1 * length
        self.ax.arrow(
            length,
            0,
            0,
            load / 1000,
            head_width=0.05 * length,
            head_length=0.1 * arrow_length,
            fc="g",
            ec="g",
        )

        # 設置軸標籤和標題
        self.ax.set_xlabel("Length (m)")
        self.ax.set_ylabel("Displacement (m)")
        self.ax.set_title(f"Cantilever Beam (Load = {abs(load)} N)")

        # 調整圖形範圍
        self.adjust_plot_limits()

        # 更新畫布
        self.canvas.draw()

        # 在繪製完主圖後，更新截面圖
        self.plot_section()

    def adjust_plot_limits(self):
        # 獲取當前的軸範圍
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()

        # 為了包含所有元素，稍微擴大範圍
        margin = 0.1  # 10% 的邊距
        x_range = x_max - x_min
        y_range = y_max - y_min

        new_x_min = x_min - margin * x_range
        new_x_max = x_max + margin * x_range
        new_y_min = y_min - margin * y_range
        new_y_max = y_max + margin * y_range

        # 設置新的軸範圍
        self.ax.set_xlim(new_x_min, new_x_max)
        self.ax.set_ylim(new_y_min, new_y_max)

        # 獲取畫布的當前大小
        canvas_width = self.canvas.get_tk_widget().winfo_width()
        canvas_height = self.canvas.get_tk_widget().winfo_height()

        # 調整圖形大小以匹配畫布大小
        self.figure.set_size_inches(
            canvas_width / self.figure.dpi, canvas_height / self.figure.dpi
        )

        # 保持縱橫比，但允許 Y 軸隨窗口大小變化
        aspect_ratio = (new_x_max - new_x_min) / (new_y_max - new_y_min)
        self.ax.set_aspect(aspect_ratio * canvas_height / canvas_width)


# 主程序
if __name__ == "__main__":
    root = tk.Tk()
    app = CantileverBeamPlotter(root)
    root.mainloop()
