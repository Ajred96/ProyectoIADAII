import math

def calcular_conflicto_vec(n, opiniones_1, opiniones_2):
    total_agentes = sum(n)
    if total_agentes == 0:
        return 0
    conflict = sum(n[i] * (opiniones_1[i] - opiniones_2[i])**2 for i in range(len(n)))
    return conflict / total_agentes

def esfuerzo_necesario(op1, op2, rigidez, e):
    return int(math.ceil(abs(op1 - op2) * rigidez * e))

def modciPD(n, opiniones_1, opiniones_2, rigidez, R_max):
    num_grupos = len(n)
    # Precalcular el cuadrado de la diferencia (para el conflicto) y la diferencia absoluta (para el esfuerzo)
    d = [(opiniones_1[i] - opiniones_2[i])**2 for i in range(num_grupos)]
    diff = [abs(opiniones_1[i] - opiniones_2[i]) for i in range(num_grupos)]

    # dp[i] será una estructura en la que para los primeros i grupos se almacena:
    # clave: esfuerzo utilizado hasta el momento
    # valor: un diccionario que mapea (total de agentes restantes) a (S, lista de decisiones)
    dp = [dict() for _ in range(num_grupos+1)]
    # Estado inicial: 0 grupos procesados, 0 esfuerzo usado, 0 agentes acumulados y S = 0.
    dp[0][0] = {0: (0, [])}

    for i in range(num_grupos):
        dp[i+1] = dict()
        # Para cada estado alcanzado con los primeros i grupos:
        for used_effort in dp[i]:
            for total_rem, (S, decisions) in dp[i][used_effort].items():
                # Para el grupo i se prueba moderar de 0 a n[i] agentes
                for e in range(n[i] + 1):
                    cost = esfuerzo_necesario(opiniones_1[i], opiniones_2[i], rigidez[i], e)
                    new_effort = used_effort + cost
                    if new_effort <= R_max:
                        new_rem = n[i] - e  # Agentes que quedan en el grupo i
                        new_total = total_rem + new_rem
                        new_S = S + new_rem * d[i]
                        new_decisions = decisions + [e]
                        # Se actualiza el estado en dp[i+1] para el esfuerzo new_effort y total new_total
                        if new_effort not in dp[i+1]:
                            dp[i+1][new_effort] = {}
                        # Si para ese esfuerzo y total no hay estado o se encontró uno con S mayor, se actualiza
                        if new_total not in dp[i+1][new_effort] or new_S < dp[i+1][new_effort][new_total][0]:
                            dp[i+1][new_effort][new_total] = (new_S, new_decisions)

    # Se busca, entre todos los estados alcanzados (para todos los niveles de esfuerzo <= R_max),
    # aquel que minimice el conflicto: conflict = S / (total de agentes restantes) (o 0 si no quedan agentes)
    best_conflict = float('inf')
    best_state = None
    for used_effort in dp[num_grupos]:
        for total_rem, (S, decisions) in dp[num_grupos][used_effort].items():
            if total_rem == 0:
                conflict = 0
            else:
                conflict = S / total_rem
            if conflict < best_conflict:
                best_conflict = conflict
                best_state = (used_effort, total_rem, S, decisions)

    if best_state is None:
        return None, None
    else:
        return best_conflict, best_state[3]  # conflict y la lista de decisiones
