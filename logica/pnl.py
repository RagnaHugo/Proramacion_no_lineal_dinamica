import base64
import io

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from .parser import interpretar_funcion

x_sym = sp.symbols("x")


def graficar_funcion(expr, x_min=-10, x_max=10, puntos_criticos=None):
    """Genera la gráfica de la función y la devuelve como imagen base64."""
    f_lamb = sp.lambdify(x_sym, expr, modules=["numpy"])

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
