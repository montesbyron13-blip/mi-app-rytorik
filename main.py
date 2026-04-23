import flet as ft
from datetime import datetime
import urllib.parse

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

def generar_html_ticket(datos_local, datos_total, fecha_hora):
    now_str = fecha_hora.strftime("%d/%m/%Y %H:%M:%S")
    html = f"""
    <html>
    <head><meta charset="UTF-8"><style>
        @media print {{ body {{ margin: 0; padding: 0; }} }}
        body {{ font-family: monospace; font-size: 12px; width: 80mm; padding: 5mm; margin: 0 auto; }}
        .center {{ text-align: center; }}
        .line {{ border-top: 1px dashed #000; margin: 5px 0; }}
        table {{ width: 100%; }}
        td {{ padding: 2px 0; }}
        .right {{ text-align: right; }}
        .title {{ font-weight: bold; font-size: 14px; margin: 5px 0; }}
    </style></head>
    <body>
        <div class="center"><b>💰 CIERRE DE CAJA</b><br/>{now_str}</div>
        <div class="line"></div>
        <div class="title">🏪 CIERRE LOCAL</div>
        <table>
            <tr><td>Comandas físicas:</td><td class="right">{datos_local['com_fisicas']:,.2f}</td></tr>
            <tr><td>POS:</td><td class="right">{datos_local['pos']:,.2f}</td></tr>
            <tr><td>Caja inicial:</td><td class="right">{datos_local['caja_ini']:,.2f}</td></tr>
            <tr><td>Salidas dinero:</td><td class="right">{datos_local['salidas']:,.2f}</td></tr>
            <tr><td>Efectivo contado:</td><td class="right">{datos_local['efectivo_cont']:,.2f}</td></tr>
            <tr><td>Depósitos:</td><td class="right">{datos_local['depositos']:,.2f}</td></tr>
        </table>
        <div class="line"></div>
        <table>
            <tr><td><b>Ventas efectivo:</b></td><td class="right"><b>{datos_local['ventas_efectivo']:,.2f}</b></td></tr>
            <tr><td><b>Efectivo ideal:</b></td><td class="right"><b>{datos_local['efectivo_ideal']:,.2f}</b></td></tr>
            <tr><td><b>Diferencia:</b></td><td class="right"><b>{datos_local['diferencia']:,.2f}</b></td></tr>
            <tr><td><b>Estado final caja:</b></td><td class="right"><b>{datos_local['estado_final']:,.2f}</b></td></tr>
        </table>
        <div class="line"></div>
        <div class="title">💳 CIERRE TOTAL</div>
        <table>
            <tr><td>POS + ventas efectivo:</td><td class="right">{datos_total['pos_ventas']:,.2f}</td></tr>
            <tr><td>Fondo inicial:</td><td class="right">{datos_total['fondo_ini']:,.2f}</td></tr>
            <tr><td>Salidas totales:</td><td class="right">{datos_total['salidas']:,.2f}</td></tr>
            <tr><td>Caja contada:</td><td class="right">{datos_total['caja_contada']:,.2f}</td></tr>
            <tr><td>Pedidos Ya:</td><td class="right">{datos_total['pedidos_ya']:,.2f}</td></tr>
            <tr><td>Depósitos:</td><td class="right">{datos_total['depositos']:,.2f}</td></tr>
        </table>
        <div class="line"></div>
        <table>
            <tr><td><b>Ventas totales:</b></td><td class="right"><b>{datos_total['ventas_totales']:,.2f}</b></td></tr>
            <tr><td><b>Caja ideal:</b></td><td class="right"><b>{datos_total['caja_ideal']:,.2f}</b></td></tr>
            <tr><td><b>Diferencia:</b></td><td class="right"><b>{datos_total['diferencia']:,.2f}</b></td></tr>
            <tr><td><b>Estado cuentas:</b></td><td class="right"><b>{datos_total['estado_cuentas']:,.2f}</b></td></tr>
        </table>
        <div class="line"></div>
        <div class="center">✅ Cierre de Caja App</div>
    </body>
    </html>
    """
    return html

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
Estado final caja: {local_estado.value}

