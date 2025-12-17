import flet as ft
from app.db.connection import get_connection
from app.components.navbar import navbar
from datetime import date

def dashboard_view(page: ft.Page):

    # 🔐 Solo ADMIN
    if page.session.get("role_id") != 1:
        page.go("/home")
        return

    # =========================
    # DB
    # =========================
    conn = get_connection()
    cursor = conn.cursor()

    # VENTAS HOY
    cursor.execute("""
        SELECT IFNULL(SUM(total), 0)
        FROM orders
        WHERE DATE(created_at) = CURDATE()
    """)
    sales_today = cursor.fetchone()[0]

    # VENTAS SEMANA
    cursor.execute("""
        SELECT IFNULL(SUM(total), 0)
        FROM orders
        WHERE YEARWEEK(created_at, 1) = YEARWEEK(CURDATE(), 1)
    """)
    sales_week = cursor.fetchone()[0]

    # VENTAS MES
    cursor.execute("""
        SELECT IFNULL(SUM(total), 0)
        FROM orders
        WHERE MONTH(created_at) = MONTH(CURDATE())
        AND YEAR(created_at) = YEAR(CURDATE())
    """)
    sales_month = cursor.fetchone()[0]

    # PRODUCTOS VENDIDOS SEMANA
    cursor.execute("""
        SELECT IFNULL(SUM(quantity), 0)
        FROM order_details od
        JOIN orders o ON od.order_id = o.id
        WHERE YEARWEEK(o.created_at, 1) = YEARWEEK(CURDATE(), 1)
    """)
    products_week = cursor.fetchone()[0]

    # =========================
    # GRÁFICO SEMANAL
    # =========================
    cursor.execute("""
        SELECT DAYNAME(created_at) AS day, SUM(total)
        FROM orders
        WHERE YEARWEEK(created_at, 1) = YEARWEEK(CURDATE(), 1)
        GROUP BY day
    """)

    chart_data = {d: 0 for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]}
    for d, total in cursor.fetchall():
        chart_data[d[:3]] = float(total)

    conn.close()

    bar_groups = [
        ft.BarChartGroup(
            x=i,
            bar_rods=[ft.BarChartRod(from_y=0, to_y=value, width=20, color=ft.Colors.BLUE)]
        )
        for i, value in enumerate(chart_data.values())
    ]

    chart = ft.BarChart(
        bar_groups=bar_groups,
        left_axis=ft.ChartAxis(labels_size=40),
        bottom_axis=ft.ChartAxis(
            labels=[ft.ChartAxisLabel(value=i, label=ft.Text(day)) for i, day in enumerate(chart_data.keys())]
        ),
        expand=True,
        height=250
    )

    # =========================
    # KPI CARD FUNCIONES SEPARADAS
    # =========================
    def kpi_money(title, value, icon, color):
        return ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Icon(icon, size=30, color=color),
                        ft.Text(title, size=14, color=ft.Colors.GREY),
                        ft.Text(f"S/ {value:,.2f}", size=22, weight=ft.FontWeight.BOLD),
                    ]
                )
            )
        )

    def kpi_count(title, value, icon, color):
        return ft.Card(
            content=ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=8,
                    controls=[
                        ft.Icon(icon, size=30, color=color),
                        ft.Text(title, size=14, color=ft.Colors.GREY),
                        ft.Text(str(int(value)), size=22, weight=ft.FontWeight.BOLD),
                    ]
                )
            )
        )

    # =========================
    # UI
    # =========================
    return ft.Column(
        expand=True,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            navbar(page),

            ft.Container(
                padding=20,
                content=ft.Column(
                    spacing=25,
                    controls=[
                        ft.Text("Dashboard", size=28, weight=ft.FontWeight.BOLD),

                        # KPIs
                        ft.ResponsiveRow(
                            spacing=20,
                            controls=[
                                ft.Container(
                                    col={"xs": 12, "sm": 6, "md": 3},
                                    content=kpi_money("Ventas Hoy", sales_today, ft.Icons.TODAY, ft.Colors.GREEN)
                                ),
                                ft.Container(
                                    col={"xs": 12, "sm": 6, "md": 3},
                                    content=kpi_money("Ventas Semana", sales_week, ft.Icons.DATE_RANGE, ft.Colors.BLUE)
                                ),
                                ft.Container(
                                    col={"xs": 12, "sm": 6, "md": 3},
                                    content=kpi_money("Ventas Mes", sales_month, ft.Icons.CALENDAR_MONTH, ft.Colors.ORANGE)
                                ),
                                ft.Container(
                                    col={"xs": 12, "sm": 6, "md": 3},
                                    content=kpi_count("Unidades vendidas (semana)", products_week, ft.Icons.INVENTORY, ft.Colors.PURPLE)
                                ),
                            ]
                        ),

                        # GRÁFICO
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Ventas de la Semana", size=18, weight=ft.FontWeight.BOLD),
                                        chart
                                    ]
                                )
                            )
                        )
                    ]
                )
            )
        ]
    )
