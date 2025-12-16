import flet as ft
import bcrypt
from app.db.connection import get_connection

def login_view(page: ft.Page):

    email = ft.TextField(label="Email")
    password = ft.TextField(label="Contraseña", password=True)

    def login(e):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.id, u.username, u.password, r.name
            FROM users u
            JOIN roles r ON u.role_id = r.id
            WHERE u.email=%s
        """, (email.value,))

        user = cursor.fetchone()
        conn.close()

        if user and bcrypt.checkpw(password.value.encode(), user[2].encode()):
            page.session.set("user_id", user[0])
            page.session.set("username", user[1])
            page.session.set("role", user[3])  # 🔥 CLAVE

            page.go("/home")
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Credenciales incorrectas"))
            page.snack_bar.open = True
            page.update()

    return ft.Column(
        [
            ft.Text("Login", size=30),
            email,
            password,
            ft.ElevatedButton("Ingresar", on_click=login),
            ft.TextButton(
                "Registrarse",
                on_click=lambda _: page.go("/register")
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
