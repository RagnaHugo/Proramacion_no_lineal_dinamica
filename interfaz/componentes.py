"""Widgets reutilizables entre vistas (dashboard, módulos, etc.)."""

import flet as ft

from . import tema


def tarjeta_modulo(titulo, subtitulo, on_click, activa=False):
    """Tarjeta clicable usada en el dashboard para entrar a un módulo.

    `activa=True` la resalta con el gradiente de color principal;
    en caso contrario se muestra como tarjeta neutra.
    """
    contenido = ft.Column(
        controls=[
            ft.Text(titulo, size=28, weight=ft.FontWeight.BOLD, color=tema.TEXTO),
            ft.Text(subtitulo, size=12, color=tema.TEXTO_TENUE if activa else tema.TEXTO_SUAVE),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    estilo = {}
    if activa:
        estilo["gradient"] = ft.LinearGradient(
            begin=ft.Alignment(-1.0, -1.0),
            end=ft.Alignment(1.0, 1.0),
            colors=[tema.PRIMARIO, tema.ACENTO_MORADO],
        )
    else:
        estilo["bgcolor"] = tema.TARJETA
        estilo["border"] = ft.Border.all(1, tema.BORDE)

    return ft.Container(
        content=contenido,
        width=160,
        height=140,
        border_radius=16,
        padding=ft.Padding.all(16),
        ink=True,
        on_click=on_click,
        **estilo,
    )


def panel_seccion(contenido):
    """Contenedor de página estándar: fondo, borde y esquinas redondeadas."""
    return ft.Container(
        padding=ft.Padding.all(32),
        bgcolor=tema.PANEL,
        border=ft.Border.all(1, tema.BORDE_SUAVE),
        border_radius=24,
        content=contenido,
    )


def envoltura_pagina(contenido):
    """Envoltura de página completa (centrada, con el fondo general)."""
    return ft.Container(
        expand=True,
        padding=ft.Padding.all(40),
        alignment=ft.Alignment(0, 0),
        bgcolor=tema.FONDO,
        content=contenido,
    )
