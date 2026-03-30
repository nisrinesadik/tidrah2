import tkinter as tk
from tkinter import messagebox
from backend.data_fetcher import fetch_pvgis_hourly
from backend.wind_model_detailed import run_full_wind_model
from backend.solar_model_detailed import run_full_solar_model

class Page2Validation(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.status_label = tk.Label(self, text="Step 2: Validating site and preparing data")
        self.status_label.pack(pady=10)

        self.validate_button = tk.Button(self, text="Validate Tech Data", command=self.run_validation)
        self.validate_button.pack(pady=5)

        self.next_button = tk.Button(self, text="Next", command=self.goto_next)
        self.next_button.pack(pady=10)
        self.next_button.config(state="disabled")

    def run_validation(self):
        page1 = self.controller.frames["Page1Inputs"]

        try:
            lat = float(page1.latitude_entry.get())
            lon = float(page1.longitude_entry.get())
            app_type = page1.application_type.get()
            h2_target = float(page1.h2_output.get())  # kg/day
            capex = float(page1.capex.get())
            pv_area = float(page1.pv_area.get())
            electrolyzer_type = page1.electrolyzer.get()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric inputs in Page 1.")
            return

        if not app_type or not electrolyzer_type:
            messagebox.showerror("Error", "Please select valid options for application type and electrolyzer.")
            return


        # Step 2: Assign hub height
        hub_height = 60 if app_type == "Commercial" else 80

        # Step 3: Estimate energy need (kWh/year)
        efficiency_map = {"Alkaline": 0.65, "PEM": 0.58}
        default_eff = efficiency_map.get(electrolyzer_type, 0.6)
        energy_per_kg = 33.3 / default_eff
        annual_kWh = h2_target * energy_per_kg * 365

        # Step 4: Run wind model
        self.status_label.config(text="Running wind energy model...")
        try:
            wind_result = run_full_wind_model(lat, lon, hub_height, annual_kWh)
        except Exception as e:
            messagebox.showerror("Wind Modeling Error", str(e))
            return

        # Step 5: Run solar model
        self.status_label.config(text="Running solar energy model...")
        try:
            solar_result = run_full_solar_model(
                lat=lat,
                lon=lon,
                area_m2=pv_area,
                eta=0.15,
                loss_factor=0.14,
                tilt=30,
                aspect=0,
                rated_power_kw=pv_area * 0.15
            )
        except Exception as e:
            messagebox.showerror("Solar Modeling Error", str(e))
            return

        # Step 6: Fixed financial parameters
        discount_rate = 0.08
        lifetime = 20

        # Step 7: Store shared state
        self.controller.shared_data = {
            "coordinates": (lat, lon),
            "hub_height": hub_height,
            "capex_limit": capex,
            "pv_area": pv_area,
            "electrolyzer_type": electrolyzer_type,
            "h2_target": h2_target,
            "energy_required": annual_kWh,
            "wind_model_result": wind_result,
            "solar_model_result": solar_result,
            "df_hourly_solar": solar_result["df_hourly"],
            "df_daily_solar": solar_result["df_daily"],
            "discount_rate": discount_rate,
            "lifetime": lifetime
        }

        self.status_label.config(text="All data validated successfully.")
        self.next_button.config(state="normal")

    def goto_next(self):
        self.controller.show_frame("Page3Simulation")
