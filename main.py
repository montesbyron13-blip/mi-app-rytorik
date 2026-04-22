import flet as ft

def main(page: ft.Page):
    page.title = "Test"
    page.add(ft.Text("Hola mundo, si ves esto, Flet funciona"))

ft.app(target=main)