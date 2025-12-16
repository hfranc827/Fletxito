import flet as ft
from app.db.connection import get_connection
from app.components.navbar import navbar

def dashboard_view(page: ft.Page):

    if page.session.get("role") != "ADMIN":
        page.go("/home")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users")
    users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM products")
    products = cursor.fetchone()[0]

    conn.close()

    return ft.Column([
        navbar(page),
        ft.Text("Dashboard", size=30),
        ft.Text(f"Usuarios registrados: {users}"),
        ft.Text(f"Productos en catálogo: {products}")
    ])
