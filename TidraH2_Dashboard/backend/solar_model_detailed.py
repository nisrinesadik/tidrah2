import requests
import pandas as pd

def fetch_hourly_pvgis_irradiance(lat, lon, tilt=30, aspect=0):
    url = (
        "https://re.jrc.ec.europa.eu/api/v5_2/seriescalc?"
        f"lat={lat}&lon={lon}&startyear=2016&endyear=2016"
        f"&outputformat=json&pvtechchoice=crystSi&mountingplace=free"
        f"&loss=0&angle={tilt}&aspect={aspect}&optimalangles=0&hourlyvalues=1"
    )
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to fetch PVGIS timeseries data")
    data = response.json()['outputs']['hourly']
    df = pd.DataFrame(data)
    return df

def calculate_hourly_energy(df, area_m2, eta=0.15, loss_factor=0.14):
    # Calculate raw hourly energy (Eh) in kWh
    df['Eh'] = (df['G(i)'] / 1000) * area_m2 * eta
    # Apply system loss correction
    df['Enet'] = df['Eh'] * (1 - loss_factor)
    return df

def calculate_solar_metrics(df, rated_power_kw):
    # ✅ FIXED datetime parsing format
    df['hour'] = pd.to_datetime(df['time'], format='%Y%m%d:%H%M')
    df['day'] = df['hour'].dt.dayofyear

    E_annual = df['Enet'].sum()  # Total annual kWh
    daily_energy = df.groupby('day')['Enet'].sum().reset_index(name='E_daily')
    CF = E_annual / (8760 * rated_power_kw) if rated_power_kw > 0 else 0

    return {
        'df_hourly': df,
        'E_annual': E_annual,
        'capacity_factor': CF,
        'df_daily': daily_energy
    }

def run_full_solar_model(lat, lon, area_m2, eta=0.15, loss_factor=0.14, tilt=30, aspect=0, rated_power_kw=1.0):
    df = fetch_hourly_pvgis_irradiance(lat, lon, tilt, aspect)
    df = calculate_hourly_energy(df, area_m2, eta, loss_factor)
    results = calculate_solar_metrics(df, rated_power_kw)
    return results
