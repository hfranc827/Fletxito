import flet as ft
from app.components.navbar import navbar
from app.utils.order_utils import confirm_order
from app.utils.receipt_generator import generate_receipt


def checkout_view(page: ft.Page):

    if page.session.get("role_id") != 2:
        page.go("/home")
        return

    def confirm(e):
        user_id = page.session.get("user_id")
        order_id = confirm_order(user_id)

        if order_id:
            generate_receipt(order_id)
            page.go("/home")

    return ft.Column([
        navbar(page),
        ft.Text("Confirmar Compra", size=28),
        ft.Text("¿Deseas finalizar la compra?"),
        ft.ElevatedButton("Confirmar y Generar Boleta", on_click=confirm)
    ])
