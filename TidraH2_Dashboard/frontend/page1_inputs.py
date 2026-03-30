import tkinter as tk
from tkinter import ttk

class Page1Inputs(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Site Coordinates
        tk.Label(self, text="Site Coordinates (for reference only):").pack(pady=5)
        self.latitude_entry = tk.Entry(self, width=30)
        self.latitude_entry.pack(pady=2)
        self.longitude_entry = tk.Entry(self, width=30)
        self.longitude_entry.pack(pady=2)

        # Application Type
        tk.Label(self, text="Application Type:").pack(pady=5)
        self.application_type = ttk.Combobox(self, values=["Commercial", "Industrial"])
        self.application_type.pack(pady=2)

        # Hydrogen Output Target
        tk.Label(self, text="Hydrogen Output Target (kg/day):").pack(pady=5)
        self.h2_output = tk.Entry(self, width=30)
        self.h2_output.pack(pady=2)

        # CAPEX Limit
        tk.Label(self, text="CAPEX Limit (USD):").pack(pady=5)
        self.capex = tk.Entry(self, width=30)
        self.capex.pack(pady=2)

        # Available PV Surface Area
        tk.Label(self, text="Available PV Surface Area (m²):").pack(pady=5)
        self.pv_area = tk.Entry(self, width=30)
        self.pv_area.pack(pady=2)

        # Electrolyzer Type
        tk.Label(self, text="Electrolyzer Type:").pack(pady=5)
        self.electrolyzer = ttk.Combobox(self, values=["Alkaline", "PEM", "Evaluate All"])
        self.electrolyzer.pack(pady=2)

        # Preferred Energy Source
        tk.Label(self, text="Preferred Energy Source:").pack(pady=5)
        self.energy_source = ttk.Combobox(self, values=["Solar", "Wind", "Optimize"])
        self.energy_source.pack(pady=2)

        # Fixed Parameters (Information only)
        tk.Label(self, text="Discount Rate (%): 8.0").pack(pady=5)
        tk.Label(self, text="Project Lifetime (years): 20").pack(pady=2)

        # Next Button
        tk.Button(self, text="Next", command=lambda: controller.show_frame("Page2Validation")).pack(pady=20)
