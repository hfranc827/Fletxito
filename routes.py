import flet as ft

from app.views.login import login_view
from app.views.register import register_view
from app.views.home import home_view
from app.views.catalog import catalog_view
from app.views.dashboard import dashboard_view
from app.views.products import products_view


def route_change(e: ft.RouteChangeEvent):
    page = e.page

    page.views.clear()

    routes = {
        "/": login_view,
        "/register": register_view,
        "/home": home_view,
        "/catalog": catalog_view,
        "/dashboard": dashboard_view,
        "/products": products_view
    }

    view = routes.get(page.route)

    if view:
        page.views.append(
            ft.View(
                route=page.route,
                controls=[view(page)]
            )
        )
    else:
        page.views.append(
            ft.View(
                route="/404",
                controls=[ft.Text("Página no encontrada")]
            )
        )

    page.update()
