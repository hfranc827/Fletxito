import flet as ft
import bcrypt
from app.db.connection import get_connection


def login_view(page: ft.Page):

    page.title = "Login"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # =========================
    # INPUTS
    # =========================
    email = ft.TextField(
        label="Email",
        prefix_icon=ft.Icons.EMAIL,
        keyboard_type=ft.KeyboardType.EMAIL,
        autofocus=True
    )

    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True
    )

    # =========================
    # LOGIN
    # =========================
    def login(e):
        if not email.value or not password.value:
            show_error("Completa todos los campos")
            return

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, username, password, role_id
            FROM users
            WHERE email=%s
        """, (email.value,))

        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.value.encode(), user[2].encode()):
            page.session.set("user_id", user[0])
            page.session.set("username", user[1])
            page.session.set("role_id", user[3])

            page.go("/home")
        else:
            show_error("Email o contraseña incorrectos")

    def show_error(msg):
        page.snack_bar = ft.SnackBar(
            ft.Text(msg),
            bgcolor=ft.Colors.RED_400
        )
        page.snack_bar.open = True
        page.update()

    # =========================
    # UI
    # =========================
    return ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Card(
            elevation=6,
            content=ft.Container(
                width=360,
                padding=30,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Icon(ft.Icons.LOGIN, size=50, color=ft.Colors.BLUE),
                        ft.Text(
                            "Bienvenido",
                            size=24,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            "Ingresa tus credenciales",
                            size=14,
                            color=ft.Colors.GREY
                        ),

                        email,
                        password,

                        ft.ElevatedButton(
                            "Ingresar",
                            width=200,
                            height=45,
                            on_click=login
                        ),

                        ft.Divider(),

                        ft.TextButton(
                            "¿No tienes cuenta? Regístrate",
                            on_click=lambda _: page.go("/register")
                        )
                    ]
                )
            )
        )
    )
