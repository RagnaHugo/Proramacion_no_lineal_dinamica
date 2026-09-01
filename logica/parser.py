import re
import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr, standard_transformations,
    implicit_multiplication_application, convert_xor,
)

_TRANSFORMACIONES = standard_transformations + (
    implicit_multiplication_application,  # permite "2x" en vez de "2*x"
    convert_xor,                          # convierte "^" en "**"
)

_FUNCIONES_PERMITIDAS = {
    "sqrt": sp.sqrt, "raiz": sp.sqrt,
    "ln": sp.log, "log": sp.log,
    "sin": sp.sin, "sen": sp.sin,
    "cos": sp.cos, "tan": sp.tan,
    "abs": sp.Abs,
    "e": sp.E, "pi": sp.pi,
}

# OJO: este diccionario reemplaza por completo el entorno de eval.
# Sin esto, sympify/parse_expr inyectan TODAS las funciones nativas
# de Python (incluido __import__, open, etc.) y permiten ejecutar
# código arbitrario. Solo incluimos lo mínimo necesario para que
# los números y símbolos se construyan correctamente.
_GLOBAL_DICT_SEGURO = {
    "__builtins__": {},
    "Integer": sp.Integer,
    "Float": sp.Float,
    "Rational": sp.Rational,
    "Symbol": sp.Symbol,
}


def interpretar_funcion(entrada):
    patron = r'^\s*([A-Za-z]\w*)\s*\(\s*([A-Za-z]\w*)\s*\)\s*=\s*(.+)$'
    match = re.match(patron, entrada)

    if not match:
        raise ValueError("Formato incorrecto. Ejemplo: f(x) = x^2 + 3*x / 2")

    nombre = match.group(1)
    variable = sp.Symbol(match.group(2))
    expresion_txt = match.group(3).strip()

    if not expresion_txt:
        raise ValueError("Falta la expresión después del '='.")

    local_dict = dict(_FUNCIONES_PERMITIDAS)
    local_dict[str(variable)] = variable

    try:
        funcion = parse_expr(
            expresion_txt,
            local_dict=local_dict,
            global_dict=_GLOBAL_DICT_SEGURO,
            transformations=_TRANSFORMACIONES,
        )
    except Exception:
        raise ValueError(f"No se pudo interpretar la expresión: '{expresion_txt}'")

    extra = funcion.free_symbols - {variable}
    if extra:
        raise ValueError(
            f"La expresión usa símbolos no declarados: {', '.join(str(s) for s in extra)}"
        )

    return nombre, variable, funcion
