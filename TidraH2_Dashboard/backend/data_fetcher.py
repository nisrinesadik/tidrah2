# backend/data_fetcher.py

import requests
import pandas as pd

PVGIS_API_URL = "https://re.jrc.ec.europa.eu/api/v5_3/seriescalc"

def fetch_pvgis_hourly(lat, lon, year=2020, peak_power=1.0, tilt=30, azimuth=0):
    """
    Fetch hourly solar radiation data from PVGIS for a given location.
    Returns a pandas DataFrame with hourly data for the full year (8760 hours).
    """
    params = {
        'lat': lat,
        'lon': lon,
        'startyear': year,
        'endyear': year,
        'outputformat': 'json',
        'pvtechchoice': 'crystSi',
        'mountingplace': 'free',
        'loss': 14,
        'peakpower': peak_power,
        'angle': tilt,
        'aspect': azimuth,
        'optimalangles': 0,
        'hourlyvalues': 1,
    }

    try:
        response = requests.get(PVGIS_API_URL, params=params)
        response.raise_for_status()
        data = response.json()

        if 'outputs' not in data or 'hourly' not in data['outputs']:
            return None, "No hourly data found in PVGIS response."

        df = pd.DataFrame(data['outputs']['hourly'])
        return df, "PVGIS data successfully retrieved."

    except requests.exceptions.RequestException as e:
        return None, f"Request failed: {e}"

    except Exception as ex:
        return None, f"Unexpected error: {ex}"

