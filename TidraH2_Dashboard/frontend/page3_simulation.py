import streamlit as st
from backend.optimizer import evaluate_options

def render():
    st.header("Hydrogen Simulation Results")

    # Initialize shared data if missing
    if "shared_data" not in st.session_state:
        st.session_state.shared_data = {}

    shared_data = st.session_state.shared_data

    if st.button("Run Simulation"):
        try:
            energy_source = shared_data.get("energy_source", "")
            electrolyzer_option = shared_data.get("electrolyzer", "")
            h2_target_day = float(shared_data.get("h2_output", ""))
            capex_limit = float(shared_data.get("capex", ""))
            discount_rate = shared_data.get("discount_rate", 0.08)
            lifetime = shared_data.get("lifetime", 20)
        except Exception:
            st.error("Missing or invalid input fields from Page 1.")
            return

        solar_kwh = shared_data.get("solar_model_result", {}).get("E_annual", 0)
        wind_kwh = shared_data.get("wind_model_result", {}).get("total_energy", 0)
        hybrid_kwh = solar_kwh + wind_kwh

        df_solar = shared_data.get("df_hourly_solar", None)
        df_wind = shared_data.get("wind_model_result", {}).get("df_hourly", None)

        opts = evaluate_options(
            solar_kwh,
            wind_kwh,
            hybrid_kwh,
            h2_target_day,
            capex_limit,
            electrolyzer_option,
            df_solar_hourly=df_solar,
            df_wind_hourly=df_wind,
            user_source=energy_source,
            discount_rate=discount_rate,
            lifetime=lifetime
        )

        if opts.get("selected_source") is None:
            st.error(opts.get("message", "Simulation failed."))
            return

        h2 = opts.get("hydrogen_result", {})
        if not h2:
            st.warning("No hydrogen result returned by the optimizer.")
            return

        kg_day = h2.get("kg_per_day")
        kg_year = h2.get("kg_per_year")
        efficiency = h2.get("efficiency")
        energy_per_kg = h2.get("energy_per_kg")

        if kg_day is None or kg_year is None or kg_day <= 0 or kg_year <= 0:
            st.warning("Hydrogen output not available.")
            st.warning("Warning: Hydrogen yield could not be calculated properly.")
            return

        if energy_per_kg is None:
            st.warning("Missing energy per kg value from backend.")
            return

        enet = kg_year * energy_per_kg
        pv_area = shared_data.get("pv_area", 1000)

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
        st.success("Simulation completed successfully.")

        st.write(f"**Selected Source:** {opts['selected_source']}")
        st.write(f"**Electrolyzer:** {opts.get('electrolyzer', electrolyzer_option)}")
        st.write(f"**Hydrogen Production:** {kg_day:.2f} kg/day | {kg_year:.2f} kg/year")
        st.write(f"**Energy per kg H₂:** {energy_per_kg:.2f} kWh/kg")

        if "lcoh" in opts and opts["lcoh"] is not None:
            st.write(f"**LCOH:** {opts['lcoh']:.3f} €/kg")

        if "score" in opts and opts["score"] is not None:
            st.write(f"**Scenario Score:** {opts['score']:.2f}")

        if opts["selected_source"] == "Hybrid" and "hybrid_summary" in opts:
            summary = opts["hybrid_summary"]
            st.write(f"**Hybrid Energy Total:** {summary['E_hybrid_total']:.2f} kWh")
            st.write(f"**Solar Used:** {summary['E_solar_used']:.2f} kWh ({summary['solar_share_percent']:.2f}%)")
            st.write(f"**Wind Used:** {summary['E_wind_used']:.2f} kWh ({summary['wind_share_percent']:.2f}%)")

        # Save result to shared data
        shared_data["simulation_result"] = {
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
            },
            "hybrid_summary": opts.get("hybrid_summary", None)
        }

        shared_data["simulation_complete"] = True
        st.session_state.shared_data = shared_data

    # Show previous results if they already exist
    simulation_result = shared_data.get("simulation_result", None)
    if simulation_result:
        st.subheader("Saved Simulation Summary")
        st.write(f"**Selected Source:** {simulation_result['source']}")
        st.write(f"**Electrolyzer:** {simulation_result['electrolyzer']}")
        st.write(f"**Hydrogen Production:** {simulation_result['kg_day']:.2f} kg/day | {simulation_result['kg_year']:.2f} kg/year")
        st.write(f"**Energy per kg H₂:** {simulation_result['energy_per_kg']:.2f} kWh/kg")

        if simulation_result.get("lcoh") is not None:
            st.write(f"**LCOH:** {simulation_result['lcoh']:.3f} €/kg")

        if simulation_result.get("score") is not None:
            st.write(f"**Scenario Score:** {simulation_result['score']:.2f}")

        hybrid_summary = simulation_result.get("hybrid_summary")
        if simulation_result["source"] == "Hybrid" and hybrid_summary:
            st.write(f"**Hybrid Energy Total:** {hybrid_summary['E_hybrid_total']:.2f} kWh")
            st.write(f"**Solar Used:** {hybrid_summary['E_solar_used']:.2f} kWh ({hybrid_summary['solar_share_percent']:.2f}%)")
            st.write(f"**Wind Used:** {hybrid_summary['E_wind_used']:.2f} kWh ({hybrid_summary['wind_share_percent']:.2f}%)")

    # Next button only enabled after simulation succeeds
    simulation_complete = shared_data.get("simulation_complete", False)

    if simulation_complete:
        if st.button("Next"):
            st.session_state.current_page = "Results"
            st.rerun()
    else:
        st.button("Next", disabled=True)