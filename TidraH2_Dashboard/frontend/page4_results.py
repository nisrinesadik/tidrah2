import streamlit as st
from backend.report_generator import generate_report

def render():
    st.header("Simulation Results Summary")

    # Initialize shared data if missing
    if "shared_data" not in st.session_state:
        st.session_state.shared_data = {}

    shared_data = st.session_state.shared_data

    if not shared_data or "simulation_result" not in shared_data:
        st.warning("No results to display.")
        return

    result = shared_data["simulation_result"]

    st.write(f"**Selected Source:** {result['source']}")
    st.write(f"**Electrolyzer:** {result['electrolyzer']}")
    st.write(f"**Hydrogen Output:** {result['kg_day']:.2f} kg/day | {result['kg_year']:.2f} kg/year")

    if "lcoh" in result and result["lcoh"] is not None:
        st.write(f"**LCOH:** {result['lcoh']:.3f} €/kg")

    if "score" in result and result["score"] is not None:
        st.write(f"**Scenario Score:** {result['score']:.2f}")

    if "enet" in result:
        st.write(f"**Net Energy Used:** {result['enet']:.0f} kWh/year")

    if "jobs" in result:
        st.write(f"**Jobs Created:** {result['jobs']:.0f}")

    if "gdp_impact" in result:
        st.write(f"**GDP Impact:** {result['gdp_impact']:.0f} €")

    if "co2_saved" in result:
        st.write(f"**CO₂ Saved:** {result['co2_saved']:.0f} kg/year")

    if "sdg_scores" in result:
        st.subheader("SDG Scores (normalized to 100%)")
        for key, value in result["sdg_scores"].items():
            st.write(f"**{key}:** {value:.2f}%")

    if result["source"] == "Hybrid" and "hybrid_summary" in result and result["hybrid_summary"] is not None:
        summary = result["hybrid_summary"]
        st.subheader("Hybrid Energy Breakdown")
        st.write(f"**Total Hybrid Energy:** {summary['E_hybrid_total']:.2f} kWh")
        st.write(f"**Solar Used:** {summary['E_solar_used']:.2f} kWh ({summary['solar_share_percent']:.2f}%)")
        st.write(f"**Wind Used:** {summary['E_wind_used']:.2f} kWh ({summary['wind_share_percent']:.2f}%)")

    # Export report
    if st.button("Export Full Report (PDF)"):
        try:
            sim_data = result.copy()
            sim_data["capex"] = float(shared_data.get("capex", 0))
            filename = generate_report(sim_data)
            st.success(f"Report saved as: {filename}")
        except Exception as e:
            st.error(f"Failed to generate report: {str(e)}")

    # Restart simulation
    if st.button("Run Another Simulation"):
        st.session_state.shared_data = {}
        st.session_state.current_page = "Inputs"
        st.rerun()