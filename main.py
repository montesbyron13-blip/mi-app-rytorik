import flet as ft
from datetime import datetime

def calcular_local(com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos):
    ventas_efectivo = com_fisicas - pos
    efectivo_ideal = ventas_efectivo + caja_ini - salidas
    diferencia = efectivo_cont - efectivo_ideal
    estado_final = efectivo_cont - depositos
    return ventas_efectivo, efectivo_ideal, diferencia, estado_final

def calcular_total(pos_ventas, fondo_ini, salidas_total, estado_cuentas, pedidos_ya, retiro_fondos):
    ventas_totales = pos_ventas + pedidos_ya
    caja_ideal = pos_ventas + fondo_ini + pedidos_ya - salidas_total
    diferencia = estado_cuentas - caja_ideal
    estado_final_cuentas = estado_cuentas - retiro_fondos
    return ventas_totales, caja_ideal, diferencia, estado_final_cuentas

def safe_float(value):
    if value is None or value == "":
        return 0.0
    try:
        return float(str(value).replace(',', '.').strip())
    except ValueError:
        return 0.0

def main(page: ft.Page):
    page.title = "💰 Cierre de Caja"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Función para crear campos con eventos automáticos
    def crear_campo(label):
        return ft.TextField(
            label=label,
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=actualizar,
            on_blur=actualizar,
            on_submit=actualizar
        )

    # Campos locales
    com_fisicas = crear_campo("Comandas físicas")
    pos = crear_campo("POS")
    caja_ini = crear_campo("Caja inicial")
    salidas = crear_campo("Salidas dinero")
    efectivo_cont = crear_campo("Efectivo contado")
    depositos = crear_campo("Depósitos")

    # Campos totales
    pos_ventas = crear_campo("POS + ventas efectivo")
    fondo_ini = crear_campo("Fondo inicial")
    salidas_total = crear_campo("Salidas totales")
    estado_cuentas = crear_campo("Estado cuentas")
    pedidos_ya = crear_campo("Pedidos Ya")
    retiro_fondos = crear_campo("Retiro de fondos")

    # Resultados
    local_ventas = ft.Text("0.00")
    local_ideal = ft.Text("0.00")
    local_diferencia = ft.Text("0.00")
    local_estado = ft.Text("0.00")
    total_ventas = ft.Text("0.00")
    total_ideal = ft.Text("0.00")
    total_diferencia = ft.Text("0.00")
    total_estado_final_cuentas = ft.Text("0.00")

    def actualizar(e=None):
        # Local
        cf = safe_float(com_fisicas.value)
        p = safe_float(pos.value)
        ci = safe_float(caja_ini.value)
        sal = safe_float(salidas.value)
        ec = safe_float(efectivo_cont.value)
        dep = safe_float(depositos.value)
        v, i, d, e = calcular_local(cf, p, ci, sal, ec, dep)
        local_ventas.value = f"{v:,.2f}"
        local_ideal.value = f"{i:,.2f}"
        local_diferencia.value = f"{d:,.2f}"
        local_diferencia.color = ft.Colors.RED if d != 0 else ft.Colors.GREEN
        local_estado.value = f"{e:,.2f}"

        # Total
        pv = safe_float(pos_ventas.value)
        fi = safe_float(fondo_ini.value)
        st = safe_float(salidas_total.value)
        ec_total = safe_float(estado_cuentas.value)
        py = safe_float(pedidos_ya.value)
        rf = safe_float(retiro_fondos.value)
        vt, it, dt, ef = calcular_total(pv, fi, st, ec_total, py, rf)
        total_ventas.value = f"{vt:,.2f}"
        total_ideal.value = f"{it:,.2f}"
        total_diferencia.value = f"{dt:,.2f}"
        total_diferencia.color = ft.Colors.RED if dt != 0 else ft.Colors.GREEN
        total_estado_final_cuentas.value = f"{ef:,.2f}"
        page.update()

    def reset_local(e):
        com_fisicas.value = "0"
        pos.value = "0"
        caja_ini.value = "0"
        salidas.value = "0"
        efectivo_cont.value = "0"
        depositos.value = "0"
        actualizar()

    def reset_total(e):
        pos_ventas.value = "0"
        fondo_ini.value = "0"
        salidas_total.value = "0"
        estado_cuentas.value = "0"
        pedidos_ya.value = "0"
        retiro_fondos.value = "0"
        actualizar()

    def copiar_resultados(e):
        texto = f"""💰 CIERRE DE CAJA - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

🏪 LOCAL
Comandas físicas: {com_fisicas.value}
POS: {pos.value}
Caja inicial: {caja_ini.value}
Salidas dinero: {salidas.value}
Efectivo contado: {efectivo_cont.value}
Depósitos: {depositos.value}
Ventas efectivo: {local_ventas.value}
Efectivo ideal: {local_ideal.value}
Diferencia: {local_diferencia.value}
Estado final en caja: {local_estado.value}

💳 TOTAL
POS + ventas efectivo: {pos_ventas.value}
Fondo inicial: {fondo_ini.value}
Salidas totales: {salidas_total.value}
Estado cuentas: {estado_cuentas.value}
Pedidos Ya: {pedidos_ya.value}
Retiro de fondos: {retiro_fondos.value}
Ventas totales: {total_ventas.value}
Caja ideal: {total_ideal.value}
Diferencia: {total_diferencia.value}
Estado final de cuentas: {total_estado_final_cuentas.value}
"""
        page.set_clipboard(texto)
        page.snack_bar = ft.SnackBar(ft.Text("Resultados copiados al portapapeles"))
        page.snack_bar.open = True
        page.update()

    # Interfaz (sin botón recalcular)
    page.add(
        ft.Text("💰 CIERRE DE CAJA", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("🏪 CIERRE LOCAL", size=18, weight=ft.FontWeight.BOLD),
        com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos,
        ft.ElevatedButton("🔄 Resetear Local", on_click=reset_local),
        ft.Text("📊 Resultados Locales", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([ft.Text("Ventas efectivo:"), local_ventas]),
        ft.Row([ft.Text("Efectivo final (ideal):"), local_ideal]),
        ft.Row([ft.Text("Diferencia:"), local_diferencia]),
        ft.Row([ft.Text("Estado final en caja:"), local_estado]),
        ft.Divider(),
        ft.Text("💳 CIERRE TOTAL", size=18, weight=ft.FontWeight.BOLD),
        pos_ventas, fondo_ini, salidas_total, estado_cuentas, pedidos_ya, retiro_fondos,
        ft.Row([ft.ElevatedButton("🔄 Resetear Total", on_click=reset_total), ft.ElevatedButton("📋 Copiar resultados", on_click=copiar_resultados, icon=ft.icons.CONTENT_COPY)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Text("📊 Resultados Totales", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([ft.Text("Ventas totales:"), total_ventas]),
        ft.Row([ft.Text("Caja ideal:"), total_ideal]),
        ft.Row([ft.Text("Diferencia:"), total_diferencia]),
        ft.Row([ft.Text("Estado final de cuentas:"), total_estado_final_cuentas]),
    )
    actualizar()

ft.app(target=main)