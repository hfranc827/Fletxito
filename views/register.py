import flet as ft
import bcrypt
from app.db.connection import get_connection

def register_view(page: ft.Page):

    user = ft.TextField(label="Usuario")
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Contraseña", password=True)

    def register(e):
        conn = get_connection()
        cursor = conn.cursor()

        # 🔹 Validar correo duplicado
        cursor.execute("SELECT id FROM users WHERE email=%s", (email.value,))
        if cursor.fetchone():
            page.snack_bar = ft.SnackBar(ft.Text("El correo ya está registrado"))
            page.snack_bar.open = True
            page.update()
            conn.close()
            return

        # 🔹 Encriptar contraseña correctamente
        hashed_password = bcrypt.hashpw(
            password.value.encode(),
            bcrypt.gensalt()
        ).decode()

        # 🔹 Insertar usuario con rol USER (2)
        cursor.execute(
            "INSERT INTO users(username,email,password,role_id) VALUES(%s,%s,%s,%s)",
            (user.value, email.value, hashed_password, 2)
        )

        conn.commit()
        conn.close()

        page.snack_bar = ft.SnackBar(ft.Text("Registro exitoso"))
        page.snack_bar.open = True
        page.update()

        # 🔹 Redirigir al login
        page.go("/")

    return ft.Column(
        [
            ft.Text("Registro", size=30),
            user,
            email,
            password,
            ft.ElevatedButton("Registrar", on_click=register),
            ft.TextButton(
                "¿Ya tienes cuenta? Inicia sesión",
                on_click=lambda _: page.go("/")
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
