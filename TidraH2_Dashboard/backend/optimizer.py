from backend.hydrogen_model import compute_hydrogen_yield, compute_hourly_hydrogen_production
from backend.hybrid_model import compute_hybrid_energy
from backend.finance_model import calculate_crf, calculate_lcoh, calculate_score

def evaluate_options(
    solar_kwh,
    wind_kwh,
    hybrid_kwh,
    h2_target_day,
    capex_limit,
    electrolyzer_type,
    df_solar_hourly=None,
    df_wind_hourly=None,
    user_source="Optimize",
    discount_rate=0.08,
    lifetime=20
):
    target_kg_year = h2_target_day * 365
    crf = calculate_crf(discount_rate, lifetime)
    opex = 0.05 * capex_limit
    capex_per_kw = {"Solar": 1000, "Wind": 1200, "Hybrid": 1300}

    def get_eff_params(etype):
        if etype.lower() == "pem":
            eff = 0.70
        else:
            eff = 0.65
        return eff, 33.3 / eff

    def evaluate_all_types(energy, hourly_df, label, reliability):
        best = None
        for etype in ["PEM", "Alkaline"]:
            try:
                desal = target_kg_year * 0.009 * 4
                usable = energy - desal
                if usable <= 0:
                    continue
                power_kw = usable / 8760
                cost = power_kw * capex_per_kw[label]
                if cost > capex_limit:
                    continue

                eff, energy_per_kg = get_eff_params(etype)

                if hourly_df is not None:
                    df = hourly_df.copy()
                    df["Enet"] -= desal / 8760
                    _, h2_total = compute_hourly_hydrogen_production(df, etype)
                else:
                    result = compute_hydrogen_yield(usable, etype)
                    h2_total = result["kg_per_year"]

                if h2_total < target_kg_year:
                    continue

                lcoh = calculate_lcoh(capex_limit, opex, crf, h2_total)
                score = calculate_score(lcoh, reliability)
                result_dict = {
                    "selected_source": label,
                    "electrolyzer": etype,
                    "hydrogen_result": {
                        "kg_per_year": h2_total,
                        "kg_per_day": h2_total / 365,
                        "efficiency": eff,
                        "energy_per_kg": energy_per_kg
                    },
                    "lcoh": lcoh,
                    "score": score,
                    "capex_cost": cost,
                    "meets_target": True
                }

                if not best or result_dict["score"] > best["score"]:
                    best = result_dict

            except Exception:
                continue
        return best

    def check_path(label, energy, hourly_df=None, reliability=0.9):
        try:
            if energy <= 0:
                return {"error": f"{label} path has insufficient energy."}
            desal = target_kg_year * 0.009 * 4
            usable = energy - desal
            if usable <= 0:
                return {"error": f"{label} path fails due to desalination load > energy produced."}
            power_kw = usable / 8760
            cost = power_kw * capex_per_kw[label]
            if cost > capex_limit:
                return {"error": f"{label} path cost exceeds CAPEX."}

            if electrolyzer_type.lower() == "evaluate all":
                return evaluate_all_types(energy, hourly_df, label, reliability)

            eff, energy_per_kg = get_eff_params(electrolyzer_type)

            if hourly_df is not None:
                df = hourly_df.copy()
                df["Enet"] -= desal / 8760
                _, h2_total = compute_hourly_hydrogen_production(df, electrolyzer_type)
            else:
                result = compute_hydrogen_yield(usable, electrolyzer_type)
                h2_total = result["kg_per_year"]

            if h2_total < target_kg_year:
                return {"error": f"{label} path yield is too low."}

            lcoh = calculate_lcoh(capex_limit, opex, crf, h2_total)
            score = calculate_score(lcoh, reliability)

            return {
                "selected_source": label,
                "electrolyzer": electrolyzer_type,
                "hydrogen_result": {
                    "kg_per_year": h2_total,
                    "kg_per_day": h2_total / 365,
                    "efficiency": eff,
                    "energy_per_kg": energy_per_kg
                },
                "lcoh": lcoh,
                "score": score,
                "capex_cost": cost,
                "meets_target": True
            }
        except Exception as e:
            return {"error": f"{label} path failed: {str(e)}"}

    # Forced user choice
    if user_source == "Solar":
        return check_path("Solar", solar_kwh, df_solar_hourly, 0.85)
    if user_source == "Wind":
        return check_path("Wind", wind_kwh, df_wind_hourly, 0.92)

    # Try Solar and Wind in fallback
    for label, energy, df, reliability in [
        ("Solar", solar_kwh, df_solar_hourly, 0.85),
        ("Wind", wind_kwh, df_wind_hourly, 0.92)
    ]:
        result = check_path(label, energy, df, reliability)
        if result and result.get("meets_target"):
            return result

    # Try Hybrid
    if df_solar_hourly is not None and df_wind_hourly is not None:
        try:
            df_hybrid, summary = compute_hybrid_energy(df_solar_hourly, df_wind_hourly)
            hybrid_energy = df_hybrid["Enet"].sum()
            desal = target_kg_year * 0.009 * 4
            usable = hybrid_energy - desal
            if usable <= 0:
                return {"error": "Hybrid path fails due to desal load."}

            if electrolyzer_type.lower() == "evaluate all":
                best = evaluate_all_types(hybrid_energy, df_hybrid, "Hybrid", 0.95)
                if best:
                    best["hybrid_summary"] = summary
                    return best

            eff, energy_per_kg = get_eff_params(electrolyzer_type)
            df_h = df_hybrid.copy()
            df_h["Enet"] -= desal / 8760
            _, h2_total = compute_hourly_hydrogen_production(df_h, electrolyzer_type)
            power_kw = usable / 8760
            cost = power_kw * capex_per_kw["Hybrid"]

            if h2_total >= target_kg_year and cost <= capex_limit:
                lcoh = calculate_lcoh(capex_limit, opex, crf, h2_total)
                score = calculate_score(lcoh, reliability=0.95)
                return {
                    "selected_source": "Hybrid",
                    "electrolyzer": electrolyzer_type,
                    "hydrogen_result": {
                        "kg_per_year": h2_total,
                        "kg_per_day": h2_total / 365,
                        "efficiency": eff,
                        "energy_per_kg": energy_per_kg
                    },
                    "lcoh": lcoh,
                    "score": score,
                    "capex_cost": cost,
                    "hybrid_summary": summary,
                    "meets_target": True
                }

        except Exception as e:
            return {"error": f"Hybrid path failed: {str(e)}"}

    return {
        "selected_source": None,
        "hydrogen_result": None,
        "message": "No configuration meets both technical and economic constraints.",
        "meets_target": False
    }
