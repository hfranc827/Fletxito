import bcrypt
from app.db.connection import get_connection


def seed_admin():
    conn = get_connection()
    cursor = conn.cursor()

    # 1️⃣ Verificar si ya existe un ADMIN
    cursor.execute(
        "SELECT id FROM users WHERE role_id = 1 LIMIT 1"
    )
    if cursor.fetchone():
        conn.close()
        return  # Ya existe admin

    # 2️⃣ Crear contraseña segura
    password = "admin123"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    # 3️⃣ Insertar ADMIN
    cursor.execute("""
        INSERT INTO users (username, email, password, role_id)
        VALUES (%s, %s, %s, 1)
    """, (
        "Administrador",
        "admin@system.com",
        hashed
    ))

    conn.commit()
    conn.close()

    print("✅ Admin por defecto creado")
