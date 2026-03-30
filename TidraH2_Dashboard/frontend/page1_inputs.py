import streamlit as st

def render():
    st.header("Step 1: Input Parameters")

    if "shared_data" not in st.session_state:
        st.session_state.shared_data = {}

    shared_data = st.session_state.shared_data

    st.subheader("Site Coordinates (for reference only)")
    latitude = st.text_input(
        "Latitude",
        value=shared_data.get("latitude", "")
    )
    longitude = st.text_input(
        "Longitude",
        value=shared_data.get("longitude", "")
    )

    st.subheader("Application Type")
    application_type_options = ["Commercial", "Industrial"]
    default_application_type = shared_data.get("application_type", "Commercial")
    if default_application_type not in application_type_options:
        default_application_type = "Commercial"

    application_type = st.selectbox(
        "Select Application Type",
        options=application_type_options,
        index=application_type_options.index(default_application_type)
    )

    st.subheader("Hydrogen Output Target")
    h2_output = st.text_input(
        "Hydrogen Output Target (kg/day)",
        value=shared_data.get("h2_output", "")
    )

    st.subheader("CAPEX Limit")
    capex = st.text_input(
        "CAPEX Limit (USD)",
        value=shared_data.get("capex", "")
    )

    st.subheader("Available PV Surface Area")
    pv_area = st.text_input(
        "Available PV Surface Area (m²)",
        value=shared_data.get("pv_area", "")
    )

    st.subheader("Electrolyzer Type")
    electrolyzer_options = ["Alkaline", "PEM", "Evaluate All"]
    default_electrolyzer = shared_data.get("electrolyzer", "Alkaline")
    if default_electrolyzer not in electrolyzer_options:
        default_electrolyzer = "Alkaline"

    electrolyzer = st.selectbox(
        "Select Electrolyzer Type",
        options=electrolyzer_options,
        index=electrolyzer_options.index(default_electrolyzer)
    )

    st.subheader("Preferred Energy Source")
    energy_source_options = ["Solar", "Wind", "Optimize"]
    default_energy_source = shared_data.get("energy_source", "Solar")
    if default_energy_source not in energy_source_options:
        default_energy_source = "Solar"

    energy_source = st.selectbox(
        "Select Preferred Energy Source",
        options=energy_source_options,
        index=energy_source_options.index(default_energy_source)
    )

    st.subheader("Fixed Parameters")
    st.info("Discount Rate (%): 8.0")
    st.info("Project Lifetime (years): 20")

    shared_data["latitude"] = latitude
    shared_data["longitude"] = longitude
    shared_data["application_type"] = application_type
    shared_data["h2_output"] = h2_output
    shared_data["capex"] = capex
    shared_data["pv_area"] = pv_area
    shared_data["electrolyzer"] = electrolyzer
    shared_data["energy_source"] = energy_source
    shared_data["discount_rate"] = 8.0
    shared_data["project_lifetime"] = 20

    st.session_state.shared_data = shared_data

    if st.button("Next"):
        st.session_state.current_page = "Validation"
        st.rerun()