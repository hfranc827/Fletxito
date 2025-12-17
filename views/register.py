import flet as ft
import bcrypt
from app.db.connection import get_connection


def register_view(page: ft.Page):

    page.title = "Registro"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # =========================
    # INPUTS
    # =========================
    user = ft.TextField(
        label="Usuario",
        prefix_icon=ft.Icons.PERSON
    )

    email = ft.TextField(
        label="Email",
        prefix_icon=ft.Icons.EMAIL,
        keyboard_type=ft.KeyboardType.EMAIL
    )

    password = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK,
        password=True,
        can_reveal_password=True
    )

    # =========================
    # REGISTRAR
    # =========================
    def register(e):
        if not user.value or not email.value or not password.value:
            show_error("Completa todos los campos")
            return

        conn = get_connection()
        cursor = conn.cursor()

        # 🔹 Validar correo duplicado
        cursor.execute(
            "SELECT id FROM users WHERE email=%s",
            (email.value,)
        )
        if cursor.fetchone():
            conn.close()
            show_error("El correo ya está registrado")
            return

        # 🔹 Encriptar contraseña
        hashed_password = bcrypt.hashpw(
            password.value.encode(),
            bcrypt.gensalt()
        ).decode()

        # 🔹 Insertar usuario (USER)
        cursor.execute("""
            INSERT INTO users(username, email, password, role_id)
            VALUES (%s, %s, %s, %s)
        """, (user.value, email.value, hashed_password, 2))

        conn.commit()
        conn.close()

        page.snack_bar = ft.SnackBar(
            ft.Text("Registro exitoso"),
            bgcolor=ft.Colors.GREEN_400
        )
        page.snack_bar.open = True
        page.update()

        page.go("/")

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
                        ft.Icon(
                            ft.Icons.PERSON_ADD,
                            size=50,
                            color=ft.Colors.BLUE
                        ),
                        ft.Text(
                            "Crear cuenta",
                            size=24,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(
                            "Regístrate para continuar",
                            size=14,
                            color=ft.Colors.GREY
                        ),

                        user,
                        email,
                        password,

                        ft.ElevatedButton(
                            "Registrarse",
                            width=200,
                            height=45,
                            on_click=register
                        ),

                        ft.Divider(),

                        ft.TextButton(
                            "¿Ya tienes cuenta? Inicia sesión",
                            on_click=lambda _: page.go("/")
                        )
                    ]
                )
            )
        )
    )
