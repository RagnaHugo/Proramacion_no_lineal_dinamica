import base64
import io
from dataclasses import dataclass, field

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

from .parser import interpretar_funcion

x_sym = sp.symbols("x")


@dataclass
class PuntoCritico:
    """Un punto crítico ya clasificado, listo para mostrarse en una tarjeta."""
    x_str: str
    y_str: str
    condicion: str      # "> 0", "< 0" o "= 0"
    tipo: str            # "Mínimo", "Máximo" o "Indeterminado"
    clasificacion: str   # "convexa", "cóncava" o "Convexa y Cóncava"


@dataclass
class ResultadoPNL:
    """Resultado del análisis, ya separado por paso para la interfaz."""
    nombre: str
    variable: str
    funcion_str: str
    primera_derivada_str: str
    segunda_derivada_str: str
    ecuacion_critica_str: str
    valores_criticos_str: list = field(default_factory=list)
    puntos: list = field(default_factory=list)  # de PuntoCritico
    imagen_b64: str = ""


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
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ax.plot(xs, ys, color="#2563EB", linewidth=2)
    ax.axhline(0, color="#94A3B8", linewidth=1)
    ax.axvline(0, color="#94A3B8", linewidth=1)

    if puntos_criticos:
        for cx, cy in puntos_criticos:
            ax.plot(cx, cy, "o", color="#16A34A", markersize=7)

    ax.tick_params(colors="#64748B", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#E2E8F0")
    ax.grid(True, color="#F1F5F9", linewidth=0.6)

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

    Devuelve un ResultadoPNL con cada paso ya separado para la interfaz.
    """
    nombre, x, f = interpretar_funcion(funcion_txt)

    f1 = sp.diff(f, x)
    f2 = sp.diff(f1, x)

    criticos = sp.solve(sp.Eq(f1, 0), x)
    criticos_reales = [c for c in criticos if getattr(c, 'is_real', True)]

    puntos = []
    puntos_para_grafica = []

    for c in criticos_reales:
        valor_f2 = sp.simplify(f2.subs(x, c))
        valor_y = sp.simplify(f.subs(x, c))

        if valor_f2.is_positive:
            condicion, tipo, clasificacion = "> 0", "Mínimo", "convexa"
        elif valor_f2.is_negative:
            condicion, tipo, clasificacion = "< 0", "Máximo", "cóncava"
        else:
            condicion, tipo, clasificacion = "= 0", "Indeterminado", "Convexa y Cóncava"

        puntos.append(PuntoCritico(
            x_str=str(c),
            y_str=str(valor_y),
            condicion=condicion,
            tipo=tipo,
            clasificacion=clasificacion,
        ))

        try:
            puntos_para_grafica.append((float(c), float(valor_y)))
        except Exception:
            pass

    if puntos_para_grafica:
        xs_criticos = [p[0] for p in puntos_para_grafica]
        centro = sum(xs_criticos) / len(xs_criticos)
        x_min, x_max = centro - 10, centro + 10
    else:
        x_min, x_max = -10, 10

    img_b64 = graficar_funcion(f, x_min, x_max, puntos_para_grafica)

    return ResultadoPNL(
        nombre=nombre,
        variable=str(x),
        funcion_str=f"{nombre}({x}) = {f}",
        primera_derivada_str=f"{nombre}'({x}) = {f1}",
        segunda_derivada_str=f"{nombre}''({x}) = {f2}",
        ecuacion_critica_str=f"{f1} = 0",
        valores_criticos_str=[f"{x} = {c}" for c in criticos_reales],
        puntos=puntos,
        imagen_b64=img_b64,
    )
