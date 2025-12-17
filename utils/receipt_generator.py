from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from app.db.connection import get_connection
import os

def generate_receipt(order_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Datos de la orden
    cursor.execute("""
        SELECT o.id, u.username, o.total, o.created_at
        FROM orders o
        JOIN users u ON o.user_id = u.id
        WHERE o.id = %s
    """, (order_id,))
    order = cursor.fetchone()

    # Detalles
    cursor.execute("""
        SELECT product_name, quantity, price
        FROM order_details
        WHERE order_id = %s
    """, (order_id,))
    items = cursor.fetchall()

    conn.close()

    os.makedirs("boletas", exist_ok=True)
    path = f"boletas/boleta_{order_id}.pdf"

    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "BOLETA DE VENTA")

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 90, f"Cliente: {order['username']}")
    c.drawString(50, height - 110, f"Orden N°: {order_id}")
    c.drawString(50, height - 130, f"Fecha: {order['created_at']}")

    y = height - 170
    c.setFont("Helvetica-Bold", 10)
    c.drawString(50, y, "Producto")
    c.drawString(250, y, "Cantidad")
    c.drawString(330, y, "Precio")
    c.drawString(420, y, "Subtotal")

    y -= 20
    c.setFont("Helvetica", 10)

    for item in items:
        subtotal = item["quantity"] * item["price"]
        c.drawString(50, y, item["product_name"])
        c.drawString(260, y, str(item["quantity"]))
        c.drawString(340, y, f"S/ {item['price']}")
        c.drawString(430, y, f"S/ {subtotal}")
        y -= 18

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawString(330, y, "TOTAL:")
    c.drawString(430, y, f"S/ {order['total']}")

    c.showPage()
    c.save()

    return path
