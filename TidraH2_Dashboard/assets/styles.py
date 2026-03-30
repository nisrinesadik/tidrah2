import streamlit as st

def load_custom_styles():
    st.markdown("""
    <style>
    .stApp {
        background-color: #F7F9FC;
    }

    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #102A43;
        margin-bottom: 0.2rem;
    }

    .subtitle-text {
        font-size: 1rem;
        color: #486581;
        margin-bottom: 1.5rem;
    }

    .section-card {
        background-color: white;
        padding: 1.4rem 1.4rem 1.2rem 1.4rem;
        border-radius: 16px;
        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
        margin-bottom: 1.2rem;
        border: 1px solid #E6EDF5;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #12344D;
        margin-bottom: 0.8rem;
    }

    .kpi-box {
        background: linear-gradient(135deg, #FFFFFF 0%, #F1F5F9 100%);
        padding: 1rem;
        border-radius: 14px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
        text-align: center;
    }

    .kpi-title {
        font-size: 0.9rem;
        color: #486581;
        margin-bottom: 0.3rem;
    }

    .kpi-value {
        font-size: 1.4rem;
        font-weight: 700;
        color: #102A43;
    }

    .hero-box {
        background: linear-gradient(135deg, #0F766E 0%, #155E75 100%);
        padding: 1.5rem;
        border-radius: 18px;
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.95;
    }

    .small-note {
        font-size: 0.9rem;
        color: #64748B;
        margin-top: 0.3rem;
    }

    div.stButton > button {
        border-radius: 10px;
        padding: 0.55rem 1.2rem;
        font-weight: 600;
        border: none;
    }

    div[data-testid="stSidebar"] {
        background-color: #EEF3F8;
    }

    label, .stSelectbox label, .stTextInput label, .stNumberInput label {
        font-weight: 600;
        color: #243B53;
    }
    </style>
    """, unsafe_allow_html=True)