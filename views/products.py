import flet as ft
from app.db.connection import get_connection
from app.components.navbar import navbar


def products_view(page: ft.Page):

    # 🔐 Solo ADMIN
    if page.session.get("role_id") != 1:
        page.go("/home")
        return

    # =========================
    # INPUTS
    # =========================
    name = ft.TextField(label="Producto", expand=True)
    description = ft.TextField(label="Descripción", expand=True)
    price = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    stock = ft.TextField(label="Stock", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    category_id = ft.TextField(label="ID Categoría", keyboard_type=ft.KeyboardType.NUMBER, expand=True)

    # =========================
    # TABLA
    # =========================
    table = ft.DataTable(
        expand=True,
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )

    selected_category = None  # Filtrado por categoría

    # =========================
    # CARGAR PRODUCTOS
    # =========================
    def load_products(category=None):
        table.rows.clear()
        conn = get_connection()
        cursor = conn.cursor()

        if category:
            cursor.execute("""
                SELECT id, name, price, stock 
                FROM products 
                WHERE category_id=%s
            """, (category,))
        else:
            cursor.execute("SELECT id, name, price, stock FROM products")

        for p in cursor.fetchall():
            table.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p[0])),
                        ft.DataCell(ft.Text(p[1])),
                        ft.DataCell(ft.Text(f"S/ {p[2]:,.2f}")),
                        ft.DataCell(ft.Text(p[3])),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color="red",
                                on_click=lambda e, pid=p[0]: delete_product(pid)
                            )
                        ),
                    ]
                )
            )
        conn.close()
        page.update()

    # =========================
    # AGREGAR PRODUCTO
    # =========================
    def add_product(e):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO products(name, description, price, stock, category_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            name.value,
            description.value,
            float(price.value),
            int(stock.value),
            int(category_id.value)
        ))

        conn.commit()
        conn.close()

        name.value = description.value = price.value = stock.value = category_id.value = ""
        load_products(selected_category)

    # =========================
    # ELIMINAR
    # =========================
    def delete_product(pid):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id=%s", (pid,))
        conn.commit()
        conn.close()
        load_products(selected_category)

    # =========================
    # CARGAR CATEGORÍAS
    # =========================
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories")
    categories = cursor.fetchall()
    conn.close()

    # =========================
    # BOTONES DE FILTRO
    # =========================
    def filter_by_category(e, cat_id):
        nonlocal selected_category
        selected_category = cat_id
        load_products(selected_category)

    category_buttons = [
        ft.ElevatedButton(
            cat[1],
            on_click=lambda e, cid=cat[0]: filter_by_category(e, cid),
            style=ft.ButtonStyle(bgcolor=ft.Colors.LIGHT_BLUE_100)
        )
        for cat in categories
    ]
    # Botón para mostrar todos
    category_buttons.insert(0, ft.ElevatedButton(
        "Todos",
        on_click=lambda e: filter_by_category(e, None),
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREY_300)
    ))

    # =========================
    # CARGAR INICIAL
    # =========================
    load_products()

    # =========================
    # UI
    # =========================
    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            navbar(page),

            ft.Text("Gestión de Productos", size=28, weight=ft.FontWeight.BOLD),

            # FORMULARIO
            ft.Card(
                ft.Container(
                    padding=20,
                    content=ft.ResponsiveRow(
                        controls=[
                            name,
                            description,
                            price,
                            stock,
                            category_id,
                            ft.Container(
                                col={"xs": 12},
                                content=ft.ElevatedButton(
                                    "Agregar Producto",
                                    icon=ft.Icons.ADD,
                                    on_click=add_product
                                )
                            ),
                        ],
                        columns=12
                    )
                )
            ),

            # FILTRO DE CATEGORÍAS
            ft.Container(
                padding=10,
                content=ft.Row(
                    spacing=10,
                    wrap=True,
                    controls=category_buttons
                )
            ),

            # TABLA CON SCROLL
            ft.Container(
                expand=True,
                content=ft.Column(
                    scroll=ft.ScrollMode.AUTO,
                    controls=[table]
                )
            )
        ]
    )
