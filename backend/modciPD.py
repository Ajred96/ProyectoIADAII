import math
from utils import esfuerzo_necesario, extraer_datos_red, calcular_ci_esfuerzo

def actualizar_dp(dp, i, used_effort, total_rem, S, decisions, n, opiniones_1, opiniones_2, rigidez, d, R_max):
    """Actualiza la tabla de programación dinámica con nuevas decisiones."""
    for e in range(n[i] + 1):
        cost = esfuerzo_necesario(opiniones_1[i], opiniones_2[i], rigidez[i], e)
        new_effort = used_effort + cost
        if new_effort <= R_max:
            new_rem = n[i] - e
            new_total = total_rem + new_rem
            new_S = S + new_rem * d[i]
            new_decisions = decisions + [e]
            if new_effort not in dp[i+1]:
                dp[i+1][new_effort] = {}
            if new_total not in dp[i+1][new_effort] or new_S < dp[i+1][new_effort][new_total][0]:
                dp[i+1][new_effort][new_total] = (new_S, new_decisions)
                
def seleccionar_mejor_estrategia(dp, num_grupos):
    """Selecciona la mejor estrategia minimizando el conflicto interno."""
    best_conflict = float('inf')
    best_state = None
    best_decisions = None

    for used_effort in dp[num_grupos]:
        for total_rem, (S, decisions) in dp[num_grupos][used_effort].items():
            conflict = S / num_grupos if num_grupos > 0 else 0
            if conflict < best_conflict:
                best_conflict = conflict
                best_state = (used_effort, total_rem, S)
                best_decisions = decisions

    return best_conflict, best_state, best_decisions


def modciPD(red_social, R_max):
    """Calcula la mejor estrategia de moderación usando programación dinámica.
    
    Args:
        red_social (list of tuples): Lista de grupos (n_i, op1_i, op2_i, rigidez_i), donde:
            - n_i (int): Personas en el grupo.
            - op1_i, op2_i (float): Opinión inicial y objetivo.
            - rigidez_i (float): Factor de resistencia al cambio.
        R_max (float): Esfuerzo máximo disponible.

    Returns:
        tuple: (CI óptimo, Esfuerzo total, Estrategia óptima)
            - CI óptimo (float): Conflicto interno mínimo alcanzado.
            - Esfuerzo total (float): Recursos usados en la estrategia.
            - Estrategia óptima (list of int): Esfuerzo asignado a cada grupo.
            
    """
    num_grupos = len(red_social)
    # Extraemos datos con la función modular
    n, opiniones_1, opiniones_2, rigidez = extraer_datos_red(red_social)
    # Precalcular valores
    d = [(opiniones_1[i] - opiniones_2[i])**2 for i in range(num_grupos)]
    # Inicializar DP
    dp = [dict() for _ in range(num_grupos+1)]
    dp[0][0] = {0: (0, [])}

    for i in range(num_grupos):
        dp[i+1] = dict()
        for used_effort in dp[i]:
            for total_rem, (S, decisions) in dp[i][used_effort].items():
                actualizar_dp(dp, i, used_effort, total_rem, S, decisions, n, opiniones_1, opiniones_2, rigidez, d, R_max)

    # Encontrar mejor solución usando calcular_conflicto
    best_conflict, best_state, best_decisions = seleccionar_mejor_estrategia(dp, num_grupos)

    if best_state is None:
        return None, None, None

    ci, esfuerzo = calcular_ci_esfuerzo(red_social, best_decisions)

    return ci, esfuerzo, best_decisions
