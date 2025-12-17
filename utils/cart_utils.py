from app.db.connection import get_connection


def get_or_create_cart(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM cart WHERE user_id=%s", (user_id,))
    cart = cursor.fetchone()

    if cart:
        cart_id = cart[0]
    else:
        cursor.execute(
            "INSERT INTO cart(user_id) VALUES(%s)",
            (user_id,)
        )
        conn.commit()
        cart_id = cursor.lastrowid

    conn.close()
    return cart_id
