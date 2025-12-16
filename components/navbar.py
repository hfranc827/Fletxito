import flet as ft

def navbar(page: ft.Page):
    role = page.session.get("role")

    controls = [
        ft.Text(f"Usuario: {page.session.get('username')}")
    ]

    if role == "ADMIN":
        controls.append(ft.ElevatedButton("Dashboard", on_click=lambda _: page.go("/dashboard")))
        controls.append(ft.ElevatedButton("Productos", on_click=lambda _: page.go("/products")))

    if role == "USER":
        controls.append(ft.ElevatedButton("Catálogo", on_click=lambda _: page.go("/catalog")))

    controls.append(ft.ElevatedButton("Salir", on_click=lambda _: logout(page)))

    return ft.Row(controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

def logout(page):
    page.session.clear()
    page.go("/")
