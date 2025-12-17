import flet as ft
from app.db.connection import get_connection
from app.components.navbar import navbar


def cart_view(page: ft.Page):

    # 🔐 Solo USER
    if page.session.get("role_id") != 2:
        page.go("/home")
        return

    user_id = page.session.get("user_id")

    items_column = ft.Column(spacing=15)
    total_text = ft.Text(size=20, weight=ft.FontWeight.BOLD)

    # =========================
    # CARGAR CARRITO
    # =========================
    def load_cart():
        items_column.controls.clear()
        total = 0

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT ci.id, p.name, ci.quantity, ci.price
            FROM cart_items ci
            JOIN cart c ON ci.cart_id = c.id
            JOIN products p ON ci.product_id = p.id
            WHERE c.user_id=%s
        """, (user_id,))

        for item_id, name, qty, price in cursor.fetchall():
            subtotal = qty * price
            total += subtotal

            items_column.controls.append(
                ft.Card(
                    ft.Container(
                        padding=15,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                # INFO PRODUCTO
                                ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.Text(name, size=18, weight=ft.FontWeight.BOLD),
                                        ft.Text(f"S/ {price}", color=ft.Colors.GREY),
                                    ]
                                ),

                                # CONTROLES
                                ft.Row(
                                    spacing=5,
                                    controls=[
                                        ft.IconButton(
                                            ft.Icons.REMOVE,
                                            on_click=lambda e, iid=item_id: update_qty(iid, -1)
                                        ),
                                        ft.Text(str(qty), size=16),
                                        ft.IconButton(
                                            ft.Icons.ADD,
                                            on_click=lambda e, iid=item_id: update_qty(iid, 1)
                                        ),
                                    ]
                                ),

                                # SUBTOTAL
                                ft.Text(
                                    f"S/ {subtotal:.2f}",
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),

                                # DELETE
                                ft.IconButton(
                                    ft.Icons.DELETE,
                                    icon_color="red",
                                    on_click=lambda e, iid=item_id: remove_item(iid)
                                )
                            ]
                        )
                    )
                )
            )

        conn.close()

        total_text.value = f"Total: S/ {total:.2f}"
        page.update()

    # =========================
    # UPDATE QTY
    # =========================
    def update_qty(item_id, delta):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE cart_items SET quantity = quantity + %s WHERE id=%s",
            (delta, item_id)
        )
        cursor.execute(
            "DELETE FROM cart_items WHERE id=%s AND quantity <= 0",
            (item_id,)
        )

        conn.commit()
        conn.close()
        load_cart()

    # =========================
    # REMOVE ITEM
    # =========================
    def remove_item(item_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM cart_items WHERE id=%s", (item_id,))
        conn.commit()
        conn.close()
        load_cart()

    load_cart()

    # =========================
    # UI
    # =========================
    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            navbar(page),

            ft.Text("Mi Carrito", size=28, weight=ft.FontWeight.BOLD),

            items_column,

            ft.Card(
                ft.Container(
                    padding=20,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            total_text,
                            ft.ElevatedButton(
                                "Confirmar compra",
                                icon=ft.Icons.CHECK_CIRCLE,
                                on_click=lambda e: page.go("/checkout")
                            )
                        ]
                    )
                )
            )
        ]
    )
