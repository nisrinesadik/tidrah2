import tkinter as tk
from backend.optimizer import evaluate_options

class Page3Simulation(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.result_label = tk.Label(self, text="Hydrogen Simulation Results", font=("Arial", 14))
        self.result_label.pack(pady=10)

        self.output_text = tk.Text(self, width=90, height=28)
        self.output_text.pack(pady=10)

        self.simulate_button = tk.Button(self, text="Run Simulation", command=self.run_simulation)
        self.simulate_button.pack(pady=5)

        self.next_button = tk.Button(self, text="Next", command=self.goto_next)
        self.next_button.pack(pady=10)
        self.next_button.config(state="disabled")

    def run_simulation(self):
        self.output_text.delete("1.0", tk.END)
        data = self.controller.shared_data
        page1 = self.controller.frames["Page1Inputs"]

        try:
            energy_source = page1.energy_source.get()
            electrolyzer_option = page1.electrolyzer.get()
            h2_target_day = float(page1.h2_output.get())
            capex_limit = float(page1.capex.get())
            discount_rate = data.get("discount_rate", 0.08)
            lifetime = data.get("lifetime", 20)
        except Exception:
            self.output_text.insert("1.0", "Missing or invalid input fields from Page 1.\n")
            return

        solar_kwh = data.get("solar_model_result", {}).get("E_annual", 0)
        wind_kwh = data.get("wind_model_result", {}).get("total_energy", 0)
        hybrid_kwh = solar_kwh + wind_kwh

        df_solar = data.get("df_hourly_solar", None)
        df_wind = data.get("wind_model_result", {}).get("df_hourly", None)

        opts = evaluate_options(
            solar_kwh, wind_kwh, hybrid_kwh,
            h2_target_day, capex_limit, electrolyzer_option,
            df_solar_hourly=df_solar,
            df_wind_hourly=df_wind,
            user_source=energy_source,
            discount_rate=discount_rate,
            lifetime=lifetime
        )

        if opts.get("selected_source") is None:
            self.output_text.insert(tk.END, opts.get("message", "Simulation failed.") + "\n")
            return

        h2 = opts.get("hydrogen_result", {})
        if not h2:
            self.output_text.insert(tk.END, "⚠️ No hydrogen result returned by the optimizer.\n")
            return

        kg_day = h2.get("kg_per_day")
        kg_year = h2.get("kg_per_year")
        efficiency = h2.get("efficiency")
        energy_per_kg = h2.get("energy_per_kg")

        if kg_day is None or kg_year is None or kg_day <= 0 or kg_year <= 0:
            self.output_text.insert(tk.END, "⚠️ Hydrogen output not available.\n")
            self.output_text.insert(tk.END, "⚠️ Warning: Hydrogen yield could not be calculated properly.\n")
            return

        if energy_per_kg is None:
            self.output_text.insert(tk.END, "⚠️ Missing energy per kg value from backend.\n")
            return

        enet = kg_year * energy_per_kg
        pv_area = data.get("pv_area", 1000)

        # SDG Calculations
        emax = 1_000_000
        sdg7 = min((enet / emax) * 100, 100)

        capacity_kw = pv_area * 0.15
        jobs = (capacity_kw * 10) / 1000
        gdp_impact = (capex_limit + 0.05 * capex_limit) * 1.3
        sdg8 = min((jobs / 10) * 50 + (gdp_impact / 100_000) * 50, 100)

        co2_saved = kg_year * 10
        sdg13 = min((co2_saved / 1_000_000) * 100, 100)

        # Display results
        self.output_text.insert(tk.END, f"Selected Source: {opts['selected_source']}\n")
        self.output_text.insert(tk.END, f"Electrolyzer: {opts.get('electrolyzer', electrolyzer_option)}\n")
        self.output_text.insert(tk.END, f"Hydrogen Production: {kg_day:.2f} kg/day | {kg_year:.2f} kg/year\n")
        self.output_text.insert(tk.END, f"Energy per kg H2: {energy_per_kg:.2f} kWh/kg\n")

        if "lcoh" in opts:
            self.output_text.insert(tk.END, f"LCOH: {opts['lcoh']:.3f} €/kg\n")
        if "score" in opts:
            self.output_text.insert(tk.END, f"Scenario Score: {opts['score']:.2f}\n")

        if opts["selected_source"] == "Hybrid" and "hybrid_summary" in opts:
            summary = opts["hybrid_summary"]
            self.output_text.insert(tk.END, f"Hybrid Energy Total: {summary['E_hybrid_total']:.2f} kWh\n")
            self.output_text.insert(tk.END, f"Solar Used: {summary['E_solar_used']:.2f} kWh ({summary['solar_share_percent']:.2f}%)\n")
            self.output_text.insert(tk.END, f"Wind Used: {summary['E_wind_used']:.2f} kWh ({summary['wind_share_percent']:.2f}%)\n")

        # Save result to shared data
        self.controller.shared_data["simulation_result"] = {
            "source": opts["selected_source"],
            "electrolyzer": opts.get("electrolyzer", electrolyzer_option),
            "kg_day": round(kg_day, 2),
            "kg_year": round(kg_year, 2),
            "efficiency": efficiency,
            "energy_per_kg": round(energy_per_kg, 2),
            "lcoh": opts.get("lcoh"),
            "score": opts.get("score"),
            "enet": round(enet, 2),
            "jobs": round(jobs, 2),
            "gdp_impact": round(gdp_impact, 2),
            "co2_saved": round(co2_saved, 2),
            "sdg_scores": {
                "SDG 7": round(sdg7, 2),
                "SDG 8": round(sdg8, 2),
                "SDG 13": round(sdg13, 2)
            }
        }

        self.next_button.config(state="normal")

    def goto_next(self):
        self.controller.show_frame("Page4Results")
