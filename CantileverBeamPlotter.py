import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class CantileverBeamPlotter:
    def __init__(self, master):
        self.master = master
        master.title("Cantilever Beam Plotter")

        self.length = tk.DoubleVar(value=10)
        self.load = tk.DoubleVar(value=1000)
        self.E = 200e9  # Young's modulus for steel (Pa)
        self.I = 1e-6  # Moment of inertia (m^4)

        # Create controls
        ttk.Label(master, text="Beam Length (m):").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(master, textvariable=self.length).grid(
            row=0, column=1, padx=5, pady=5
        )

        ttk.Label(master, text="Load (N):").grid(row=1, column=0, padx=5, pady=5)
        ttk.Entry(master, textvariable=self.load).grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(master, text="Plot", command=self.plot_beam).grid(
            row=2, column=0, columnspan=2, pady=10
        )

        # Modify figure creation part
        self.figure = plt.Figure(figsize=(8, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.get_tk_widget().grid(
            row=3, column=0, columnspan=2, padx=10, pady=10
        )

        # Add window closing event handling
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def calculate_deflection(self, x):
        L = self.length.get()
        P = self.load.get()
        return (P * x**2 * (3 * L - x)) / (6 * self.E * self.I)

    def plot_beam(self):
        L = self.length.get()
        P = self.load.get()

        self.ax.clear()

        # Plot beam
        x = np.linspace(0, L, 100)
        y = self.calculate_deflection(x)
        self.ax.plot(x, y, "b-", linewidth=2)

        # Plot fixed end
        self.ax.plot([0], [0], "ks", markersize=10)

        # Plot load arrow
        max_deflection = self.calculate_deflection(L)
        arrow_length = min(0.2 * L, abs(max_deflection) * 2)
        self.ax.arrow(
            L,
            max_deflection,
            0,
            -arrow_length,
            head_width=0.02 * L,
            head_length=0.05 * L,
            fc="r",
            ec="r",
            width=0.005 * L,
            length_includes_head=True,
        )

        # Add labels
        self.ax.text(L / 2, max_deflection / 2, f"Length = {L:.2f} m", ha="center")
        self.ax.text(
            L, max_deflection - arrow_length, f"Load = {P:.0f} N", ha="right", va="top"
        )
        self.ax.text(
            0,
            max_deflection / 2,
            f"Max Deflection = {abs(max_deflection):.4f} m",
            ha="left",
            va="center",
        )

        # Set limits and aspect
        self.ax.set_xlim(-0.1 * L, 1.1 * L)
        y_range = max(abs(max_deflection), 0.1 * L)
        self.ax.set_ylim(-1.5 * y_range, 0.5 * y_range)
        self.ax.set_aspect("equal", adjustable="box")

        # Add labels and title
        self.ax.set_xlabel("Length (m)")
        self.ax.set_ylabel("Deflection (m)")
        self.ax.set_title("Cantilever Beam Deflection")

        self.canvas.draw()

    def on_closing(self):
        plt.close("all")  # Close all Matplotlib figures
        self.master.destroy()  # Destroy Tkinter window


# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = CantileverBeamPlotter(root)
    root.mainloop()
