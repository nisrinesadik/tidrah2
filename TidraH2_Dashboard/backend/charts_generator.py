
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

def create_kpi_dashboard(kpi_dict, save_path):
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.axis("off")
    table_data = [[k, f"{v:.2f}" if isinstance(v, (float, int)) else v] for k, v in kpi_dict.items()]
    table = ax.table(cellText=table_data, colLabels=["KPI", "Value"], loc="center", cellLoc="left")
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.2, 1.2)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def create_line_chart(x, y, title, xlabel, ylabel, save_path):
    plt.figure(figsize=(6, 3))
    plt.plot(x, y, color="teal", linewidth=1.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def create_bar_chart(categories, values, title, ylabel, save_path):
    plt.figure(figsize=(6, 3))
    plt.bar(categories, values, color="skyblue")
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def create_pie_chart(labels, sizes, title, save_path):
    plt.figure(figsize=(5, 5))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def create_radar_chart(categories, values, title, save_path):
    labels = np.array(categories)
    values += values[:1]
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
    ax.plot(angles, values, color="green", linewidth=2)
    ax.fill(angles, values, color="green", alpha=0.25)
    ax.set_yticklabels([])
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    plt.title(title, y=1.1)
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()
