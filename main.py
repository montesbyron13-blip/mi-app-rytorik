import flet as ft

def main(page: ft.Page):
    page.title = "Test"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.padding = 20

    mensaje = ft.Text(
        "Hola mundo, Flet funciona correctamente",
        size=24,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )
    page.add(mensaje)

ft.app(target=main)