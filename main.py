import flet as ft
from datetime import datetime, date
import asyncio

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
            <tr><td>POS + ventas efectivo:</td><td class="right">{datos_total['pos_ventas']:,.2f}Zo</td></tr>
            <tr><td>Fondo inicial:</td><td class="right">{datos_total['fondo_ini']:,.2f}Zo</td></tr>
            <tr><td>Salidas totales:</td><td class="right">{datos_total['salidas']:,.2f}Zo</td></tr>
            <tr><td>Caja contada:</td><td class="right">{datos_total['caja_contada']:,.2f}Zo</td></tr>
            <tr><td>Pedidos Ya:</td><td class="right">{datos_total['pedidos_ya']:,.2f}Zo</td></tr>
            <tr><td>Depósitos:</td><td class="right">{datos_total['depositos']:,.2f}Zo</td></tr>
        </table>
        <div class="line"></div>
        <table>
            <tr><td><b>Ventas totales:</b>Zo<td class="right"><b>{datos_total['ventas_totales']:,.2f}</b>Zo</td></tr>
            <tr><td><b>Caja ideal:</b>Zo<td class="right"><b>{datos_total['caja_ideal']:,.2f}</b>Zo</td></tr>
            <tr><td><b>Diferencia:</b>Zo<td class="right"><b>{datos_total['diferencia']:,.2f}</b>Zo</td></tr>
            <tr><td><b>Estado cuentas:</b>Zo<td class="right"><b>{datos_total['estado_cuentas']:,.2f}</b>Zo</td></tr>
        </table>
        <div class="line"></div>
        <div class="center">✅ Cierre de Caja App</div>
    </body>
    </html>
    """
    return html

# ---------- APP PRINCIPAL ----------
def main(page: ft.Page):
    page.title = "💰 Cierre de Caja"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # ---- Variables de estado ----
    fecha_seleccionada = date.today()

    # Campos locales
    com_fisicas = ft.TextField(label="Comandas físicas", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    pos = ft.TextField(label="POS", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    caja_ini = ft.TextField(label="Caja inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    salidas = ft.TextField(label="Salidas de dinero", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    efectivo_cont = ft.TextField(label="Efectivo contado (real)", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    depositos = ft.TextField(label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER)

    # Campos totales
    pos_ventas = ft.TextField(label="POS y ventas en efectivo", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    fondo_ini = ft.TextField(label="Fondo inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    salidas_total = ft.TextField(label="Salidas de dinero (total)", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    caja_contada = ft.TextField(label="Caja contada (real)", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    pedidos_ya = ft.TextField(label="Pedidos Ya", value="0", keyboard_type=ft.KeyboardType.NUMBER)
    depositos_total = ft.TextField(label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER)

    # Resultados (Text)
    local_ventas = ft.Text("0.00", size=16, weight=ft.FontWeight.BOLD)
    local_ideal = ft.Text("0.00", size=16, weight=ft.FontWeight.BOLD)
    local_diferencia = ft.Text("0.00", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    local_estado = ft.Text("0.00", size=16, weight=ft.FontWeight.BOLD)

    total_ventas = ft.Text("0.00", size=16, weight=ft.FontWeight.BOLD)
    total_ideal = ft.Text("0.00", size=16, weight=ft.FontWeight.BOLD)
    total_diferencia = ft.Text("0.00", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
    total_estado = ft.Text("0.00", size=16, weight=ft.FontWeight.BOLD)

    # ---- Funciones de actualización ----
    def actualizar_todos(e=None):
        # Local
        try:
            cf = float(com_fisicas.value or 0)
        except:
            cf = 0
        try:
            p = float(pos.value or 0)
        except:
            p = 0
        try:
            ci = float(caja_ini.value or 0)
        except:
            ci = 0
        try:
            sal = float(salidas.value or 0)
        except:
            sal = 0
        try:
            ec = float(efectivo_cont.value or 0)
        except:
            ec = 0
        try:
            dep = float(depositos.value or 0)
        except:
            dep = 0

        v_ef, i_ef, dif_l, est_l = calcular_local(cf, p, ci, sal, ec, dep)
        local_ventas.value = f"{v_ef:,.2f}"
        local_ideal.value = f"{i_ef:,.2f}"
        local_diferencia.value = f"{dif_l:,.2f}"
        local_diferencia.color = ft.Colors.RED if dif_l != 0 else ft.Colors.GREEN
        local_estado.value = f"{est_l:,.2f}"

        # Total
        try:
            pv = float(pos_ventas.value or 0)
        except:
            pv = 0
        try:
            fi = float(fondo_ini.value or 0)
        except:
            fi = 0
        try:
            st = float(salidas_total.value or 0)
        except:
            st = 0
        try:
            cc = float(caja_contada.value or 0)
        except:
            cc = 0
        try:
            py = float(pedidos_ya.value or 0)
        except:
            py = 0
        try:
            dt = float(depositos_total.value or 0)
        except:
            dt = 0

        v_t, i_t, dif_t, est_t = calcular_total(pv, fi, st, cc, py, dt)
        total_ventas.value = f"{v_t:,.2f}"
        total_ideal.value = f"{i_t:,.2f}"
        total_diferencia.value = f"{dif_t:,.2f}"
        total_diferencia.color = ft.Colors.RED if dif_t != 0 else ft.Colors.GREEN
        total_estado.value = f"{est_t:,.2f}"

        page.update()

    # Asignar evento a todos los campos
    for campo in [com_fisicas, pos, caja_ini, salidas, efectivo_cont, depositos,
                  pos_ventas, fondo_ini, salidas_total, caja_contada, pedidos_ya, depositos_total]:
        campo.on_change = actualizar_todos

    # ---- Resets ----
    def reset_local(e):
        com_fisicas.value = "0"
        pos.value = "0"
        caja_ini.value = "0"
        salidas.value = "0"
        efectivo_cont.value = "0"
        depositos.value = "0"
        actualizar_todos()

    def reset_total(e):
        pos_ventas.value = "0"
        fondo_ini.value = "0"
        salidas_total.value = "0"
        caja_contada.value = "0"
        pedidos_ya.value = "0"
        depositos_total.value = "0"
        actualizar_todos()

    # ---- Exportar resultados (copiar al portapapeles) ----
    def copiar_resultados(e):
        texto = f"""💰 CIERRE DE CAJA - {fecha_seleccionada.strftime('%d/%m/%Y')} {datetime.now().strftime('%H:%M:%S')}

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

    # ---- Generar ticket HTML (guardar archivo y compartir) ----
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
        fecha_hora = datetime.combine(fecha_seleccionada, datetime.now().time())
        html = generar_html_ticket(datos_local, datos_total, fecha_hora)

        # Guardar en almacenamiento local del dispositivo (solo Android/iOS)
        import tempfile, os
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html)
                temp_path = f.name
            # En Android, abrir con el navegador usando webbrowser puede no funcionar, pero intentamos
            import webbrowser
            webbrowser.open(temp_path)
            page.snack_bar = ft.SnackBar(ft.Text("Ticket generado, se abrirá en el navegador"))
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ex}"))
        page.snack_bar.open = True
        page.update()

    # ---- Reloj en vivo (actualización cada segundo) ----
    reloj_text = ft.Text("", size=18, weight=ft.FontWeight.BOLD)

    async def actualizar_reloj():
        while True:
            ahora = datetime.now()
            reloj_text.value = f"🕒 {ahora.strftime('%d/%m/%Y %H:%M:%S')} (hora local)"
            page.update()
            await asyncio.sleep(1)

    # ---- Selector de fecha ----
    fecha_picker = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        on_change=lambda e: actualizar_fecha()
    )
    page.overlay.append(fecha_picker)

    fecha_text = ft.Text(fecha_seleccionada.strftime("%d/%m/%Y"), size=16)

    def actualizar_fecha():
        nonlocal fecha_seleccionada
        if fecha_picker.value:
            fecha_seleccionada = fecha_picker.value
            fecha_text.value = fecha_seleccionada.strftime("%d/%m/%Y")
            page.update()

    def mostrar_calendario(e):
        fecha_picker.pick_date()

    # ---- Construcción de la interfaz ----
    # Sección Local
    local_section = ft.Container(
        content=ft.Column([
            ft.Text("🏪 Cierre de Caja Local", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([ft.Column([com_fisicas, caja_ini, efectivo_cont, depositos]), ft.Column([pos, salidas])]),
            ft.ElevatedButton("🔄 Resetear Local", on_click=reset_local),
            ft.Divider(),
            ft.Text("📊 Resultados Locales", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([ft.Text("Ventas en efectivo:"), local_ventas]),
            ft.Row([ft.Text("Efectivo final (ideal):"), local_ideal]),
            ft.Row([ft.Text("Diferencia:"), local_diferencia]),
            ft.Row([ft.Text("Estado final en caja:"), local_estado]),
        ], spacing=10),
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=10,
    )

    # Sección Total
    total_section = ft.Container(
        content=ft.Column([
            ft.Text("💳 Cierre de Caja Total (Físico + Digital)", size=20, weight=ft.FontWeight.BOLD),
            ft.Row([ft.Column([pos_ventas, fondo_ini, caja_contada, depositos_total]), ft.Column([salidas_total, pedidos_ya])]),
            ft.ElevatedButton("🔄 Resetear Total", on_click=reset_total),
            ft.Divider(),
            ft.Text("📊 Resultados Totales", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([ft.Text("Ventas totales:"), total_ventas]),
            ft.Row([ft.Text("Caja ideal:"), total_ideal]),
            ft.Row([ft.Text("Diferencia:"), total_diferencia]),
            ft.Row([ft.Text("Estado final de cuentas:"), total_estado]),
        ], spacing=10),
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_300),
        border_radius=10,
    )

    # Botones de exportación
    export_buttons = ft.Row([
        ft.ElevatedButton("📋 Copiar resultados", on_click=copiar_resultados, icon=ft.icons.CONTENT_COPY),
        ft.ElevatedButton("🖨️ Generar Ticket HTML", on_click=generar_ticket, icon=ft.icons.PRINT),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    # Cabecera con fecha y reloj
    header = ft.Row([
        ft.ElevatedButton("📅 Seleccionar fecha", on_click=mostrar_calendario),
        ft.Text("Fecha: "),
        fecha_text,
    ], alignment=ft.MainAxisAlignment.START)

    # Añadir todo a la página
    page.add(reloj_text, header, local_section, total_section, export_buttons)

    # Iniciar tarea del reloj
    page.run_task(actualizar_reloj)

    # Calcular valores iniciales
    actualizar_todos()

ft.app(target=main)