💳 TOTAL
POS + ventas efectivo: {pos_ventas.value}
Fondo inicial: {fondo_ini.value}
Salidas totales: {salidas_total.value}
Caja contada: {caja_contada.value}
Pedidos Ya: {pedidos_ya.value}
Depósitos: {depositos_total.value}
Ventas totales: {total_ventas.value}
Caja ideal: {total_ideal.value}
Diferencia: {total_diferencia.value}
Estado cuentas: {total_estado.value}
"""
        page.set_clipboard(texto)
        page.snack_bar = ft.SnackBar(ft.Text("Resultados copiados"))
        page.snack_bar.open = True
        page.update()

    def ticket(e):
        cf = float(com_fisicas.value or 0)
        p = float(pos.value or 0)
        ci = float(caja_ini.value or 0)
        sal = float(salidas.value or 0)
        ec = float(efectivo_cont.value or 0)
        dep = float(depositos.value or 0)
        v_ef, i_ef, d_local, e_local = calcular_local(cf, p, ci, sal, ec, dep)
        pv = float(pos_ventas.value or 0)
        fi = float(fondo_ini.value or 0)
        st = float(salidas_total.value or 0)
        cc = float(caja_contada.value or 0)
        py = float(pedidos_ya.value or 0)
        dt = float(depositos_total.value or 0)
        vt, it, d_total, e_total = calcular_total(pv, fi, st, cc, py, dt)
        datos_local = {
            'com_fisicas': cf, 'pos': p, 'caja_ini': ci, 'salidas': sal,
            'efectivo_cont': ec, 'depositos': dep,
            'ventas_efectivo': v_ef, 'efectivo_ideal': i_ef,
            'diferencia': d_local, 'estado_final': e_local
        }
        datos_total = {
            'pos_ventas': pv, 'fondo_ini': fi, 'salidas': st,
            'caja_contada': cc, 'pedidos_ya': py, 'depositos': dt,
            'ventas_totales': vt, 'caja_ideal': it,
            'diferencia': d_total, 'estado_cuentas': e_total
        }
        fecha_hora = datetime.now()
        html = generar_html_ticket(datos_local, datos_total, fecha_hora)
        data_uri = "data:text/html;charset=utf-8," + urllib.parse.quote(html)
        page.launch_url(data_uri)
        page.snack_bar = ft.SnackBar(ft.Text("Ticket generado, se abrirá en el navegador"))
        page.snack_bar.open = True
        page.update()

    # Interfaz
    page.add(
        ft.Text("💰 CIERRE DE CAJA", size=24, weight=ft.FontWeight.BOLD),
        ft.Divider(),
        ft.Text("🏪 LOCAL", size=18, weight=ft.FontWeight.BOLD),
        com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos,
        ft.ElevatedButton("🔄 Resetear Local", on_click=reset_local),
        ft.Text("📊 Resultados Locales", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([ft.Text("Ventas efectivo:"), local_ventas]),
        ft.Row([ft.Text("Efectivo final (ideal):"), local_ideal]),
        ft.Row([ft.Text("Diferencia:"), local_diferencia]),
        ft.Row([ft.Text("Estado final en caja:"), local_estado]),
        ft.Divider(),
        ft.Text("💳 TOTAL", size=18, weight=ft.FontWeight.BOLD),
        pos_ventas, fondo_ini, salidas_total, caja_contada, pedidos_ya, depositos_total,
        ft.ElevatedButton("🔄 Resetear Total", on_click=reset_total),
        ft.Text("📊 Resultados Totales", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([ft.Text("Ventas totales:"), total_ventas]),
        ft.Row([ft.Text("Caja ideal:"), total_ideal]),
        ft.Row([ft.Text("Diferencia:"), total_diferencia]),
        ft.Row([ft.Text("Estado final de cuentas:"), total_estado]),
        ft.Divider(),
        ft.Row([
            ft.ElevatedButton("📋 Copiar resultados", on_click=copiar, icon=ft.icons.CONTENT_COPY),
            ft.ElevatedButton("🧾 Imprimir ticket", on_click=ticket, icon=ft.icons.PRINT),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
    )
    actualizar(None)

ft.app(target=main)