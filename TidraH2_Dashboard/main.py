import streamlit as st
from assets.styles import load_custom_styles

# --------------------------------------------------
# Page configuration
# --------------------------------------------------
st.set_page_config(
    page_title="TidraH2",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# Load custom CSS styles
# --------------------------------------------------
load_custom_styles()

# --------------------------------------------------
# Initialize session state
# --------------------------------------------------
if "shared_data" not in st.session_state:
    st.session_state.shared_data = {}

if "current_page" not in st.session_state:
    st.session_state.current_page = "Inputs"

# --------------------------------------------------
# Navigation setup
# --------------------------------------------------
pages = ["Inputs", "Validation", "Simulation", "Results"]

# Ensure current page is always valid
if st.session_state.current_page not in pages:
    st.session_state.current_page = "Inputs"

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    try:
        st.image("assets/tidrah2_logo.png", width=95)
    except Exception:
        pass

    st.markdown("## TidraH2")
    st.caption("Hydrogen planning and territorial intelligence platform")

    st.markdown("---")

    selected_page = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state.current_page)
    )

    st.markdown("---")

    shared_data = st.session_state.shared_data

    if shared_data:
        st.markdown("### Project Snapshot")

        if shared_data.get("latitude") and shared_data.get("longitude"):
            st.write(f"**Site:** {shared_data.get('latitude')}, {shared_data.get('longitude')}")

        if shared_data.get("application_type"):
            st.write(f"**Application:** {shared_data.get('application_type')}")

        if shared_data.get("electrolyzer"):
            st.write(f"**Electrolyzer:** {shared_data.get('electrolyzer')}")

        if shared_data.get("energy_source"):
            st.write(f"**Energy Source:** {shared_data.get('energy_source')}")

        if shared_data.get("h2_output"):
            st.write(f"**H₂ Target:** {shared_data.get('h2_output')} kg/day")

# Keep sidebar and page state synchronized
st.session_state.current_page = selected_page

# --------------------------------------------------
# Hero section
# --------------------------------------------------
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">TidraH2</div>
        <div class="hero-subtitle">
            Territorial Interface for Dakhla’s Renewable Advancement.<br>
            A professional decision-support platform for evaluating hydrogen production scenarios
            using solar, wind, and hybrid systems.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Top summary KPIs
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="kpi-box">
            <div class="kpi-title">Region Focus</div>
            <div class="kpi-value">Dakhla</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="kpi-box">
            <div class="kpi-title">Scenario Types</div>
            <div class="kpi-value">3</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="kpi-box">
            <div class="kpi-title">Key SDGs</div>
            <div class="kpi-value">7 · 8 · 13</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="kpi-box">
            <div class="kpi-title">Output</div>
            <div class="kpi-value">PDF Report</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)

# --------------------------------------------------
# Page router
# --------------------------------------------------
if st.session_state.current_page == "Inputs":
    from frontend.page1_inputs import render
    render()

elif st.session_state.current_page == "Validation":
    from frontend.page2_validation import render
    render()

elif st.session_state.current_page == "Simulation":
    from frontend.page3_simulation import render
    render()

elif st.session_state.current_page == "Results":
    from frontend.page4_results import render
    render()