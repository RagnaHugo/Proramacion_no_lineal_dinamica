"""Vista: Módulo PNL — ingresar función, resolver y ver el análisis paso a paso.

Todo el análisis (función, derivadas, valores críticos, clasificación,
resultado y gráfica) se muestra junto, en un único ft.ResponsiveRow: cada
tarjeta declara cuánto ancho ocupa por breakpoint (`col`), así se
reacomodan solas en vez de solaparse cuando la ventana es angosta.
"""

import libreria_grafica_hugo as ft

from logica.pnl import resolver_pnl

from . import tema
from .componentes import insignia, tarjeta_resultado

COL_MITAD = {"xs": 12, "md": 6}
COL_COMPLETA = {"xs": 12}


def build_pnl_view(page: ft.Page):
    input_funcion = ft.TextField(
        hint_text="Ej: f(x) = x**2 - 4*x + 3",
        bgcolor=tema.TARJETA,
        border_color=tema.BORDE,
        color=tema.TEXTO,
        border_radius=10,
        content_padding=ft.Padding.symmetric(vertical=10, horizontal=14),
        expand=True,
    )

    mensaje_error = ft.Text("", size=13, color=tema.ERROR, visible=False)

    area_resultados = ft.ResponsiveRow(controls=[], run_spacing=16, spacing=16)

    marcador_vacio = ft.Container(
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        border_radius=12,
        padding=ft.Padding.all(24),
        content=ft.Text(
            "Ingresa una función y presiona “Resolver función” para ver el análisis paso a paso.",
            size=13,
            color=tema.TEXTO_SUAVE,
        ),
    )
    area_resultados.controls.append(ft.Container(col=COL_COMPLETA, content=marcador_vacio))

    def _texto_monoespaciado(valor, size=16, color=None):
        return ft.Text(valor, size=size, color=color or tema.TEXTO, selectable=True, font_family="Consolas")

    def _tarjeta_clasificacion(punto, indice, total):
        sufijo = f" (punto {indice})" if total > 1 else ""
        color_condicion = tema.VERDE if punto.tipo == "Mínimo" else (
            tema.ERROR if punto.tipo == "Máximo" else tema.TEXTO_SUAVE
        )
        return tarjeta_resultado(
            f"CLASIFICACIÓN{sufijo}",
            ft.Column(
                controls=[
                    ft.Text(
                        f"En x = {punto.x_str}: f''(x) {punto.condicion}",
                        size=13,
                        color=tema.TEXTO_SUAVE,
                    ),
                    ft.Container(height=8),
                    insignia(f"Función {punto.clasificacion}", color_condicion),
                ],
            ),
            bgcolor=tema.TARJETA_VERDE,
            col=COL_MITAD,
        )

    def _tarjeta_punto(punto, indice, total):
        sufijo = f" (punto {indice})" if total > 1 else ""
        if punto.tipo == "Indeterminado":
            cuerpo = ft.Text(
                "La segunda derivada es 0: la prueba no es concluyente "
                "(posible punto de inflexión).",
                size=13,
                color=tema.TEXTO_SUAVE,
            )
        else:
            icono = ft.Icons.TRENDING_DOWN if punto.tipo == "Mínimo" else ft.Icons.TRENDING_UP
            cuerpo = ft.Row(
                controls=[
                    ft.Icon(icono, color=tema.VERDE, size=22),
                    ft.Column(
                        controls=[
                            ft.Text(f"{punto.tipo.upper()} LOCAL", size=13, weight=ft.FontWeight.BOLD, color=tema.TEXTO),
                            _texto_monoespaciado(f"Punto: ({punto.x_str}, {punto.y_str})", size=13, color=tema.TEXTO_SUAVE),
                        ],
                        spacing=2,
                    ),
                ],
                spacing=10,
            )
        return tarjeta_resultado(f"RESULTADO{sufijo}", cuerpo, bgcolor=tema.TARJETA_VERDE, col=COL_MITAD)

    def _construir_tarjetas(resultado):
        tarjetas = [
            tarjeta_resultado(
                "FUNCIÓN",
                _texto_monoespaciado(resultado.funcion_str),
                bgcolor=tema.TARJETA_MORADA,
                col=COL_MITAD,
            ),
            tarjeta_resultado(
                "PRIMERA DERIVADA",
                _texto_monoespaciado(resultado.primera_derivada_str),
                bgcolor=tema.TARJETA_MORADA,
                col=COL_MITAD,
            ),
            tarjeta_resultado(
                "SEGUNDA DERIVADA",
                _texto_monoespaciado(resultado.segunda_derivada_str),
                bgcolor=tema.TARJETA_AMBAR,
                col=COL_MITAD,
            ),
            tarjeta_resultado(
                "VALORES CRÍTICOS",
                ft.Column(
                    controls=[
                        _texto_monoespaciado(resultado.ecuacion_critica_str, size=14),
                        ft.Container(height=8),
                        *([_texto_monoespaciado(v, size=14, color=tema.TEXTO_SUAVE) for v in resultado.valores_criticos_str]
                          or [ft.Text("No se encontraron valores críticos reales.", size=13, color=tema.TEXTO_SUAVE)]),
                        ft.Container(height=8),
                        insignia(f"{len(resultado.puntos)} punto(s) crítico(s) encontrado(s)", tema.ACENTO),
                    ],
                ),
                bgcolor=tema.TARJETA_AMBAR,
                col=COL_MITAD,
            ),
        ]

        total = len(resultado.puntos)
        for i, punto in enumerate(resultado.puntos, start=1):
            tarjetas.append(_tarjeta_clasificacion(punto, i, total))
            tarjetas.append(_tarjeta_punto(punto, i, total))

        tarjetas.append(
            tarjeta_resultado(
                "GRÁFICA",
                ft.Container(
                    content=ft.Image(src=resultado.imagen_b64, fit=ft.BoxFit.CONTAIN),
                    alignment=ft.Alignment(0, 0),
                    height=320,
                ),
                col=COL_COMPLETA,
            )
        )
        return tarjetas

    def on_resolver(e):
        txt = input_funcion.value.strip()
        mensaje_error.visible = False
        if not txt:
            mensaje_error.value = "Ingresa una función."
            mensaje_error.visible = True
            page.update()
            return
        try:
            resultado = resolver_pnl(txt)
            area_resultados.controls = _construir_tarjetas(resultado)
        except Exception as ex:
            mensaje_error.value = f"Error al procesar la función: {ex}"
            mensaje_error.visible = True
        page.update()

    def on_limpiar(e):
        input_funcion.value = ""
        mensaje_error.visible = False
        area_resultados.controls = [ft.Container(col=COL_COMPLETA, content=marcador_vacio)]
        page.update()

    estilo_boton_recto = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))

    boton_resolver = ft.Button(
        content=ft.Row(
            [ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, size=16), ft.Text("Resolver función")],
            spacing=6,
            tight=True,
        ),
        bgcolor=tema.PRIMARIO,
        color=tema.TEXTO_INVERSO,
        style=estilo_boton_recto,
        on_click=on_resolver,
    )

    boton_limpiar = ft.TextButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.CLEANING_SERVICES_OUTLINED, size=15), ft.Text("Limpiar")],
            spacing=6,
            tight=True,
        ),
        style=estilo_boton_recto,
        on_click=on_limpiar,
    )

    tarjeta_entrada = ft.Container(
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        border_radius=12,
        padding=ft.Padding.all(20),
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Ingresa la función", size=14, weight=ft.FontWeight.BOLD, color=tema.ACENTO),
                        ft.Container(expand=True),
                        boton_limpiar,
                    ],
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(col={"xs": 12, "sm": 8}, content=input_funcion),
                        ft.Container(col={"xs": 12, "sm": 4}, content=boton_resolver),
                    ],
                    spacing=10,
                    run_spacing=10,
                ),
                mensaje_error,
                ft.Text(
                    "Ejemplos:  f(x) = x**2 - 4*x + 3     C(x) = ln(x) + sqrt(x)     P(t) = t**3 - 6*t",
                    size=11,
                    color=tema.TEXTO_SUAVE,
                ),
            ],
            spacing=10,
        ),
    )

    return [
        ft.Text("MÓDULO: PROGRAMACIÓN NO LINEAL", size=18, weight=ft.FontWeight.BOLD, color=tema.TEXTO),
        tarjeta_entrada,
        area_resultados,
    ]
