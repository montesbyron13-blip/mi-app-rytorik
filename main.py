import flet as ft
from datetime import datetime

def calcular_local(com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos):
    ventas_efectivo = com_fisicas - pos
    efectivo_ideal = ventas_efectivo + caja_ini - salidas
    diferencia = efectivo_cont - efectivo_ideal
    estado_final = efectivo_cont - depositos
    return ventas_efectivo, efectivo_ideal, diferencia, estado_final

def calcular_total(pos_ventas, fondo_ini, salidas_total, caja_contada, pedidos_ya, depositos_total):
    ventas_totales = pos_ventas + pedidos_ya
    caja_ideal = pos_ventas + fondo_ini + pedidos_ya - salidas_total
    diferencia = caja_contada - caja_ideal
    estado_cuentas = caja_contada - depositos_total
    return ventas_totales, caja_ideal, diferencia, estado_cuentas

def main(page: ft.Page):
    page.title = "💰 Cierre de Caja"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Campos locales
    com_fisicas = ft.TextField(label="Comandas físicas", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    pos = ft.TextField(label="POS", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    caja_ini = ft.TextField(label="Caja inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    salidas = ft.TextField(label="Salidas dinero", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    efectivo_cont = ft.TextField(label="Efectivo contado", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    depositos = ft.TextField(label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER)

    # Campos totales
    pos_ventas = ft.TextField(label="POS + ventas efectivo", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    fondo_ini = ft.TextField(label="Fondo inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    salidas_total = ft.TextField(label="Salidas totales", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    caja_contada = ft.TextField(label="Caja contada", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    pedidos_ya = ft.TextField(label="Pedidos Ya", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    depositos_total = ft.TextField(label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER)

    # Resultados
    local_ventas = ft.Text("0.00")
    local_ideal = ft.Text("0.00")
    local_diferencia = ft.Text("0.00")
    local_estado = ft.Text("0.00")
    total_ventas = ft.Text("0.00")
    total_ideal = ft.Text("0.00")
    total_diferencia = ft.Text("0.00")
    total_estado = ft.Text("0.00")

    def actualizar(e):
        # Local
        try:
            cf = float(com_fisicas.value or 0)
            p = float(pos.value or 0)
            ci = float(caja_ini.value or 0)
            sal = float(salidas.value or 0)
            ec = float(efectivo_cont.value or 0)
            dep = float(depositos.value or 0)
            v, i, d, e = calcular_local(cf, p, ci, sal, ec, dep)
            local_ventas.value = f"{v:,.2f}"
            local_ideal.value = f"{i:,.2f}"
            local_diferencia.value = f"{d:,.2f}"
            local_diferencia.color = ft.Colors.RED if d != 0 else ft.Colors.GREEN
            local_estado.value = f"{e:,.2f}"
        except: pass
        # Total
        try:
            pv = float(pos_ventas.value or 0)
            fi = float(fondo_ini.value or 0)
            st = float(salidas_total.value or 0)
            cc = float(caja_contada.value or 0)
            py = float(pedidos_ya.value or 0)
            dt = float(depositos_total.value or 0)
            vt, it, dt, et = calcular_total(pv, fi, st, cc, py, dt)
            total_ventas.value = f"{vt:,.2f}"
            total_ideal.value = f"{it:,.2f}"
            total_diferencia.value = f"{dt:,.2f}"
            total_diferencia.color = ft.Colors.RED if dt != 0 else ft.Colors.GREEN
            total_estado.value = f"{et:,.2f}"
        except: pass
        page.update()

    for campo in [com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos,
                  pos_ventas, fondo_ini, salidas_total, caja_contada, pedidos_ya, depositos_total]:
        campo.on_change = actualizar

    def reset_local(e):
        com_fisicas.value = "0"
        pos.value = "0"
        caja_ini.value = "0"
        salidas.value = "0"
        efectivo_cont.value = "0"
        depositos.value = "0"
        actualizar(e)

    def reset_total(e):
        pos_ventas.value = "0"
        fondo_ini.value = "0"
        salidas_total.value = "0"
        caja_contada.value = "0"
        pedidos_ya.value = "0"
        depositos_total.value = "0"
        actualizar(e)

    def copiar(e):
        texto = f"CIERRE - {datetime.now()}\nLocal: {local_ventas.value}\nTotal: {total_ventas.value}"
        page.set_clipboard(texto)
        page.snack_bar = ft.SnackBar(ft.Text("Copiado"))
        page.snack_bar.open = True
        page.update()

    # Construcción sencilla (sin responsiverow por ahora)
    page.add(
        ft.Text("💰 CIERRE DE CAJA", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("Local", size=18),
        com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos,
        ft.ElevatedButton("Reset Local", on_click=reset_local),
        ft.Text("Resultados:", weight=ft.FontWeight.BOLD),
        ft.Row([ft.Text("Ventas efectivo:"), local_ventas]),
        ft.Row([ft.Text("Diferencia:"), local_diferencia]),
        ft.Divider(),
        ft.Text("Total", size=18),
        pos_ventas, fondo_ini, salidas_total, caja_contada, pedidos_ya, depositos_total,
        ft.ElevatedButton("Reset Total", on_click=reset_total),
        ft.Text("Resultados Totales:"),
        ft.Row([ft.Text("Ventas totales:"), total_ventas]),
        ft.Row([ft.Text("Diferencia:"), total_diferencia]),
        ft.ElevatedButton("Copiar", on_click=copiar),
    )
    actualizar(None)

ft.app(target=main)