import flet as ft
from app.routes import route_change
from app.db.seed import seed_admin   # 👈 IMPORTANTE

def main(page: ft.Page):
    page.title = "Sistema de Productos de Cómputo"

    # 🔐 Crear ADMIN por defecto (solo si no existe)
    seed_admin()

    page.on_route_change = route_change
    page.go("/")

ft.app(target=main)
