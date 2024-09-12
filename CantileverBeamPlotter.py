import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CantileverBeamPlotter:
    def __init__(self, master):
        self.master = master
        master.title("Cantilever Beam Plotter")

        # 創建輸入框和標籤
        ttk.Label(master, text="Beam Length:").grid(row=0, column=0, padx=5, pady=5)
        self.length_entry = ttk.Entry(master)
        self.length_entry.grid(row=0, column=1, padx=5, pady=5)
        self.length_entry.insert(0, "10")  # 默認值

        ttk.Label(master, text="Load:").grid(row=1, column=0, padx=5, pady=5)
        self.load_entry = ttk.Entry(master)
        self.load_entry.grid(row=1, column=1, padx=5, pady=5)
        self.load_entry.insert(0, "100")  # 默認值

        # 創建按鈕
        self.plot_button = ttk.Button(master, text="Solve", command=self.plot)
        self.plot_button.grid(row=2, column=0, columnspan=2, pady=10)

        # 創建圖形和畫布
        self.figure = plt.Figure(figsize=(8, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().grid(
            row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew"
        )

        # 設置網格權重
        master.grid_rowconfigure(3, weight=1)
        master.grid_columnconfigure(0, weight=1)
        master.grid_columnconfigure(1, weight=1)

        # 綁定調整大小事件
        self.canvas.get_tk_widget().bind("<Configure>", self.on_resize)

        # 初始繪製未變形的梁
        self.plot_undeformed_beam()

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
