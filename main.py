import base64
import io

import flet as ft
import matplotlib

from funcion import interpretar_funcion

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import sympy as sp


def main(page: ft.Page):
    page.title = "Programación No Lineal y Dinámica"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = "#090C15"

    # ------------------------------------------------------------------
    # Utilidades matemáticas (para el módulo de PNL)
    # ------------------------------------------------------------------
    x_sym = sp.symbols("x")

    def graficar_funcion(expr, x_min=-10, x_max=10, puntos_criticos=None):
        """Genera la gráfica de la función y la devuelve como imagen base64."""
        f_lamb = sp.lambdify(x_sym, expr, modules=["numpy"])

        import numpy as np

        xs = np.linspace(x_min, x_max, 400)
        ys = []
        for xv in xs:
            try:
                yv = float(f_lamb(xv))
            except Exception:
                yv = float("nan")
            ys.append(yv)

        fig, ax = plt.subplots(figsize=(4.2, 3.6), dpi=130)
        fig.patch.set_facecolor("#0F1524")
        ax.set_facecolor("#0F1524")

        ax.plot(xs, ys, color="#00F5C4", linewidth=2)
        ax.axhline(0, color="#3B4A6B", linewidth=1)
        ax.axvline(0, color="#3B4A6B", linewidth=1)

        if puntos_criticos:
            for cx, cy in puntos_criticos:
                ax.plot(cx, cy, "o", color="#7C3AED", markersize=7)

        ax.tick_params(colors="#8FA3BF", labelsize=8)
        for spine in ax.spines.values():
            spine.set_color("#263354")
        ax.grid(True, color="#1E2945", linewidth=0.6)

        buf = io.BytesIO()
        fig.tight_layout()
        fig.savefig(buf, format="png", facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode("utf-8")




    def resolver_pnl(funcion_txt):
        """
        Analiza la función: calcula derivadas, halla puntos críticos, evalúa la
        concavidad y clasifica máximos/mínimos.

        Devuelve la tupla (texto_resultado, imagen_base64).
        """
        nombre, x, f = interpretar_funcion(funcion_txt)

        # Derivadas
        f1 = sp.diff(f, x)
        f2 = sp.diff(f1, x)

        # Valores críticos reales
        criticos = sp.solve(sp.Eq(f1, 0), x)
        criticos_reales = [c for c in criticos if getattr(c, 'is_real', True)]

        # Construcción del reporte en texto
        resultado = f"Función: {nombre}({x}) = {sp.pretty(f)}\n\n"

        # 1. Primera derivada
        resultado += "1. Primera derivada\n"
        resultado += "-" * 45 + "\n"
        resultado += f"{nombre}'({x}) = {sp.pretty(f1)}\n\n"
        resultado += "Valor crítico, igualando la primera derivada a cero:\n"
        resultado += f"{sp.pretty(f1)} = 0\n\n"

        if not criticos_reales:
            resultado += "No se encontraron valores críticos reales.\n"
        else:
            resultado += "Valores críticos:\n"
            for c in criticos_reales:
                resultado += f"{x} = {sp.pretty(c)}\n"

        # 2. Segunda derivada
        resultado += "\n2. Segunda derivada\n"
        resultado += "-" * 45 + "\n"
        resultado += f"{nombre}''({x}) = {sp.pretty(f2)}\n\n  "

        # 3. Máximo / Mínimo
        resultado += "3. Máximo/Mínimo\n"
        resultado += "-" * 45 + "\n"

        puntos_para_grafica = []

        for c in criticos_reales:
            valor_f2 = sp.simplify(f2.subs(x, c))
            valor_y = sp.simplify(f.subs(x, c))

            resultado += f"\nEn {x} = {sp.pretty(c)}:\n"
            resultado += f"{nombre}''({x}) = {sp.pretty(valor_f2)}\n"

            # Determinación de la condición (> 0, < 0, = 0)
            if valor_f2.is_positive:
                condicion = "> 0"
                tipo = "Mínimo"
                clasificacion = "convexa"
            elif valor_f2.is_negative:
                condicion = "< 0"
                tipo = "Máximo"
                clasificacion = "cóncava"
            else:
                condicion = "= 0"
                tipo = "Indeterminado"
                clasificacion = "Convexa y Cóncava"

            # Muestra el valor de x reemplazado en la segunda derivada y su relación con cero
            resultado += f"{nombre}''({sp.pretty(c)}) = {sp.pretty(valor_f2)} {condicion}\n"

            if tipo == "Mínimo":
                resultado += f"→ La función es {clasificacion}.\n"
                resultado += "→ Tiene un mínimo local.\n"
                resultado += f"→ Punto mínimo: ({sp.pretty(c)}, {sp.pretty(valor_y)})\n"
            elif tipo == "Máximo":
                resultado += f"→ La función es {clasificacion}.\n"
                resultado += "→ Tiene un máximo local.\n"
                resultado += f"→ Punto máximo: ({sp.pretty(c)}, {sp.pretty(valor_y)})\n"
            else:
                resultado += "→ La segunda derivada es 0.\n"
                resultado += "→ La prueba no es concluyente (posible punto de inflexión).\n"

            # Coordenadas numéricas para la gráfica
            try:
                c_float = float(c)
                y_float = float(valor_y)
                puntos_para_grafica.append((c_float, y_float))
            except Exception:
                pass

        # Rango de graficación centrado en los puntos críticos
        if puntos_para_grafica:
            xs_criticos = [p[0] for p in puntos_para_grafica]
            centro = sum(xs_criticos) / len(xs_criticos)
            x_min, x_max = centro - 10, centro + 10
        else:
            x_min, x_max = -10, 10

        # Generar la gráfica en Base64
        img_b64 = graficar_funcion(f, x_min, x_max, puntos_para_grafica)

        return resultado, img_b64

    # ------------------------------------------------------------------
    # Vista: Dashboard principal
    # ------------------------------------------------------------------
    def build_dashboard():
        seleccion = ft.Text(
            "Selecciona un módulo para continuar.",
            size=15,
            color="#8FA3BF",
        )

        def mostrar_pnl(e):
            page.clean()
            page.add(build_pnl_view())

        def mostrar_dinamica(e):
            seleccion.value = "Módulo activo: Dinámica."
            seleccion.color = "#3B82F6"
            page.update()

        boton_pnl = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("PNL", size=28, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Text("Optimización", size=12, color="#E2E8F0"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=160,
            height=140,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1.0, -1.0),
                end=ft.Alignment(1.0, 1.0),
                colors=["#2563EB", "#7C3AED"],
            ),
            border_radius=16,
            padding=ft.Padding.all(16),
            ink=True,
            on_click=mostrar_pnl,
        )

        boton_dinamica = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Dinámica", size=28, weight=ft.FontWeight.BOLD, color="#FFFFFF"),
                    ft.Text("Modelos", size=12, color="#8FA3BF"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=160,
            height=140,
            bgcolor="#141B2D",
            border=ft.Border.all(1, "#263354"),
            border_radius=16,
            padding=ft.Padding.all(16),
            ink=True,
            on_click=mostrar_dinamica,
        )

        integrantes = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "INTEGRANTES",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color="#8FA3BF",
                    ),
                    ft.Container(height=4),
                    ft.Column(
                        controls=[
                            ft.Row([ft.Icon(ft.Icons.PERSON, size=16, color="#00F5C4"), ft.Text("Isabel", size=15, color="#FFFFFF")]),
                            ft.Row([ft.Icon(ft.Icons.PERSON, size=16, color="#00F5C4"), ft.Text("Milagros", size=15, color="#FFFFFF")]),
                            ft.Row([ft.Icon(ft.Icons.PERSON, size=16, color="#00F5C4"), ft.Text("Hugo", size=15, color="#FFFFFF")]),
                        ],
                        spacing=12,
                    ),
                ],
                spacing=12,
            ),
            bgcolor="#141B2D",
            border=ft.Border.all(1, "#263354"),
            padding=ft.Padding.all(24),
            border_radius=16,
            width=200,
        )

        caja_estado = ft.Container(
            content=seleccion,
            bgcolor="#141B2D",
            border=ft.Border.all(1, "#263354"),
            padding=ft.Padding.all(16),
            border_radius=12,
            width=340,
        )

        panel_principal = ft.Container(
            padding=ft.Padding.all(32),
            bgcolor="#0F1524",
            border=ft.Border.all(1, "#1E2945"),
            border_radius=24,
            content=ft.Column(
                controls=[
                    ft.Text(
                        "PROGRAMACIÓN NO LINEAL Y DINÁMICA",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color="#FFFFFF",
                    ),
                    ft.Text(
                        "DASHBOARD / MENÚ PRINCIPAL",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color="#00F5C4",
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Row(
                                        controls=[boton_pnl, boton_dinamica],
                                        spacing=20,
                                    ),
                                    caja_estado,
                                ],
                                spacing=20,
                            ),
                            integrantes,
                        ],
                        spacing=24,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                spacing=6,
            ),
        )

        return ft.Container(
            expand=True,
            padding=ft.Padding.all(40),
            alignment=ft.Alignment(0, 0),
            bgcolor="#090C15",
            content=panel_principal,
        )

    # ------------------------------------------------------------------
    # Vista: Módulo PNL (ingresar función, resolver, graficar)
    # ------------------------------------------------------------------
    def build_pnl_view():
        input_funcion = ft.TextField(
            hint_text="Ej: x**2 - 4*x + 3",
            bgcolor="#141B2D",
            border_color="#263354",
            color="#FFFFFF",
            border_radius=10,
            content_padding=ft.Padding.symmetric(vertical=10, horizontal=14),
        )

        texto_resultado = ft.Text(
            "resultado",
            size=14,
            color="#8FA3BF",
            selectable=True,
        )

        imagen_grafica = ft.Image(
            src=None,
            fit=ft.BoxFit.CONTAIN,
        )

        caja_grafica = ft.Container(
            content=imagen_grafica,
            width=340,
            height=300,
            bgcolor="#141B2D",
            border=ft.Border.all(1, "#263354"),
            border_radius=12,
            alignment=ft.Alignment(0, 0),
        )

        def on_resolver(e):
            txt = input_funcion.value.strip()
            if not txt:
                texto_resultado.value = "Ingresa una función."
                texto_resultado.color = "#EF4444"
                page.update()
                return
            try:
                resultado_txt, img_b64 = resolver_pnl(txt)
                texto_resultado.value = resultado_txt
                texto_resultado.color = "#00F5C4"
                imagen_grafica.src = img_b64
            except Exception as ex:
                texto_resultado.value = f"Error al procesar la función: {ex}"
                texto_resultado.color = "#EF4444"
                imagen_grafica.src = None
            page.update()

        boton_resolver = ft.Button(
            content="Resolver",
            bgcolor="#2563EB",
            color="#FFFFFF",
            on_click=on_resolver,
        )

        def volver(e):
            page.clean()
            page.add(build_dashboard())

        boton_volver = ft.TextButton(
            content="← Volver",
            icon=ft.Icons.ARROW_BACK,
            on_click=volver,
        )

        columna_izquierda = ft.Column(
            controls=[
                ft.Text("Ingresa la función", size=14, weight=ft.FontWeight.BOLD, color="#00F5C4"),
                input_funcion,
                ft.Container(height=8),
                boton_resolver,
                ft.Container(height=16),
                texto_resultado,
            ],
            spacing=8,
            width=320,
        )

        columna_derecha = ft.Column(
            controls=[
                ft.Text("Gráfica de la función", size=14, weight=ft.FontWeight.BOLD, color="#3B82F6"),
                caja_grafica,
            ],
            spacing=8,
        )

        panel_pnl = ft.Container(
            padding=ft.Padding.all(32),
            bgcolor="#0F1524",
            border=ft.Border.all(1, "#1E2945"),
            border_radius=24,
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            boton_volver,
                            ft.Text(
                                "MÓDULO: PROGRAMACIÓN NO LINEAL",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF",
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Container(height=12),
                    ft.Row(
                        controls=[columna_izquierda, columna_derecha],
                        spacing=32,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                ],
                spacing=6,
            ),
        )

        return ft.Container(
            expand=True,
            padding=ft.Padding.all(40),
            alignment=ft.Alignment(0, 0),
            bgcolor="#090C15",
            content=panel_pnl,
        )

    page.add(build_dashboard())


ft.run(main)