import pandas as pd

def compute_hydrogen_yield(total_energy_kwh, electrolyzer_type):
    """
    Computes hydrogen yield (in kg/year and kg/day) from total net energy input.

    Args:
        total_energy_kwh (float): Net energy input to electrolysis (after desalination)
        electrolyzer_type (str): 'Alkaline', 'PEM', or 'Evaluate All'

    Returns:
        dict or list: One dict if single type, or list of dicts if 'Evaluate All'
    """
    efficiency_map = {
        'alkaline': 0.65,
        'pem': 0.58
    }

    if electrolyzer_type.lower() == "evaluate all":
        results = []
        for etype, eff in efficiency_map.items():
            energy_per_kg = 33.3 / eff
            hydrogen_kg_year = total_energy_kwh / energy_per_kg
            hydrogen_kg_day = hydrogen_kg_year / 365
            results.append({
                'electrolyzer': etype.capitalize(),
                'kg_per_year': hydrogen_kg_year,
                'kg_per_day': hydrogen_kg_day,
                'efficiency': eff,
                'energy_per_kg': energy_per_kg
            })
        return results

    etype = electrolyzer_type.lower()
    if etype not in efficiency_map:
        raise ValueError("Unknown electrolyzer type. Use 'Alkaline', 'PEM', or 'Evaluate All'.")

    eff = efficiency_map[etype]
    energy_per_kg = 33.3 / eff
    hydrogen_kg_year = total_energy_kwh / energy_per_kg
    hydrogen_kg_day = hydrogen_kg_year / 365

    return {
        'kg_per_year': hydrogen_kg_year,
        'kg_per_day': hydrogen_kg_day,
        'efficiency': eff,
        'energy_per_kg': energy_per_kg
    }

def compute_hourly_hydrogen_production(df_energy, electrolyzer_type):
    """
    Computes hourly hydrogen production using hourly net energy.

    Args:
        df_energy (pd.DataFrame): DataFrame with 'Enet' column (kWh)
        electrolyzer_type (str): 'Alkaline', 'PEM', or 'Evaluate All'

    Returns:
        dict or tuple:
            - If single type: (df, total_kg)
            - If 'Evaluate All': dict with data for both electrolyzers
    """
    if "Enet" not in df_energy.columns:
        raise ValueError("DataFrame must include an 'Enet' column (net energy in kWh)")

    efficiency_map = {
        'pem': 0.70,
        'alkaline': 0.65
    }

    if electrolyzer_type.lower() == "evaluate all":
        results = {}
        for etype, eff in efficiency_map.items():
            df_copy = df_energy.copy()
            energy_per_kg = 33.3 / eff
            df_copy["H2_kg"] = df_copy["Enet"] / energy_per_kg
            df_copy["H2_kg"] = df_copy["H2_kg"].fillna(0).clip(lower=0)
            results[etype] = {
                "df": df_copy,
                "total_kg": df_copy["H2_kg"].sum(),
                "efficiency": eff,
                "energy_per_kg": energy_per_kg
            }
        return results

    key = electrolyzer_type.lower()
    if key not in efficiency_map:
        raise ValueError("Electrolyzer type must be 'PEM', 'Alkaline', or 'Evaluate All'.")

    eff = efficiency_map[key]
    energy_per_kg = 33.3 / eff
    df_copy = df_energy.copy()
    df_copy["H2_kg"] = df_copy["Enet"] / energy_per_kg
    df_copy["H2_kg"] = df_copy["H2_kg"].fillna(0).clip(lower=0)
    total_kg = df_copy["H2_kg"].sum()

    return df_copy, total_kg
