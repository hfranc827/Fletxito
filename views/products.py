import flet as ft
from app.db.connection import get_connection
from app.components.navbar import navbar

def products_view(page: ft.Page):

    name = ft.TextField(label="Producto")
    price = ft.TextField(label="Precio")
    stock = ft.TextField(label="Stock")

    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Stock")),
        ],
        rows=[]
    )

    def load_products():
        table.rows.clear()
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        for p in cursor.fetchall():
            table.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(p[0])),
                    ft.DataCell(ft.Text(p[1])),
                    ft.DataCell(ft.Text(p[2])),
                    ft.DataCell(ft.Text(p[3])),
                ])
            )
        conn.close()
        page.update()

    def add_product(e):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products(name,price,stock) VALUES(%s,%s,%s)",
            (name.value, price.value, stock.value)
        )
        conn.commit()
        conn.close()
        load_products()

    load_products()

    return ft.Column(
        [
            navbar(page),
            name, price, stock,
            ft.ElevatedButton("Agregar", on_click=add_product),
            table
        ]
    )
