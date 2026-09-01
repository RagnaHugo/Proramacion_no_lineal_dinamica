"""Vista: Módulo PNL — ingresar función, resolver y ver el análisis.

El resultado se organiza en pestañas (Resumen / Procedimiento / Gráfica).
Dentro de "Resumen" las tarjetas van numeradas para que se lea como una
secuencia de pasos. Cada pestaña tiene su propio scroll interno, así nada
se corta ni se solapa si la ventana es angosta o hay varios puntos críticos.
"""

import itertools

import libreria_grafica_hugo as ft

from logica.pnl import resolver_pnl

from . import iconos, tema
from .componentes import icono, insignia, tarjeta_resultado

COL_MITAD = {"xs": 12, "md": 6}
COL_COMPLETA = {"xs": 12}
ALTURA_TABS = 560


def build_pnl_view(page: ft.Page):
    input_funcion = ft.TextField(
        hint_text="Ej: f(x) = x**2 - 4*x + 3",
        bgcolor=tema.TARJETA,
        border_color=tema.BORDE,
        color=tema.TEXTO,
        border_radius=10,
        height=tema.ALTURA_CONTROL,
        content_padding=ft.Padding.symmetric(vertical=10, horizontal=14),
        expand=True,
    )

    mensaje_error = ft.Text("", size=13, color=tema.ERROR, visible=False)

    marcador_vacio = ft.Container(
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        border_radius=12,
        padding=ft.Padding.all(24),
        content=ft.Text(
            "Ingresa una función y presiona “Resolver función” para ver el análisis.",
            size=13,
            color=tema.TEXTO_SUAVE,
        ),
    )

    resultado_slot = ft.Container(content=marcador_vacio)

    def _texto_monoespaciado(valor, size=16, color=None):
        return ft.Text(valor, size=size, color=color or tema.TEXTO, selectable=True, font_family="Consolas")

    def _pagina_pestania(controles):
        """Contenido de una pestaña: alto fijo (ALTURA_TABS) con scroll propio."""
        return ft.Container(
            padding=ft.Padding.only(top=16),
            content=ft.Column(controles, spacing=16, scroll=ft.ScrollMode.AUTO, expand=True),
        )

    def _tarjeta_clasificacion(punto, indice, total, numero=None):
        sufijo = f" (punto {indice})" if total > 1 else ""
        prefijo = f"{numero}. " if numero else ""
        color_condicion = tema.VERDE if punto.tipo == "Mínimo" else (
            tema.ERROR if punto.tipo == "Máximo" else tema.TEXTO_SUAVE
        )
        return tarjeta_resultado(
            f"{prefijo}CLASIFICACIÓN{sufijo}",
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            icono(iconos.CLASIFICACION, size=16, color=color_condicion),
                            ft.Text(
                                f"En x = {punto.x_str}: f''(x) {punto.condicion}",
                                size=13,
                                color=tema.TEXTO_SUAVE,
                            ),
                        ],
                        spacing=6,
                    ),
                    ft.Container(height=8),
                    insignia(f"Función {punto.clasificacion}", color_condicion),
                ],
            ),
            bgcolor=tema.TARJETA_VERDE,
            col=COL_MITAD,
        )

    def _tarjeta_punto(punto, indice, total, numero=None):
        sufijo = f" (punto {indice})" if total > 1 else ""
        prefijo = f"{numero}. " if numero else ""
        if punto.tipo == "Indeterminado":
            cuerpo = ft.Text(
                "La segunda derivada es 0: la prueba no es concluyente "
                "(posible punto de inflexión).",
                size=13,
                color=tema.TEXTO_SUAVE,
            )
        else:
            cuerpo = ft.Row(
                controls=[
                    icono(iconos.RESULTADO, size=22, color=tema.VERDE),
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
        return tarjeta_resultado(f"{prefijo}RESULTADO{sufijo}", cuerpo, bgcolor=tema.TARJETA_VERDE, col=COL_MITAD)

    def _pestania_resumen(resultado):
        n = itertools.count(1)
        tarjetas = [
            tarjeta_resultado(
                f"{next(n)}. FUNCIÓN",
                _texto_monoespaciado(resultado.funcion_str),
                bgcolor=tema.TARJETA_MORADA,
                col=COL_MITAD,
            ),
            tarjeta_resultado(
                f"{next(n)}. PRIMERA DERIVADA",
                _texto_monoespaciado(resultado.primera_derivada_str),
                bgcolor=tema.TARJETA_MORADA,
                col=COL_MITAD,
            ),
            tarjeta_resultado(
                f"{next(n)}. SEGUNDA DERIVADA",
                _texto_monoespaciado(resultado.segunda_derivada_str),
                bgcolor=tema.TARJETA_AMBAR,
                col=COL_MITAD,
            ),
            tarjeta_resultado(
                f"{next(n)}. VALORES CRÍTICOS",
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
            tarjetas.append(_tarjeta_clasificacion(punto, i, total, numero=next(n)))
            tarjetas.append(_tarjeta_punto(punto, i, total, numero=next(n)))

        return _pagina_pestania([ft.ResponsiveRow(controls=tarjetas, run_spacing=16, spacing=16)])

    def _pestania_procedimiento(resultado):
        pasos = [
            ("Paso 1 — Derivar la función", resultado.primera_derivada_str),
            ("Paso 2 — Igualar la primera derivada a cero",
             f"{resultado.ecuacion_critica_str}   →   "
             + (", ".join(resultado.valores_criticos_str) if resultado.valores_criticos_str
                else "sin valores críticos reales")),
            ("Paso 3 — Calcular la segunda derivada", resultado.segunda_derivada_str),
        ]

        bloques = []
        for titulo, texto in pasos:
            bloques.append(ft.Text(titulo, size=13, weight=ft.FontWeight.BOLD, color=tema.ACENTO))
            bloques.append(_texto_monoespaciado(texto, size=14))
            bloques.append(ft.Container(height=4))

        bloques.append(
            ft.Text("Paso 4 — Evaluar la segunda derivada en cada punto crítico",
                    size=13, weight=ft.FontWeight.BOLD, color=tema.ACENTO)
        )
        if not resultado.puntos:
            bloques.append(ft.Text("No hay puntos críticos reales que evaluar.", size=14, color=tema.TEXTO_SUAVE))
        for punto in resultado.puntos:
            if punto.tipo == "Indeterminado":
                explicacion = "la prueba no es concluyente (posible punto de inflexión)."
            else:
                explicacion = f"la función es {punto.clasificacion} → {punto.tipo.lower()} local en ({punto.x_str}, {punto.y_str})."
            bloques.append(
                _texto_monoespaciado(
                    f"En x = {punto.x_str}: f''(x) {punto.condicion}  →  {explicacion}",
                    size=14,
                    color=tema.TEXTO_SUAVE,
                )
            )

        bloques.append(ft.Container(height=4))
        bloques.append(
            ft.Text("Paso 5 — Reemplazar en la función objetivo para hallar el valor óptimo",
                    size=13, weight=ft.FontWeight.BOLD, color=tema.ACENTO)
        )
        puntos_no_indeterminados = [p for p in resultado.puntos if p.tipo != "Indeterminado"]
        if not puntos_no_indeterminados:
            bloques.append(ft.Text("No hay un punto óptimo que sustituir.", size=14, color=tema.TEXTO_SUAVE))
        for punto in puntos_no_indeterminados:
            bloques.append(
                ft.Row(
                    controls=[
                        _texto_monoespaciado(f"{resultado.nombre}({punto.x_str}) =", size=14, color=tema.TEXTO_SUAVE),
                        _texto_monoespaciado(f"“{punto.y_str}”", size=14, color=tema.VERDE),
                        ft.Text(f"(valor óptimo — {punto.tipo.lower()})", size=12, color=tema.TEXTO_SUAVE, italic=True),
                    ],
                    spacing=6,
                )
            )

        return _pagina_pestania([
            tarjeta_resultado("PROCEDIMIENTO COMPLETO", ft.Column(bloques, spacing=6), col=COL_COMPLETA),
        ])

    def _pestania_grafica(resultado):
        return _pagina_pestania([
            tarjeta_resultado(
                "GRÁFICA",
                ft.Container(
                    content=ft.Image(src=resultado.imagen_b64, fit=ft.BoxFit.CONTAIN),
                    alignment=ft.Alignment(0, 0),
                    height=ALTURA_TABS - 120,
                ),
                col=COL_COMPLETA,
            )
        ])

    def _construir_tabs(resultado):
        return ft.Tabs(
            length=3,
            selected_index=0,
            content=ft.Column(
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Resumen"),
                            ft.Tab(label="Procedimiento"),
                            ft.Tab(label="Gráfica"),
                        ],
                        label_color=tema.PRIMARIO,
                        unselected_label_color=tema.TEXTO_SUAVE,
                        indicator_color=tema.PRIMARIO,
                    ),
                    ft.Container(
                        height=ALTURA_TABS,
                        content=ft.TabBarView(
                            controls=[
                                _pestania_resumen(resultado),
                                _pestania_procedimiento(resultado),
                                _pestania_grafica(resultado),
                            ],
                        ),
                    ),
                ],
            ),
        )

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
            resultado_slot.content = _construir_tabs(resultado)
        except Exception as ex:
            mensaje_error.value = f"Error al procesar la función: {ex}"
            mensaje_error.visible = True
        page.update()

    def on_limpiar(e):
        input_funcion.value = ""
        mensaje_error.visible = False
        resultado_slot.content = marcador_vacio
        page.update()

    estilo_boton_recto = ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0))

    boton_resolver = ft.Button(
        content=ft.Row(
            [icono(iconos.RESOLVER, size=16, color=tema.TEXTO_INVERSO), ft.Text("Resolver función")],
            spacing=6,
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        bgcolor=tema.PRIMARIO,
        color=tema.TEXTO_INVERSO,
        height=tema.ALTURA_CONTROL,
        style=estilo_boton_recto,
        on_click=on_resolver,
    )

    boton_limpiar = ft.TextButton(
        content=ft.Row(
            [icono(iconos.LIMPIAR, size=15, color=tema.TEXTO_SUAVE), ft.Text("Limpiar")],
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
                    vertical_alignment=ft.CrossAxisAlignment.START,
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
        resultado_slot,
    ]
