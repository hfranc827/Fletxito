import flet as ft
from app.db.connection import get_connection
from app.components.navbar import navbar
from app.utils.cart_utils import get_or_create_cart


def catalog_view(page: ft.Page):

    # 🔐 Solo USER
    if page.session.get("role_id") != 2:
        page.go("/home")
        return

    # =========================
    # ESTADO FILTROS
    # =========================
    selected_category = ft.Ref[int]()
    selected_category.current = None

    # =========================
    # FILTROS SIDEBAR
    # =========================
    search = ft.TextField(
        label="Buscar",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: load_products()
    )

    price_min = ft.TextField(label="Precio mín", keyboard_type=ft.KeyboardType.NUMBER)
    price_max = ft.TextField(label="Precio máx", keyboard_type=ft.KeyboardType.NUMBER)

    # =========================
    # GRID
    # =========================
    grid = ft.ResponsiveRow(spacing=20)

    # =========================
    # COMPRAR
    # =========================
    def buy_product(pid):
        user_id = page.session.get("user_id")
        cart_id = get_or_create_cart(user_id)

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id FROM cart_items
            WHERE cart_id=%s AND product_id=%s
        """, (cart_id, pid))

        item = cursor.fetchone()

        if item:
            cursor.execute(
                "UPDATE cart_items SET quantity = quantity + 1 WHERE id=%s",
                (item[0],)
            )
        else:
            cursor.execute("""
                INSERT INTO cart_items(cart_id, product_id, quantity, price)
                SELECT %s, id, 1, price FROM products WHERE id=%s
            """, (cart_id, pid))

        conn.commit()
        conn.close()

        page.snack_bar = ft.SnackBar(ft.Text("Producto agregado al carrito"))
        page.snack_bar.open = True
        page.update()

    # =========================
    # CARGAR PRODUCTOS (con filtros)
    # =========================
    def load_products():
        grid.controls.clear()

        query = """
            SELECT p.id, p.name, p.price, p.stock, c.name AS category
            FROM products p
            JOIN categories c ON p.category_id = c.id
            WHERE p.stock > 0
        """
        params = []

        if search.value:
            query += " AND p.name LIKE %s"
            params.append(f"%{search.value}%")

        if selected_category.current:
            query += " AND p.category_id = %s"
            params.append(selected_category.current)

        if price_min.value:
            query += " AND p.price >= %s"
            params.append(price_min.value)

        if price_max.value:
            query += " AND p.price <= %s"
            params.append(price_max.value)

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)

        for p in cursor.fetchall():
            grid.controls.append(
                ft.Container(
                    col={"xs": 12, "sm": 6, "md": 4, "lg": 3},
                    content=ft.Card(
                        ft.Container(
                            padding=15,
                            content=ft.Column(
                                spacing=8,
                                controls=[
                                    ft.Text(p["name"], size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(p["category"], color="grey"),
                                    ft.Text(f"S/ {p['price']}", size=16),
                                    ft.Text(f"Stock: {p['stock']}"),
                                    ft.ElevatedButton(
                                        "Comprar",
                                        icon=ft.Icons.SHOPPING_CART,
                                        on_click=lambda e, pid=p["id"]: buy_product(pid)
                                    )
                                ]
                            )
                        )
                    )
                )
            )

        conn.close()
        page.update()

    # =========================
    # SIDEBAR
    # =========================
    def set_category(cid):
        selected_category.current = cid
        load_products()

    sidebar = ft.Container(
        width=260,
        padding=15,
        bgcolor=ft.Colors.GREY_100,
        content=ft.Column(
            spacing=15,
            controls=[
                ft.Text("Filtros", size=20, weight=ft.FontWeight.BOLD),

                search,

                ft.Text("Categorías"),
                ft.ListTile(title=ft.Text("Laptops"), on_click=lambda e: set_category(1)),
                ft.ListTile(title=ft.Text("Teclados"), on_click=lambda e: set_category(2)),
                ft.ListTile(title=ft.Text("Mouse"), on_click=lambda e: set_category(3)),
                ft.ListTile(title=ft.Text("Monitores"), on_click=lambda e: set_category(4)),
                ft.ListTile(title=ft.Text("Accesorios"), on_click=lambda e: set_category(5)),

                ft.Divider(),
                price_min,
                price_max,
                ft.ElevatedButton("Aplicar filtros", on_click=lambda e: load_products()),
                ft.TextButton(
                    "Limpiar filtros",
                    on_click=lambda e: clear_filters()
                )
            ]
        )
    )

    def clear_filters():
        search.value = ""
        price_min.value = ""
        price_max.value = ""
        selected_category.current = None
        load_products()

    # =========================
    # INIT
    # =========================
    load_products()

    # =========================
    # UI FINAL
    # =========================
    return ft.Column(
        expand=True,
        controls=[
            navbar(page),

            ft.Row(
                expand=True,
                controls=[
                    sidebar,

                    ft.Container(
                        expand=True,
                        padding=20,
                        content=ft.Column(
                            scroll=ft.ScrollMode.AUTO,
                            controls=[
                                ft.Text(
                                    "Catálogo de Productos",
                                    size=26,
                                    weight=ft.FontWeight.BOLD
                                ),
                                grid
                            ]
                        )
                    )
                ]
            )
        ]
    )
