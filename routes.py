import flet as ft
from app.views.catalog import catalog_view
from app.views.dashboard import dashboard_view
from app.views.home import home_view
from app.views.login import login_view
from app.views.products import products_view
from app.views.register import register_view
from app.views.cart import cart_view   # ✅ OK
from app.views.checkout import checkout_view



def route_change(e):
    page = e.page
    page.views.clear()

    role_id = page.session.get("role_id")

    if page.route == "/products" and role_id != 1:
        page.go("/home")
        return

    if page.route == "/dashboard" and role_id != 1:
        page.go("/home")
        return

    if page.route in ["/catalog", "/cart"] and role_id != 2:
        page.go("/home")
        return

    routes = {
        "/": login_view,
        "/register": register_view,
        "/home": home_view,
        "/catalog": catalog_view,
        "/cart": cart_view,        # 🔥 FALTABA
        "/checkout": checkout_view,   # 🔥 FALTABA
        "/dashboard": dashboard_view,
        "/products": products_view
    }

    view = routes.get(page.route)

    page.views.append(
        ft.View(page.route, [view(page)])
    )
    page.update()
