# backend/report_generator.py

import os
from datetime import datetime
from fpdf import FPDF
from backend.charts_generator import (
    create_kpi_dashboard,
    create_line_chart,
    create_bar_chart,
    create_pie_chart,
    create_radar_chart,
)

FONT_FOLDER = "fonts"
FONT_NAME = "DejaVu"

class PDFReport(FPDF):
    def __init__(self):
        super().__init__()
        # Register DejaVu font with Unicode support
        self.add_font(FONT_NAME, "", os.path.join(FONT_FOLDER, "DejaVuSans.ttf"), uni=True)
        self.add_font(FONT_NAME, "B", os.path.join(FONT_FOLDER, "DejaVuSans-Bold.ttf"), uni=True)
        self.set_font(FONT_NAME, "", 10)

    def header(self):
        if os.path.exists("assets/tidrah2_logo.png"):
            self.image("assets/tidrah2_logo.png", 10, 8, 33)
        self.set_font(FONT_NAME, "B", 12)
        self.set_xy(50, 10)
        self.cell(0, 10, "TidraH2 Simulation Report", ln=True, align="C")
        self.set_font(FONT_NAME, "", 9)
        self.set_xy(50, 18)
        self.cell(0, 10, datetime.now().strftime("Generated on %B %d, %Y at %H:%M"), ln=True, align="C")
        self.ln(5)

    def chapter_title(self, title):
        self.set_font(FONT_NAME, "B", 11)
        self.set_text_color(20, 60, 150)
        self.cell(0, 8, title, ln=True)
        self.set_text_color(0, 0, 0)
        self.ln(1)

    def chapter_body(self, text):
        self.set_font(FONT_NAME, "", 10)
        self.multi_cell(0, 5, text)
        self.ln()

    def insert_image(self, path, w=160, h=0):
        if os.path.exists(path):
            self.image(path, w=w, h=h)
            self.ln(5)

def generate_report(sim_data, output_path="TidraH2_Report.pdf"):
    pdf = PDFReport()
    pdf.add_page()

    # Section 1 – Executive Summary
    pdf.chapter_title("1. Executive Summary")
    summary = (
        f"This report summarizes the hydrogen production scenario simulated for a "
        f"{sim_data['electrolyzer']} electrolyzer powered by {sim_data['source']} energy.\n"
        f"Expected hydrogen production is {sim_data['kg_year']:.0f} kg/year, with an LCOH of "
        f"{sim_data.get('lcoh', 0):.2f} €/kg and a scenario score of {sim_data.get('score', 0):.2f}.\n"
    )
    pdf.chapter_body(summary)

    # Section 2 – Input Configuration Overview
    pdf.chapter_title("2. Input Configuration Overview")
    config_text = (
        f"Electrolyzer: {sim_data['electrolyzer']}\n"
        f"Energy Source: {sim_data['source']}\n"
        f"Target Output: {sim_data['kg_year']:.0f} kg/year\n"
        f"CAPEX: {sim_data.get('capex', 'N/A')} EUR\n"
        f"OPEX: {0.05 * float(sim_data.get('capex', 0)):.0f} EUR/year\n"
        f"Discount Rate: {sim_data.get('discount_rate', 0.08) * 100:.1f}%\n"
        f"Project Lifetime: {sim_data.get('lifetime', 20)} years\n"
    )
    pdf.chapter_body(config_text)

    # Section 3 – Performance KPIs
    pdf.chapter_title("3. Performance KPIs")
    kpi_path = "kpi_dashboard.png"
    kpis = {
        "Hydrogen (kg/yr)": sim_data["kg_year"],
        "LCOH (€/kg)": sim_data.get("lcoh", 0),
        "CAPEX (€)": sim_data.get("capex", 0),
        "OPEX (€)": 0.05 * float(sim_data.get("capex", 0)),
        "Score": sim_data.get("score", 0),
    }
    create_kpi_dashboard(kpis, kpi_path)
    pdf.insert_image(kpi_path)

    # Section 4 – Technical Performance Analysis
    pdf.chapter_title("4. Technical Performance Analysis")
    pdf.chapter_body("This section displays the hydrogen output trend and energy source breakdown.")
    if "hybrid_summary" in sim_data:
        bar_path = "energy_breakdown.png"
        labels = ["Solar", "Wind"]
        values = [
            sim_data["hybrid_summary"].get("E_solar_used", 0),
            sim_data["hybrid_summary"].get("E_wind_used", 0),
        ]
        create_bar_chart(labels, values, "Energy Source Contribution", "kWh", bar_path)
        pdf.insert_image(bar_path)

    # Section 5 – Economic Analysis
    pdf.chapter_title("5. Economic Analysis")
    pie_path = "cost_structure.png"
    create_pie_chart(
        labels=["CAPEX", "OPEX"],
        sizes=[sim_data.get("capex", 0), 0.05 * float(sim_data.get("capex", 0))],
        title="Cost Structure",
        save_path=pie_path,
    )
    pdf.insert_image(pie_path)

    # Section 6 – Environmental & SDG Impact
    pdf.chapter_title("6. Environmental & SDG Impact")
    pdf.chapter_body(
        f"CO₂ Offset: {sim_data.get('co2_saved', 0):,.0f} kg\n"
        f"Jobs Created: {sim_data.get('jobs', 0):,.1f}\n"
        f"GDP Impact: €{sim_data.get('gdp_impact', 0):,.0f}\n"
    )

    radar_path = "sdg_radar.png"
    sdg_dict = sim_data.get("sdg_scores", {"SDG 7": 85, "SDG 8": 70, "SDG 13": 90})
    categories = list(sdg_dict.keys())
    values = list(sdg_dict.values())
    create_radar_chart(
        categories=categories,
        values=values,
        title="SDG Impact Score (normalized)",
        save_path=radar_path
    )
    pdf.insert_image(radar_path)

    pdf.output(output_path)
    return output_path
