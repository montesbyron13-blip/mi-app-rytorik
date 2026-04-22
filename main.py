import flet as ft
from datetime import datetime, date
import re
import io
import base64

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

# ---------- Componentes de la app ----------
def main(page: ft.Page):
    page.title = "💰 Cierre de Caja"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # ---- Estado de la app ----
    # Fecha seleccionada (por defecto hoy)
    fecha_cierre = date.today()

    # Valores locales
    local_com_fisicas = ft.Ref[ft.TextField]()
    local_pos = ft.Ref[ft.TextField]()
    local_caja_ini = ft.Ref[ft.TextField]()
    local_salidas = ft.Ref[ft.TextField]()
    local_efectivo_cont = ft.Ref[ft.TextField]()
    local_depositos = ft.Ref[ft.TextField]()

    # Valores totales
    total_pos_ventas = ft.Ref[ft.TextField]()
    total_fondo_ini = ft.Ref[ft.TextField]()
    total_salidas = ft.Ref[ft.TextField]()
    total_caja_contada = ft.Ref[ft.TextField]()
    total_pedidos_ya = ft.Ref[ft.TextField]()
    total_depositos = ft.Ref[ft.TextField]()

    # Resultados (etiquetas)
    local_ventas_efectivo = ft.Ref[ft.Text]()
    local_efectivo_ideal = ft.Ref[ft.Text]()
    local_diferencia = ft.Ref[ft.Text]()
    local_estado_final = ft.Ref[ft.Text]()

    total_ventas_totales = ft.Ref[ft.Text]()
    total_caja_ideal = ft.Ref[ft.Text]()
    total_diferencia = ft.Ref[ft.Text]()
    total_estado_cuentas = ft.Ref[ft.Text]()

    # ---- Funciones auxiliares ----
    def actualizar_todo(e=None):
        # Leer valores locales
        try:
            com = float(local_com_fisicas.current.value or 0)
        except: com = 0
        try:
            p = float(local_pos.current.value or 0)
        except: p = 0
        try:
            ci = float(local_caja_ini.current.value or 0)
        except: ci = 0
        try:
            sal = float(local_salidas.current.value or 0)
        except: sal = 0
        try:
            ec = float(local_efectivo_cont.current.value or 0)
        except: ec = 0
        try:
            dep = float(local_depositos.current.value or 0)
        except: dep = 0

        ventas_ef, ideal_ef, dif_local, estado_local = calcular_local(com, p, ci, sal, ec, dep)
        local_ventas_efectivo.current.value = f"{ventas_ef:,.2f}"
        local_efectivo_ideal.current.value = f"{ideal_ef:,.2f}"
        local_diferencia.current.value = f"{dif_local:,.2f}"
        local_estado_final.current.value = f"{estado_local:,.2f}"
        # Color según diferencia
        local_diferencia.current.color = ft.Colors.RED if dif_local != 0 else ft.Colors.GREEN

        # Leer valores totales
        try:
            pv = float(total_pos_ventas.current.value or 0)
        except: pv = 0
        try:
            fi = float(total_fondo_ini.current.value or 0)
        except: fi = 0
        try:
            stot = float(total_salidas.current.value or 0)
        except: stot = 0
        try:
            cc = float(total_caja_contada.current.value or 0)
        except: cc = 0
        try:
            py = float(total_pedidos_ya.current.value or 0)
        except: py = 0
        try:
            dtot = float(total_depositos.current.value or 0)
        except: dtot = 0

        vt, ideal_t, dif_total, estado_total = calcular_total(pv, fi, stot, cc, py, dtot)
        total_ventas_totales.current.value = f"{vt:,.2f}"
        total_caja_ideal.current.value = f"{ideal_t:,.2f}"
        total_diferencia.current.value = f"{dif_total:,.2f}"
        total_estado_cuentas.current.value = f"{estado_total:,.2f}"
        total_diferencia.current.color = ft.Colors.RED if dif_total != 0 else ft.Colors.GREEN

        page.update()

    def reset_local(e):
        local_com_fisicas.current.value = "0"
        local_pos.current.value = "0"
        local_caja_ini.current.value = "0"
        local_salidas.current.value = "0"
        local_efectivo_cont.current.value = "0"
        local_depositos.current.value = "0"
        actualizar_todo()

    def reset_total(e):
        total_pos_ventas.current.value = "0"
        total_fondo_ini.current.value = "0"
        total_salidas.current.value = "0"
        total_caja_contada.current.value = "0"
        total_pedidos_ya.current.value = "0"
        total_depositos.current.value = "0"
        actualizar_todo()

    def exportar_ticket(e):
        # Obtener valores actuales (mismos que en actualizar_todo)
        com = float(local_com_fisicas.current.value or 0)
        p = float(local_pos.current.value or 0)
        ci = float(local_caja_ini.current.value or 0)
        sal = float(local_salidas.current.value or 0)
        ec = float(local_efectivo_cont.current.value or 0)
        dep = float(local_depositos.current.value or 0)
        ventas_ef, ideal_ef, dif_local, estado_local = calcular_local(com, p, ci, sal, ec, dep)

        pv = float(total_pos_ventas.current.value or 0)
        fi = float(total_fondo_ini.current.value or 0)
        stot = float(total_salidas.current.value or 0)
        cc = float(total_caja_contada.current.value or 0)
        py = float(total_pedidos_ya.current.value or 0)
        dtot = float(total_depositos.current.value or 0)
        vt, ideal_t, dif_total, estado_total = calcular_total(pv, fi, stot, cc, py, dtot)

        datos_local = {
            'com_fisicas': com, 'pos': p, 'caja_ini': ci, 'salidas': sal,
            'efectivo_cont': ec, 'depositos': dep,
            'ventas_efectivo': ventas_ef, 'efectivo_ideal': ideal_ef,
            'diferencia': dif_local, 'estado_final': estado_local
        }
        datos_total = {
            'pos_ventas': pv, 'fondo_ini': fi, 'salidas': stot,
            'caja_contada': cc, 'pedidos_ya': py, 'depositos': dtot,
            'ventas_totales': vt, 'caja_ideal': ideal_t,
            'diferencia': dif_total, 'estado_cuentas': estado_total
        }
        fecha_hora = datetime.combine(fecha_selector.value, datetime.now().time())
        html = generar_html_ticket(datos_local, datos_total, fecha_hora)
        # Guardar HTML en archivo temporal y abrirlo en navegador
        import tempfile, webbrowser, os
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html)
            temp_path = f.name
        webbrowser.open(temp_path)
        page.snack_bar = ft.SnackBar(ft.Text("Ticket generado, se abrirá en tu navegador"))
        page.snack_bar.open = True
        page.update()

    def compartir_resultados(e):
        # Copiar al portapapeles un resumen en texto
        texto = f"""💰 CIERRE DE CAJA - {fecha_selector.value.strftime('%d/%m/%Y')} {datetime.now().strftime('%H:%M:%S')}

🏪 LOCAL
Comandas físicas: {local_com_fisicas.current.value}
POS: {local_pos.current.value}
Caja inicial: {local_caja_ini.current.value}
Salidas dinero: {local_salidas.current.value}
Efectivo contado: {local_efectivo_cont.current.value}
Depósitos: {local_depositos.current.value}
Ventas efectivo: {local_ventas_efectivo.current.value}
Efectivo ideal: {local_efectivo_ideal.current.value}
Diferencia: {local_diferencia.current.value}
Estado final caja: {local_estado_final.current.value}

💳 TOTAL
POS + ventas efectivo: {total_pos_ventas.current.value}
Fondo inicial: {total_fondo_ini.current.value}
Salidas totales: {total_salidas.current.value}
Caja contada: {total_caja_contada.current.value}
Pedidos Ya: {total_pedidos_ya.current.value}
Depósitos: {total_depositos.current.value}
Ventas totales: {total_ventas_totales.current.value}
Caja ideal: {total_caja_ideal.current.value}
Diferencia: {total_diferencia.current.value}
Estado cuentas: {total_estado_cuentas.current.value}
"""
        page.set_clipboard(texto)
        page.snack_bar = ft.SnackBar(ft.Text("Resultados copiados al portapapeles"))
        page.snack_bar.open = True
        page.update()

    # ---- Reloj en vivo (hora local del dispositivo) ----
    reloj_text = ft.Text(value="", size=18, weight=ft.FontWeight.BOLD)
    def actualizar_reloj(e=None):
        ahora = datetime.now()
        reloj_text.value = f"🕒 {ahora.strftime('%d/%m/%Y %H:%M:%S')} (hora local)"
        page.update()
    # actualizar cada segundo
    page.add(reloj_text)
    page.add(ft.Divider())
    for i in range(60):
        page.add(ft.Text(""))  # truco para mantener el loop? mejor usar timer
    # Usamos un timer en el cliente
    page.run_task(actualizar_reloj)
    # FIX: implementar un timer periódico con page.add_interval
    page.add_interval(1000, actualizar_reloj)

    # ---- Selector de fecha ----
    fecha_selector = ft.DatePicker(
        first_date=datetime(2020, 1, 1),
        last_date=datetime(2030, 12, 31),
        on_change=lambda e: page.update()
    )
    page.overlay.append(fecha_selector)
    fecha_boton = ft.ElevatedButton(
        "📅 Seleccionar fecha",
        on_click=lambda _: fecha_selector.pick_date()
    )
    fecha_actual_text = ft.Text(value=fecha_cierre.strftime("%d/%m/%Y"))

    def fecha_seleccionada(e):
        if fecha_selector.value:
            fecha_actual_text.value = fecha_selector.value.strftime("%d/%m/%Y")
            page.update()
    fecha_selector.on_change = fecha_seleccionada

    # ---- Sección Local ----
    local_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("🏪 Cierre de Caja Local", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([
                        ft.TextField(ref=local_com_fisicas, label="Comandas físicas", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.TextField(ref=local_caja_ini, label="Caja inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.TextField(ref=local_efectivo_cont, label="Efectivo contado (real)", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.TextField(ref=local_depositos, label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                    ], spacing=10),
                    ft.Column([
                        ft.TextField(ref=local_pos, label="POS", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.TextField(ref=local_salidas, label="Salidas de dinero", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.ElevatedButton("🔄 Resetear Local", on_click=reset_local),
                    ], spacing=10),
                ]),
                ft.Divider(),
                ft.Text("📊 Resultados Locales", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([ft.Text("Ventas en efectivo:"), ft.Text(ref=local_ventas_efectivo, value="0.00")]),
                    ft.Column([ft.Text("Efectivo final (ideal):"), ft.Text(ref=local_efectivo_ideal, value="0.00")]),
                    ft.Column([ft.Text("Diferencia:"), ft.Text(ref=local_diferencia, value="0.00")]),
                    ft.Column([ft.Text("Estado final en caja:"), ft.Text(ref=local_estado_final, value="0.00")]),
                ], spacing=20),
            ], spacing=15),
            padding=15,
        )
    )

    # ---- Sección Total ----
    total_card = ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text("💳 Cierre de Caja Total (Físico + Digital)", size=20, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([
                        ft.TextField(ref=total_pos_ventas, label="POS y ventas en efectivo", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.TextField(ref=total_fondo_ini, label="Fondo inicial", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.TextField(ref=total_caja_contada, label="Caja contada (real)", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.TextField(ref=total_depositos, label="Depósitos", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                    ], spacing=10),
                    ft.Column([
                        ft.TextField(ref=total_salidas, label="Salidas de dinero (total)", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.TextField(ref=total_pedidos_ya, label="Pedidos Ya", value="0", keyboard_type=ft.KeyboardType.NUMBER, on_change=actualizar_todo),
                        ft.ElevatedButton("🔄 Resetear Total", on_click=reset_total),
                    ], spacing=10),
                ]),
                ft.Divider(),
                ft.Text("📊 Resultados Totales", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([ft.Text("Ventas totales:"), ft.Text(ref=total_ventas_totales, value="0.00")]),
                    ft.Column([ft.Text("Caja ideal:"), ft.Text(ref=total_caja_ideal, value="0.00")]),
                    ft.Column([ft.Text("Diferencia:"), ft.Text(ref=total_diferencia, value="0.00")]),
                    ft.Column([ft.Text("Estado final de cuentas:"), ft.Text(ref=total_estado_cuentas, value="0.00")]),
                ], spacing=20),
            ], spacing=15),
            padding=15,
        )
    )

    # ---- Botones de exportación ----
    export_row = ft.Row([
        ft.ElevatedButton("🖨️ Imprimir Ticket", on_click=exportar_ticket, icon=ft.icons.PRINT),
        ft.ElevatedButton("📋 Copiar resultados", on_click=compartir_resultados, icon=ft.icons.CONTENT_COPY),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

    # ---- Montar la página ----
    page.add(
        ft.Row([fecha_boton, ft.Text("Fecha: "), fecha_actual_text], alignment=ft.MainAxisAlignment.START),
        local_card,
        total_card,
        export_row,
    )
    actualizar_todo()

ft.app(target=main)