import math
from utils import extraer_datos_red, calcular_ci_esfuerzo

def actualizar_dp(dp, i, used_effort, total_rem, S, decisions, n, opiniones_1, opiniones_2, rigidez, d, R_max):
    """Actualiza la tabla DP usando math.ceil directamente (evitando llamada redundante a utils)."""
    for e in range(n[i] + 1):
        cost = math.ceil(abs(opiniones_1[i] - opiniones_2[i]) * rigidez[i] * e)  # Cálculo directo
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
    """Devuelve solo el conflicto y las decisiones óptimas."""
    best_conflict = float('inf')
    best_decisions = None

    for used_effort in dp[num_grupos]:
        for total_rem, (S, decisions) in dp[num_grupos][used_effort].items():
            conflict = S / num_grupos if num_grupos > 0 else 0
            if conflict < best_conflict:
                best_conflict = conflict
                best_decisions = decisions

    return best_conflict, best_decisions


def modciPD(red_social, R_max):
    num_grupos = len(red_social)
    if num_grupos == 0:
        return 0.0, 0, []

    n, opiniones_1, opiniones_2, rigidez = extraer_datos_red(red_social)
    d = [(o1 - o2)**2 for o1, o2 in zip(opiniones_1, opiniones_2)]

    # Inicializar DP: dp[i][used_effort][total_rem] = (S, decisions)
    dp = [{} for _ in range(num_grupos + 1)]
    dp[0][0] = {0: (0.0, [])}

    for i in range(num_grupos):
        dp[i+1] = {}
        for used_effort in dp[i]:
            for rem, (S, decisions) in dp[i][used_effort].items():
                actualizar_dp(dp, i, used_effort, rem, S, decisions, n, opiniones_1, opiniones_2, rigidez, d, R_max)

    best_conflict, best_decisions = seleccionar_mejor_estrategia(dp, num_grupos)

    if best_decisions is None:
        return float('inf'), 0, []

    return calcular_ci_esfuerzo(red_social, best_decisions) + (best_decisions,)