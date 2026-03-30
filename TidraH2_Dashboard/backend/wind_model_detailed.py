
import requests
import pandas as pd
import numpy as np
import math
from backend.turbine_library import turbine_data

def fetch_pvgis_hourly_wind(lat, lon):
    url = f"https://re.jrc.ec.europa.eu/api/v5_2/tmy?lat={lat}&lon={lon}&usehorizon=1&outputformat=json"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch PVGIS wind data")
    data = response.json()['outputs']['tmy_hourly']
    return pd.DataFrame(data)

def extrapolate_wind_speed(v10, hub_height, alpha=0.25):
    return v10 * ((hub_height / 10) ** alpha)

def compute_air_density(T_K, z_m):
    return (353.1 * np.exp(-0.0342 * z_m / T_K)) / T_K  # [kg/m³]

def bin_analysis(df, power_curve):
    bins = list(range(26))
    frequencies = []
    wind_speeds = df['WS_hub'].tolist()
    for i in bins:
        lower = i - 0.5
        upper = i + 0.5
        count = sum(lower < v <= upper for v in wind_speeds)
        frequencies.append(count)
    probs = [f / 8760 for f in frequencies]
    hours = [p * 8760 for p in probs]
    power = [power_curve[i] for i in bins]
    energy = [(p * h) / 1000 for p, h in zip(power, hours)]  # kWh
    total_energy = sum(energy)
    return pd.DataFrame({
        'Bin': bins,
        'Frequency': frequencies,
        'Probability': probs,
        'Hours': hours,
        'Power (W)': power,
        'Energy (kWh)': energy
    }), total_energy

def calculate_power_in_wind(rho, radius, v_avg):
    A = math.pi * radius ** 2
    return 0.5 * rho * A * (v_avg**3)  # Watts

def match_best_turbine(df, rho, v_avg, energy_required):
    best_match = None
    min_surplus = float('inf')
    best_data = {}

    for name, info in turbine_data.items():
        curve = info['curve_w']
        radius = info['radius_m']
        rated_power = info['rated_power_w']
        df_bin, total_energy = bin_analysis(df, curve)

        if total_energy >= energy_required:
            surplus = total_energy - energy_required
            if surplus < min_surplus:
                min_surplus = surplus
                best_data = {
                    'name': name,
                    'df_bin': df_bin,
                    'total_energy': total_energy,
                    'rated_power': rated_power,
                    'radius': radius
                }

    if not best_data:
        raise Exception("No turbine can meet the energy demand.")

    power_wind = calculate_power_in_wind(rho, best_data['radius'], v_avg)
    energy_wind = (power_wind * 8760) / 1000  # in kWh
    efficiency = (best_data['total_energy'] / energy_wind) * 100
    capacity_factor = (best_data['total_energy'] * 1000) / (best_data['rated_power'] * 8760) * 100

    best_data.update({
        'power_wind': power_wind,
        'energy_wind': energy_wind,
        'efficiency': efficiency,
        'capacity_factor': capacity_factor,
        'rho': rho,
        'v_avg': v_avg
    })

    return best_data

def run_full_wind_model(lat, lon, hub_height, energy_required):
    df = fetch_pvgis_hourly_wind(lat, lon)
    df['WS_hub'] = extrapolate_wind_speed(df['WS10m'], hub_height)
    df['T_hub_K'] = df['T2m'] + 273.15
    rho = compute_air_density(df['T_hub_K'].mean(), hub_height)
    v_avg = df['WS_hub'].mean()

    best_turbine = match_best_turbine(df, rho, v_avg, energy_required)
    best_turbine['wind_profile'] = df

    return best_turbine
