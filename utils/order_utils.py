from app.db.connection import get_connection


def confirm_order(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    # 1️⃣ Obtener carrito
    cursor.execute("SELECT id FROM cart WHERE user_id=%s", (user_id,))
    cart = cursor.fetchone()

    if not cart:
        conn.close()
        return None

    cart_id = cart[0]

    # 2️⃣ Obtener productos del carrito
    cursor.execute("""
        SELECT ci.product_id, p.name, ci.quantity, ci.price
        FROM cart_items ci
        JOIN products p ON ci.product_id = p.id
        WHERE ci.cart_id=%s
    """, (cart_id,))

    items = cursor.fetchall()
    if not items:
        conn.close()
        return None

    total = sum(q * price for _, _, q, price in items)

    # 3️⃣ Crear order
    cursor.execute("""
        INSERT INTO orders(user_id, total, status)
        VALUES (%s, %s, 'COMPLETADO')
    """, (user_id, total))

    order_id = cursor.lastrowid

    # 4️⃣ Crear order_details + descontar stock
    for pid, name, qty, price in items:
        cursor.execute("""
            INSERT INTO order_details(order_id, product_name, quantity, price)
            VALUES (%s, %s, %s, %s)
        """, (order_id, name, qty, price))

        cursor.execute("""
            UPDATE products SET stock = stock - %s WHERE id=%s
        """, (qty, pid))

    # 5️⃣ Vaciar carrito
    cursor.execute("DELETE FROM cart_items WHERE cart_id=%s", (cart_id,))

    conn.commit()
    conn.close()

    return order_id
