# main.py

import streamlit as st

st.set_page_config(
    page_title="TidraH2",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("TidraH2: Territorial Interface for Dakhla’s Renewable Advancement")
st.write("Interactive platform for evaluating hydrogen production scenarios using solar, wind, and hybrid systems.")

# Initialize shared data storage in Streamlit session state
if "shared_data" not in st.session_state:
    st.session_state.shared_data = {}

# Sidebar navigation
page = st.sidebar.radio(
    "Navigation",
    ["Inputs", "Validation", "Simulation", "Results"]
)

# Route to pages
if page == "Inputs":
    from frontend.page1_inputs import render
    render()

elif page == "Validation":
    from frontend.page2_validation import render
    render()

elif page == "Simulation":
    from frontend.page3_simulation import render
    render()

elif page == "Results":
    from frontend.page4_results import render
    render()