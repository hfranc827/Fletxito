import flet as ft
from app.routes import route_change

def main(page: ft.Page):
    page.title = "Sistema de Productos de Cómputo"
    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
