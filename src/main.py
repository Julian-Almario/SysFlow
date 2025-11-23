import flet as ft
import requests
import threading
import time

BACKEND_URL = "http://192.168.1.130:5040/stats"

def main(page: ft.Page):
    page.title = "SysFlow"
    page.theme_mode = ft.ThemeMode.DARK

    normal_radius = 60
    used_color = ft.Colors.BLUE
    free_color = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)

    used_section = ft.PieChartSection(
        0,
        color=used_color,
        radius=normal_radius
    )

    free_section = ft.PieChartSection(
        100,
        color=free_color,
        radius=normal_radius
    )

    pie_chart = ft.PieChart(
        sections=[used_section, free_section],
        center_space_radius=45,
        expand=True,
    )

    percent_text = ft.Text(
        "0%",
        size=32,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.WHITE,
        text_align=ft.TextAlign.CENTER
    )

    label_text = ft.Text(
        "CPU",
        size=16,
        weight=ft.FontWeight.W_500,
        color=ft.Colors.WHITE70,
        text_align=ft.TextAlign.CENTER
    )

    center_content = ft.Column(
        [
            percent_text,
            label_text
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=2
    )

    chart_container = ft.Stack(
        [
            pie_chart,
            ft.Container(
                content=center_content,
                alignment=ft.alignment.center
            )
        ],
        width=200,
        height=200
    )

    page.add(chart_container)

    def update_loop():
        while True:
            try:
                r = requests.get(BACKEND_URL, timeout=2)
                data = r.json()
                cpu_percent = int(data["cpu"]

                used_section.value = cpu_percent
                free_section.value = 100 - cpu_percent

                percent_text.value = f"{cpu_percent}%"

                page.update()

            except Exception:
                percent_text.value = "ERR"
                page.update()

            time.sleep(1)

    threading.Thread(target=update_loop, daemon=True).start()

ft.app(target=main)

