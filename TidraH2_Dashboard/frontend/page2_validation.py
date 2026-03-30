import streamlit as st
from backend.data_fetcher import fetch_pvgis_hourly
from backend.wind_model_detailed import run_full_wind_model
from backend.solar_model_detailed import run_full_solar_model

def render():
    st.header("Step 2: Validating Site and Preparing Data")

    # Initialize shared data if missing
    if "shared_data" not in st.session_state:
        st.session_state.shared_data = {}

    shared_data = st.session_state.shared_data

    # Status placeholder
    status_placeholder = st.empty()

    status_placeholder.info("Step 2: Validating site and preparing data")

    if st.button("Validate Tech Data"):
        try:
            lat = float(shared_data.get("latitude", ""))
            lon = float(shared_data.get("longitude", ""))
            app_type = shared_data.get("application_type", "")
            h2_target = float(shared_data.get("h2_output", ""))
            capex = float(shared_data.get("capex", ""))
            pv_area = float(shared_data.get("pv_area", ""))
            electrolyzer_type = shared_data.get("electrolyzer", "")
        except ValueError:
            st.error("Please enter valid numeric inputs in Page 1.")
            return

        if not app_type or not electrolyzer_type:
            st.error("Please select valid options for application type and electrolyzer.")
            return

        # Step 2: Assign hub height
        hub_height = 60 if app_type == "Commercial" else 80

        # Step 3: Estimate energy need (kWh/year)
        efficiency_map = {"Alkaline": 0.65, "PEM": 0.58}
        default_eff = efficiency_map.get(electrolyzer_type, 0.6)
        energy_per_kg = 33.3 / default_eff
        annual_kWh = h2_target * energy_per_kg * 365

        # Step 4: Run wind model
        status_placeholder.info("Running wind energy model...")
        try:
            wind_result = run_full_wind_model(lat, lon, hub_height, annual_kWh)
        except Exception as e:
            st.error(f"Wind Modeling Error: {str(e)}")
            return

        # Step 5: Run solar model
        status_placeholder.info("Running solar energy model...")
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
            st.error(f"Solar Modeling Error: {str(e)}")
            return

        # Step 6: Fixed financial parameters
        discount_rate = 0.08
        lifetime = 20

        # Step 7: Store shared state
        shared_data.update({
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
            "lifetime": lifetime,
            "validation_complete": True
        })

        st.session_state.shared_data = shared_data

        status_placeholder.success("All data validated successfully.")

    # Next button only enabled after validation
    validation_complete = shared_data.get("validation_complete", False)

    if validation_complete:
        if st.button("Next"):
            st.session_state.current_page = "Simulation"
            st.rerun()
    else:
        st.button("Next", disabled=True)