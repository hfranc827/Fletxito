import flet as ft
from app.db.connection import get_connection
from app.components.navbar import navbar

def catalog_view(page: ft.Page):

    if page.session.get("role") != "USER":
        page.go("/home")
        return

    products = ft.Column()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name, price, stock FROM products")
    
    for p in cursor.fetchall():
        products.controls.append(
            ft.Card(
                ft.Column([
                    ft.Text(p[0], size=18),
                    ft.Text(f"Precio: S/ {p[1]}"),
                    ft.Text(f"Stock: {p[2]}"),
                    ft.ElevatedButton("Comprar")
                ])
            )
        )

    conn.close()

    return ft.Column([navbar(page), products])
