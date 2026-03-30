
import pandas as pd

def compute_hybrid_energy(df_solar, df_wind):
    """
    Compute hybrid hourly energy from dominant source selection.

    Args:
        df_solar (DataFrame): hourly solar net energy with 'Enet' column
        df_wind (DataFrame): hourly wind net energy with 'Enet' column

    Returns:
        df_hybrid (DataFrame): with columns ['Esolar', 'Ewind', 'Ehybrid', 'source_flag']
        summary (dict): with total hybrid energy, solar/wind shares, and breakdown
    """
    if "Enet" not in df_solar.columns or "Enet" not in df_wind.columns:
        raise ValueError("Missing 'Enet' column in input dataframes.")

    df = pd.DataFrame({
        "Esolar": df_solar["Enet"].values,
        "Ewind": df_wind["Enet"].values
    })

    df["Ehybrid"] = df[["Esolar", "Ewind"]].max(axis=1)
    df["source_flag"] = df.apply(lambda row: "solar" if row["Esolar"] > row["Ewind"] else "wind", axis=1)

    # Totals
    total_hybrid_energy = df["Ehybrid"].sum()
    solar_used = df.loc[df["source_flag"] == "solar", "Esolar"].sum()
    wind_used = df.loc[df["source_flag"] == "wind", "Ewind"].sum()

    solar_share = (solar_used / total_hybrid_energy) * 100 if total_hybrid_energy > 0 else 0
    wind_share = (wind_used / total_hybrid_energy) * 100 if total_hybrid_energy > 0 else 0

    summary = {
        "E_hybrid_total": total_hybrid_energy,
        "E_solar_used": solar_used,
        "E_wind_used": wind_used,
        "solar_share_percent": solar_share,
        "wind_share_percent": wind_share
    }

    return df, summary
