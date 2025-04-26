from itertools import product
from utils import calcular_ci_esfuerzo

def modciFB(red_social, r_max):
    """
    Algoritmo de fuerza bruta para minimizar el conflicto interno con un esfuerzo máximo permitido.

    Args:
        red_social (list of tuples): Lista de grupos (n_i, op1_i, op2_i, rigidez_i), donde:
            - n_i (int): Personas en el grupo.
            - op1_i, op2_i (float): Opinión inicial y objetivo.
            - rigidez_i (float): Factor de resistencia al cambio.
        r_max (float): Esfuerzo máximo disponible.
    Returns:
        tuple: (CI óptimo, Esfuerzo total, Estrategia óptima)
            - CI óptimo (float): Conflicto interno mínimo alcanzado.
            - Esfuerzo total (float): Recursos usados en la estrategia.
            - Estrategia óptima (list of int): Esfuerzo asignado a cada grupo.
    """
    mejor_ci, mejor_esfuerzo, mejor_estrategia = float('inf'), 0, []

    # Generar todas las combinaciones de estrategias
    estrategias = [[]]

    for grupo in red_social:
        nuevas_estrategias = []
        for estrategia in estrategias:
            for e in range(grupo[0] + 1):  # Generar valores de esfuerzo de 0 a n
                nuevas_estrategias.append(estrategia + [e])
        estrategias = nuevas_estrategias  # Reemplazar con la nueva lista de combinaciones

    # Evaluar cada estrategia
    for estrategia in estrategias:
        ci, esfuerzo = calcular_ci_esfuerzo(red_social, estrategia)
        if esfuerzo <= r_max and ci < mejor_ci:
            mejor_ci, mejor_esfuerzo, mejor_estrategia = ci, esfuerzo, estrategia

    return mejor_ci, mejor_esfuerzo, mejor_estrategia
