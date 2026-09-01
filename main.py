import flet as ft

from interfaz.shell import build_shell


def main(page: ft.Page):
    page.title = "Programación No Lineal y Dinámica"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.bgcolor = "#090C15"
    page.add(build_shell(page))


if __name__ == "__main__":
    ft.run(main)
