import flet as ft
from datetime import datetime
import urllib.parse

# ---------- Funciones de cálculo ----------
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
        return float(value)
    except ValueError:
        return 0.0

# ---------- Generar ticket HTML ----------
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
        <tr>
            <tr><td>Comandas físicas: </td><td class="right">{datos_local['com_fisicas']:,.2f} </td> </tr>
            <tr><td>POS:  </td><td class="right">{datos_local['pos']:,.2f} </td> </tr>
            <tr><td>Caja inicial:  </td><td class="right">{datos_local['caja_ini']:,.2f} </td> </tr>
            <tr><td>Salidas dinero:  </td><td class="right">{datos_local['salidas']:,.2f} </td> </tr>
            <tr><td>Efectivo contado:  </td><td class="right">{datos_local['efectivo_cont']:,.2f} </td> </tr>
            <tr><td>Depósitos:  </td><td class="right">{datos_local['depositos']:,.2f} </td> </tr>
        </table>
        <div class="line"></div>
        <table>
            <tr><td><b>Ventas efectivo:</b>  </td><td class="right"><b>{datos_local['ventas_efectivo']:,.2f}</b> </td> </tr>
            <tr><td><b>Efectivo ideal:</b>  </td><td class="right"><b>{datos_local['efectivo_ideal']:,.2f}</b> </td> </tr>
            <tr><td><b>Diferencia:</b>  </td><td class="right"><b>{datos_local['diferencia']:,.2f}</b> </td> </tr>
            <tr><td><b>Estado final caja:</b>  </td><td class="right"><b>{datos_local['estado_final']:,.2f}</b> </td> </tr>
        </table>
        <div class="line"></div>
        <div class="title">💳 CIERRE TOTAL</div>
        <table>
            <tr><td>POS + ventas efectivo:  </td><td class="right">{datos_total['pos_ventas']:,.2f} </td> </tr>
            <tr><td>Fondo inicial:  </td><td class="right">{datos_total['fondo_ini']:,.2f} </td> </tr>
            <tr><td>Salidas totales:  </td><td class="right">{datos_total['salidas']:,.2f} </td> </tr>
            <tr><td>Estado cuentas:  </td><td class="right">{datos_total['estado_cuentas']:,.2f} </td> </tr>
            <tr><td>Pedidos Ya:  </td><td class="right">{datos_total['pedidos_ya']:,.2f} </td> </tr>
            <tr><td>Retiro de fondos:  </td><td class="right">{datos_total['retiro_fondos']:,.2f} </td> </tr>
        </table>
        <div class="line"></div>
        <table>
            <tr><td><b>Ventas totales:</b>  </td><td class="right"><b>{datos_total['ventas_totales']:,.2f}</b> </td> </tr>
            <tr><td><b>Caja ideal:</b>  </td><td class="right"><b>{datos_total['caja_ideal']:,.2f}</b> </td> </tr>
            <tr><td><b>Diferencia:</b>  </td><td class="right"><b>{datos_total['diferencia']:,.2f}</b> </td> </tr>
            <tr><td><b>Estado final de cuentas:</b>  </td><td class="right"><b>{datos_total['estado_final_cuentas']:,.2f}</b> </td> </tr>
        </table>
        <div class="line"></div>
        <div class="center">✅ RytoriK 🔮 - Cierre de Caja</div>
    </body>
    </html>
    """
    return html

# ---------- APP PRINCIPAL ----------
def main(page: ft.Page):
    page.title = "RytoriK 🔮 - Cierre de Caja"  # Título en la barra superior (con emoji)
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # ========== ENCABEZADO CENTRADO ==========
    header = ft.Column(
        [
            ft.Text("RytoriK 🔮", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Text("Cierre de Caja", size=18, weight=ft.FontWeight.NORMAL, text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=5,
    )

    # --- Sección Local ---
    com_fisicas = ft.TextField(label="Comandas físicas", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    pos = ft.TextField(label="POS", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    caja_ini = ft.TextField(label="Caja inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    salidas = ft.TextField(label="Salidas dinero", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    efectivo_cont = ft.TextField(label="Efectivo contado", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    depositos = ft.TextField(label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER)

    # --- Sección Total ---
    pos_ventas = ft.TextField(label="POS + ventas efectivo", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    fondo_ini = ft.TextField(label="Fondo inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    salidas_total = ft.TextField(label="Salidas totales", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    estado_cuentas = ft.TextField(label="Estado cuentas", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    pedidos_ya = ft.TextField(label="Pedidos Ya", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    retiro_fondos = ft.TextField(label="Retiro de fondos", value="0", keyboard_type=ft.KeyboardType.NUMBER)

    # Resultados Locales
    local_ventas = ft.Text("0.00")
    local_ideal = ft.Text("0.00")
    local_diferencia = ft.Text("0.00")
    local_estado = ft.Text("0.00")

    # Resultados Totales
    total_ventas = ft.Text("0.00")
    total_ideal = ft.Text("0.00")
    total_diferencia = ft.Text("0.00")
    total_estado_final_cuentas = ft.Text("0.00")

    def actualizar(e):
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
        ec = safe_float(estado_cuentas.value)
        py = safe_float(pedidos_ya.value)
        rf = safe_float(retiro_fondos.value)
        vt, it, dt, ef = calcular_total(pv, fi, st, ec, py, rf)
        total_ventas.value = f"{vt:,.2f}"
        total_ideal.value = f"{it:,.2f}"
        total_diferencia.value = f"{dt:,.2f}"
        total_diferencia.color = ft.Colors.RED if dt != 0 else ft.Colors.GREEN
        total_estado_final_cuentas.value = f"{ef:,.2f}"

        page.update()

    for campo in [com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos,
                  pos_ventas, fondo_ini, salidas_total, estado_cuentas, pedidos_ya, retiro_fondos]:
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
        estado_cuentas.value = "0"
        pedidos_ya.value = "0"
        retiro_fondos.value = "0"
        actualizar(e)

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

    def ticket(e):
        cf = safe_float(com_fisicas.value)
        p = safe_float(pos.value)
        ci = safe_float(caja_ini.value)
        sal = safe_float(salidas.value)
        ec_local = safe_float(efectivo_cont.value)
        dep = safe_float(depositos.value)
        v_ef, i_ef, d_local, e_local = calcular_local(cf, p, ci, sal, ec_local, dep)

        pv = safe_float(pos_ventas.value)
        fi = safe_float(fondo_ini.value)
        st = safe_float(salidas_total.value)
        ec = safe_float(estado_cuentas.value)
        py = safe_float(pedidos_ya.value)
        rf = safe_float(retiro_fondos.value)
        vt, it, d_total, e_total = calcular_total(pv, fi, st, ec, py, rf)

        datos_local = {
            'com_fisicas': cf, 'pos': p, 'caja_ini': ci, 'salidas': sal,
            'efectivo_cont': ec_local, 'depositos': dep,
            'ventas_efectivo': v_ef, 'efectivo_ideal': i_ef,
            'diferencia': d_local, 'estado_final': e_local
        }
        datos_total = {
            'pos_ventas': pv, 'fondo_ini': fi, 'salidas': st,
            'estado_cuentas': ec, 'pedidos_ya': py, 'retiro_fondos': rf,
            'ventas_totales': vt, 'caja_ideal': it,
            'diferencia': d_total, 'estado_final_cuentas': e_total
        }
        fecha_hora = datetime.now()
        html = generar_html_ticket(datos_local, datos_total, fecha_hora)
        data_uri = "data:text/html;charset=utf-8," + urllib.parse.quote(html)
        page.launch_url(data_uri)
        page.snack_bar = ft.SnackBar(ft.Text("Ticket generado. Se abrirá en el navegador."))
        page.snack_bar.open = True
        page.update()

    # --- Interfaz de usuario con encabezado centrado ---
    page.add(
        header,  # Título centrado
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
        ft.ElevatedButton("🔄 Resetear Total", on_click=reset_total),
        ft.Text("📊 Resultados Totales", size=16, weight=ft.FontWeight.BOLD),
        ft.Row([ft.Text("Ventas totales:"), total_ventas]),
        ft.Row([ft.Text("Caja ideal:"), total_ideal]),
        ft.Row([ft.Text("Diferencia:"), total_diferencia]),
        ft.Row([ft.Text("Estado final de cuentas:"), total_estado_final_cuentas]),
        ft.Divider(),
        ft.Row([
            ft.ElevatedButton("📋 Copiar resultados", on_click=copiar_resultados, icon=ft.icons.CONTENT_COPY),
            ft.ElevatedButton("🧾 Imprimir ticket", on_click=ticket, icon=ft.icons.PRINT),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
    )
    actualizar(None)

ft.app(target=main)