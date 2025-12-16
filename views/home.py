import flet as ft
from app.components.navbar import navbar

def home_view(page: ft.Page):
    if not page.session.get("user_id"):
        page.go("/")
        return

    return ft.Column(
        [
            navbar(page),
            ft.Text("Sistema de Productos de Cómputo", size=25)
        ]
    )
