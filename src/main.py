import flet as ft
import requests
import threading
import time

BACKEND_URL = "http://192.168.1.130:5040/stats"

def main(page: ft.Page):
    page.title = "SysFlow"
    page.theme_mode = ft.ThemeMode.DARK

    normal_radius = 20
    free_color = ft.Colors.with_opacity(0.1, ft.Colors.WHITE)

    def create_resource_widget(label, used_color):
        used_section = ft.PieChartSection(0, color=used_color, radius=normal_radius)
        free_section = ft.PieChartSection(100, color=free_color, radius=normal_radius)

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
            text_align=ft.TextAlign.CENTER,
        )

        label_text = ft.Text(
            label,
            size=16,
            weight=ft.FontWeight.W_500,
            color=ft.Colors.WHITE70,
            text_align=ft.TextAlign.CENTER,
        )

        center_content = ft.Column(
            [percent_text, label_text],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=2,
        )

        container = ft.Stack(
            [
                pie_chart,
                ft.Container(content=center_content, alignment=ft.alignment.center),
            ],
            width=200,
            height=200,
        )

        return {
            "container": container,
            "used_section": used_section,
            "free_section": free_section,
            "percent_text": percent_text,
        }

    cpu_widget = create_resource_widget("CPU", ft.Colors.BLUE)
    ram_widget = create_resource_widget("RAM", ft.Colors.GREEN)

    page.add(
        ft.Column(
            [
                ft.Row(
                    [cpu_widget["container"], ram_widget["container"]],
                    alignment="center",
                    spacing=20,
                ),
            ],
            horizontal_alignment="center",
        )
    )

    def update_loop():
        while True:
            try:
                r = requests.get(BACKEND_URL, timeout=2)
                data = r.json()

                # CPU
                cpu = int(data["cpu"])
                cpu_widget["used_section"].value = cpu
                cpu_widget["free_section"].value = 100 - cpu
                cpu_widget["percent_text"].value = f"{cpu}%"

                # RAM
                ram = int(data["ram"])
                ram_widget["used_section"].value = ram
                ram_widget["free_section"].value = 100 - ram
                ram_widget["percent_text"].value = f"{ram}%"

                page.update()

            except Exception as e:
                print("Error:", e)
                cpu_widget["percent_text"].value = "ERR"
                ram_widget["percent_text"].value = "ERR"
                page.update()

            time.sleep(1)

    threading.Thread(target=update_loop, daemon=True).start()

ft.app(target=main, view=ft.WEB_BROWSER, port=8550)

