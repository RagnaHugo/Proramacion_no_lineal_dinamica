"""Vista: Dashboard principal / menú de módulos."""

import flet as ft

from . import tema
from .componentes import envoltura_pagina, panel_seccion, tarjeta_modulo


def build_dashboard(page: ft.Page):
    from .pnl_view import build_pnl_view  # import local: evita ciclo con pnl_view

    seleccion = ft.Text(
        "Selecciona un módulo para continuar.",
        size=15,
        color=tema.TEXTO_SUAVE,
    )

    def mostrar_pnl(e):
        page.clean()
        page.add(build_pnl_view(page))

    def mostrar_dinamica(e):
        seleccion.value = "Módulo activo: Dinámica."
        seleccion.color = tema.ACENTO_AZUL
        page.update()

    boton_pnl = tarjeta_modulo("PNL", "Optimización", mostrar_pnl, activa=True)
    boton_dinamica = tarjeta_modulo("Dinámica", "Modelos", mostrar_dinamica)

    integrantes = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "INTEGRANTES",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=tema.TEXTO_SUAVE,
                ),
                ft.Container(height=4),
                ft.Column(
                    controls=[
                        ft.Row([ft.Icon(ft.Icons.PERSON, size=16, color=tema.ACENTO), ft.Text("Isabel", size=15, color=tema.TEXTO)]),
                        ft.Row([ft.Icon(ft.Icons.PERSON, size=16, color=tema.ACENTO), ft.Text("Milagros", size=15, color=tema.TEXTO)]),
                        ft.Row([ft.Icon(ft.Icons.PERSON, size=16, color=tema.ACENTO), ft.Text("Hugo", size=15, color=tema.TEXTO)]),
                    ],
                    spacing=12,
                ),
            ],
            spacing=12,
        ),
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        padding=ft.Padding.all(24),
        border_radius=16,
        width=200,
    )

    caja_estado = ft.Container(
        content=seleccion,
        bgcolor=tema.TARJETA,
        border=ft.Border.all(1, tema.BORDE),
        padding=ft.Padding.all(16),
        border_radius=12,
        width=340,
    )

    panel_principal = panel_seccion(
        ft.Column(
            controls=[
                ft.Text(
                    "PROGRAMACIÓN NO LINEAL Y DINÁMICA",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                    color=tema.TEXTO,
                ),
                ft.Text(
                    "DASHBOARD / MENÚ PRINCIPAL",
                    size=13,
                    weight=ft.FontWeight.BOLD,
                    color=tema.ACENTO,
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
        )
    )

    return envoltura_pagina(panel_principal)
