import tkinter as tk
from tkinter import messagebox
from backend.report_generator import generate_report

class Page4Results(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        title = tk.Label(self, text="Simulation Results Summary", font=("Arial", 14))
        title.pack(pady=10)

        self.result_text = tk.Text(self, width=90, height=24)
        self.result_text.pack(pady=10)

        self.export_button = tk.Button(self, text="Export Full Report (PDF)", command=self.export_report)
        self.export_button.pack(pady=10)

        self.restart_button = tk.Button(self, text="Run Another Simulation", command=self.restart)
        self.restart_button.pack(pady=5)

    def tkraise(self, *args, **kwargs):
        super().tkraise(*args, **kwargs)
        self.show_results()

    def show_results(self):
        self.result_text.delete("1.0", tk.END)
        data = self.controller.shared_data
        if not data or "simulation_result" not in data:
            self.result_text.insert(tk.END, "No results to display.\n")
            return

        result = data["simulation_result"]

        self.result_text.insert(tk.END, f"Selected Source: {result['source']}\n")
        self.result_text.insert(tk.END, f"Electrolyzer: {result['electrolyzer']}\n")
        self.result_text.insert(tk.END, f"Hydrogen Output: {result['kg_day']:.2f} kg/day | {result['kg_year']:.2f} kg/year\n")

        if "lcoh" in result:
            self.result_text.insert(tk.END, f"LCOH: {result['lcoh']:.3f} €/kg\n")
        if "score" in result:
            self.result_text.insert(tk.END, f"Scenario Score: {result['score']:.2f}\n")
        if "enet" in result:
            self.result_text.insert(tk.END, f"Net Energy Used: {result['enet']:.0f} kWh/year\n")
        if "jobs" in result:
            self.result_text.insert(tk.END, f"Jobs Created: {result['jobs']:.0f}\n")
        if "gdp_impact" in result:
            self.result_text.insert(tk.END, f"GDP Impact: {result['gdp_impact']:.0f} €\n")
        if "co2_saved" in result:
            self.result_text.insert(tk.END, f"CO₂ Saved: {result['co2_saved']:.0f} kg/year\n")

        if "sdg_scores" in result:
            self.result_text.insert(tk.END, "\nSDG Scores (normalized to 100%):\n")
            for key, value in result["sdg_scores"].items():
                self.result_text.insert(tk.END, f" - {key}: {value:.2f}%\n")

        if result["source"] == "Hybrid" and "hybrid_summary" in result:
            summary = result["hybrid_summary"]
            self.result_text.insert(tk.END, "\nHybrid Energy Breakdown:\n")
            self.result_text.insert(tk.END, f"Total Hybrid Energy: {summary['E_hybrid_total']:.2f} kWh\n")
            self.result_text.insert(tk.END, f"Solar Used: {summary['E_solar_used']:.2f} kWh ({summary['solar_share_percent']:.2f}%)\n")
            self.result_text.insert(tk.END, f"Wind Used: {summary['E_wind_used']:.2f} kWh ({summary['wind_share_percent']:.2f}%)\n")

    def export_report(self):
        try:
            sim_data = self.controller.shared_data["simulation_result"]
            sim_data["capex"] = float(self.controller.frames["Page1Inputs"].capex.get())
            filename = generate_report(sim_data)
            messagebox.showinfo("Success", f"Report saved as:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")

    def restart(self):
        self.controller.show_frame("Page1Inputs")
