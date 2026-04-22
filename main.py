import flet as ft
from datetime import datetime, date
import urllib.parse

# ---------- Funciones de cálculo ----------
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

# ---------- APP PRINCIPAL ----------
def main(page: ft.Page):
    # Configuración responsiva
    page.title = "💰 Cierre de Caja"
    page.padding = 10
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_max_width = 500  # En escritorio se ve como móvil
    page.window_center()

    # ---- Fecha seleccionada ----
    fecha_actual = date.today()
    fecha_text = ft.Text(fecha_actual.strftime("%d/%m/%Y"), size=14)

    # ---- Reloj en vivo (intervalo 1s) ----
    reloj_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)

    def actualizar_reloj(e):
        ahora = datetime.now()
        reloj_text.value = f"🕒 {ahora.strftime('%d/%m/%Y %H:%M:%S')} (hora local)"
        page.update()

    page.add_interval(1000, actualizar_reloj)

    # ---- Selector de fecha ----
    def fecha_cambiada(e):
        nonlocal fecha_actual
        if date_picker.value:
            fecha_actual = date_picker.value
            fecha_text.value = fecha_actual.strftime("%d/%m/%Y")
            page.update()

    date_picker = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        on_change=fecha_cambiada
    )
    page.overlay.append(date_picker)

    def mostrar_calendario(e):
        date_picker.pick_date()

    # ---- Campos de entrada (todos con keyboard numérico) ----
    # Locales
    com_fisicas = ft.TextField(label="Comandas físicas", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    pos = ft.TextField(label="POS", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    caja_ini = ft.TextField(label="Caja inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    salidas = ft.TextField(label="Salidas dinero", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    efectivo_cont = ft.TextField(label="Efectivo contado", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    depositos = ft.TextField(label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    # Totales
    pos_ventas = ft.TextField(label="POS + ventas efectivo", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    fondo_ini = ft.TextField(label="Fondo inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    salidas_total = ft.TextField(label="Salidas totales", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    caja_contada = ft.TextField(label="Caja contada", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    pedidos_ya = ft.TextField(label="Pedidos Ya", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    depositos_total = ft.TextField(label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER)

    # Resultados (Text)
    local_ventas = ft.Text("0.00")
    local_ideal = ft.Text("0.00")
    local_diferencia = ft.Text("0.00")
    local_estado = ft.Text("0.00")
    total_ventas = ft.Text("0.00")
    total_ideal = ft.Text("0.00")
    total_diferencia = ft.Text("0.00")
    total_estado = ft.Text("0.00")

    # ---- Actualizar todos los cálculos ----
    def actualizar_todo(e):
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

    # Asignar evento a todos los campos
    for campo in [com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos,
                  pos_ventas, fondo_ini, salidas_total, caja_contada, pedidos_ya, depositos_total]:
        campo.on_change = actualizar_todo

    # ---- Resets ----
    def reset_local(e):
        com_fisicas.value = "0"
        pos.value = "0"
        caja_ini.value = "0"
        salidas.value = "0"
        efectivo_cont.value = "0"
        depositos.value = "0"
        actualizar_todo(e)

    def reset_total(e):
        pos_ventas.value = "0"
        fondo_ini.value = "0"
        salidas_total.value = "0"
        caja_contada.value = "0"
        pedidos_ya.value = "0"
        depositos_total.value = "0"
        actualizar_todo(e)

    # ---- Copiar resultados al portapapeles ----
    def copiar_resultados(e):
        texto = f"""💰 CIERRE DE CAJA - {fecha_actual.strftime('%d/%m/%Y')} {datetime.now().strftime('%H:%M:%S')}

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
        page.snack_bar = ft.SnackBar(ft.Text("Resultados copiados al portapapeles"))
        page.snack_bar.open = True
        page.update()

    # ---- Generar ticket HTML y abrir en navegador ----
    def generar_ticket(e):
        # Obtener datos actuales
        cf = float(com_fisicas.value or 0)
        p = float(pos.value or 0)
        ci = float(caja_ini.value or 0)
        sal = float(salidas.value or 0)
        ec = float(efectivo_cont.value or 0)
        dep = float(depositos.value or 0)
        v_ef, i_ef, dif_l, est_l = calcular_local(cf, p, ci, sal, ec, dep)

        pv = float(pos_ventas.value or 0)
        fi = float(fondo_ini.value or 0)
        st = float(salidas_total.value or 0)
        cc = float(caja_contada.value or 0)
        py = float(pedidos_ya.value or 0)
        dt = float(depositos_total.value or 0)
        v_t, i_t, dif_t, est_t = calcular_total(pv, fi, st, cc, py, dt)

        datos_local = {
            'com_fisicas': cf, 'pos': p, 'caja_ini': ci, 'salidas': sal,
            'efectivo_cont': ec, 'depositos': dep,
            'ventas_efectivo': v_ef, 'efectivo_ideal': i_ef,
            'diferencia': dif_l, 'estado_final': est_l
        }
        datos_total = {
            'pos_ventas': pv, 'fondo_ini': fi, 'salidas': st,
            'caja_contada': cc, 'pedidos_ya': py, 'depositos': dt,
            'ventas_totales': v_t, 'caja_ideal': i_t,
            'diferencia': dif_t, 'estado_cuentas': est_t
        }
        fecha_hora = datetime.combine(fecha_actual, datetime.now().time())
        html = generar_html_ticket(datos_local, datos_total, fecha_hora)

        # Data URI para abrir en navegador
        data_uri = "data:text/html;charset=utf-8," + urllib.parse.quote(html)
        page.launch_url(data_uri)

        page.snack_bar = ft.SnackBar(ft.Text("Ticket generado, se abrirá en el navegador"))
        page.snack_bar.open = True
        page.update()

    # ---- Construcción de la interfaz responsiva ----
    main_content = ft.SafeArea(
        expand=True,
        content=ft.Column(
            [
                ft.Row([reloj_text], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.ElevatedButton("📅 Seleccionar fecha", on_click=mostrar_calendario, expand=True),
                    ft.Text("Fecha: ", size=14),
                    fecha_text,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Divider(),
                ft.Text("🏪 CIERRE DE CAJA LOCAL", size=20, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    [
                        ft.Column(
                            [com_fisicas, caja_ini, efectivo_cont, depositos],
                            col={"xs": 12, "sm": 6},
                        ),
                        ft.Column(
                            [pos, salidas],
                            col={"xs": 12, "sm": 6},
                        ),
                    ],
                ),
                ft.ElevatedButton("🔄 Resetear Local", on_click=reset_local, expand=True),
                ft.Text("Resultados Locales", size=16, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    [
                        ft.Column([ft.Text("Ventas en efectivo:"), local_ventas], col={"xs": 12, "sm": 6}),
                        ft.Column([ft.Text("Efectivo final (ideal):"), local_ideal], col={"xs": 12, "sm": 6}),
                        ft.Column([ft.Text("Diferencia:"), local_diferencia], col={"xs": 12, "sm": 6}),
                        ft.Column([ft.Text("Estado final en caja:"), local_estado], col={"xs": 12, "sm": 6}),
                    ],
                ),
                ft.Divider(),
                ft.Text("💳 CIERRE DE CAJA TOTAL", size=20, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    [
                        ft.Column(
                            [pos_ventas, fondo_ini, caja_contada, depositos_total],
                            col={"xs": 12, "sm": 6},
                        ),
                        ft.Column(
                            [salidas_total, pedidos_ya],
                            col={"xs": 12, "sm": 6},
                        ),
                    ],
                ),
                ft.ElevatedButton("🔄 Resetear Total", on_click=reset_total, expand=True),
                ft.Text("Resultados Totales", size=16, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    [
                        ft.Column([ft.Text("Ventas totales:"), total_ventas], col={"xs": 12, "sm": 6}),
                        ft.Column([ft.Text("Caja ideal:"), total_ideal], col={"xs": 12, "sm": 6}),
                        ft.Column([ft.Text("Diferencia:"), total_diferencia], col={"xs": 12, "sm": 6}),
                        ft.Column([ft.Text("Estado final de cuentas:"), total_estado], col={"xs": 12, "sm": 6}),
                    ],
                ),
                ft.Divider(),
                ft.ResponsiveRow(
                    [
                        ft.Column(
                            [ft.ElevatedButton("📋 Copiar resultados", on_click=copiar_resultados, icon=ft.icons.CONTENT_COPY, expand=True)],
                            col={"xs": 12, "sm": 6},
                        ),
                        ft.Column(
                            [ft.ElevatedButton("🖨️ Generar Ticket HTML", on_click=generar_ticket, icon=ft.icons.PRINT, expand=True)],
                            col={"xs": 12, "sm": 6},
                        ),
                    ],
                ),
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO,
        ),
    )

    page.add(main_content)
    actualizar_todo(None)

ft.app(target=main)