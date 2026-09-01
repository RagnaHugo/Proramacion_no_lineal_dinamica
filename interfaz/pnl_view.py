"""Vista: Módulo PNL (ingresar función, resolver, graficar)."""

import flet as ft

from logica.pnl import resolver_pnl

from . import tema
from .componentes import envoltura_pagina, panel_seccion


def build_pnl_view(page: ft.Page):
    from .dashboard import build_dashboard  # import local: evita ciclo con dashboard

    input_funcion = ft.TextField(
        hint_text="Ej: x**2 - 4*x + 3",
        bgcolor=tema.TARJETA,
        border_color=tema.BORDE,
        color=tema.TEXTO,
        border_radius=10,
        content_padding=ft.Padding.symmetric(vertical=10, horizontal=14),
    )

    texto_resultado = ft.Text(
        "resultado",
        size=14,
        color=tema.TEXTO_SUAVE,
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
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        border_radius=12,
        alignment=ft.Alignment(0, 0),
    )

    def on_resolver(e):
        txt = input_funcion.value.strip()
        if not txt:
            texto_resultado.value = "Ingresa una función."
            texto_resultado.color = tema.ERROR
            page.update()
            return
        try:
            resultado_txt, img_b64 = resolver_pnl(txt)
            texto_resultado.value = resultado_txt
            texto_resultado.color = tema.ACENTO
            imagen_grafica.src = img_b64
        except Exception as ex:
            texto_resultado.value = f"Error al procesar la función: {ex}"
            texto_resultado.color = tema.ERROR
            imagen_grafica.src = None
        page.update()

    boton_resolver = ft.Button(
        content="Resolver",
        bgcolor=tema.PRIMARIO,
        color=tema.TEXTO,
        on_click=on_resolver,
    )

    def volver(e):
        page.clean()
        page.add(build_dashboard(page))

    boton_volver = ft.TextButton(
        content="← Volver",
        icon=ft.Icons.ARROW_BACK,
        on_click=volver,
    )

    columna_izquierda = ft.Column(
        controls=[
            ft.Text("Ingresa la función", size=14, weight=ft.FontWeight.BOLD, color=tema.ACENTO),
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
            ft.Text("Gráfica de la función", size=14, weight=ft.FontWeight.BOLD, color=tema.ACENTO_AZUL),
            caja_grafica,
        ],
        spacing=8,
    )

    panel_pnl = panel_seccion(
        ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        boton_volver,
                        ft.Text(
                            "MÓDULO: PROGRAMACIÓN NO LINEAL",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=tema.TEXTO,
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
        )
    )

    return envoltura_pagina(panel_pnl)
