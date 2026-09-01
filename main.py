import flet as ft

from interfaz import tema
from interfaz.shell import build_shell


def main(page: ft.Page):
    page.title = "Programación No Lineal y Dinámica"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = tema.FONDO
    page.add(build_shell(page))


if __name__ == "__main__":
    ft.run(main, assets_dir="recursos")
