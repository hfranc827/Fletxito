import flet as ft

def navbar(page: ft.Page):
    role_id = page.session.get("role_id")

    controls = [
        ft.Text(f"Usuario: {page.session.get('username')}")
    ]

    # ADMIN
    if role_id == 1:
        controls.append(
            ft.ElevatedButton("Dashboard", on_click=lambda _: page.go("/dashboard"))
        )
        controls.append(
            ft.ElevatedButton("Productos", on_click=lambda _: page.go("/products"))
        )

    # USER
    if role_id == 2:
        controls.append(
            ft.ElevatedButton("Catálogo", on_click=lambda _: page.go("/catalog"))
        )
        controls.append(
            ft.ElevatedButton("Carrito", on_click=lambda _: page.go("/cart"))
        )

    controls.append(
        ft.ElevatedButton("Salir", on_click=lambda _: logout(page))
    )

    return ft.Row(controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)


def logout(page):
    page.session.clear()
    page.go("/")
