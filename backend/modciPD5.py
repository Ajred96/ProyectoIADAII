import numpy as np

def calcular_conflicto(n, opiniones_1, opiniones_2):
    """Calcula el conflicto interno total de la red social."""
    total_agentes = sum(n)
    conflicto = sum(n[i] * (opiniones_1[i] - opiniones_2[i])**2 for i in range(len(n)))
    return conflicto / total_agentes if total_agentes > 0 else 0

def esfuerzo_necesario(op1, op2, rigidez, e):
    """Calcula el esfuerzo necesario para cambiar la opinión de e agentes."""
    return np.ceil(abs(op1 - op2) * rigidez * e).astype(int)

def resolver_modci(n, opiniones_1, opiniones_2, rigidez, R_max):
    """Resuelve el problema de minimización del conflicto interno usando programación dinámica."""
    num_grupos = len(n)

    # Inicialización de la tabla DP y de decisiones
    DP = np.full((R_max + 1, num_grupos + 1), float('inf'))
    decision = np.zeros((R_max + 1, num_grupos + 1), dtype=int)

    # Caso base: Si no se usa esfuerzo, el conflicto es el original
    for r in range(R_max + 1):
        DP[r][0] = calcular_conflicto(n, opiniones_1, opiniones_2)

    # Llenado de la tabla DP
    for i in range(1, num_grupos + 1):  # Recorrer los grupos de agentes
        for r in range(R_max + 1):  # Recorrer los valores de esfuerzo
            DP[r][i] = DP[r][i-1]  # Caso base: No cambiar ningún agente
            for e in range(n[i-1] + 1):  # Probar cambiar desde 0 hasta todos los agentes del grupo
                costo = esfuerzo_necesario(opiniones_1[i-1], opiniones_2[i-1], rigidez[i-1], e)
                if costo <= r:
                    nuevo_n = n.copy()
                    nuevo_n[i-1] -= e  # Reducimos el número de agentes con conflicto
                    nuevo_conflicto = calcular_conflicto(nuevo_n, opiniones_1, opiniones_2)
                    if DP[r - costo][i-1] + nuevo_conflicto < DP[r][i]:
                        DP[r][i] = DP[r - costo][i-1] + nuevo_conflicto
                        decision[r][i] = e  # Guardar cuántos agentes se cambiaron

    # Reconstrucción de la solución
    r = R_max
    cambios = [0] * num_grupos
    for i in range(num_grupos, 0, -1):
        cambios[i-1] = decision[r][i]
        r -= esfuerzo_necesario(opiniones_1[i-1], opiniones_2[i-1], rigidez[i-1], cambios[i-1])

    return DP[R_max][num_grupos], cambios

# Ejemplo de uso
n = [7, 3, 6, 6, 5]  # Número de agentes por grupo
opiniones_1 = [-52, -44, -13, 24, 37]  # Opiniones sobre afirmación 1
opiniones_2 = [87, -27, 100, 40, -38]  # Opiniones sobre afirmación 2
rigidez = [0.372, 0.965, 0.439, 0.45, 0.18]  # Nivel de rigidez
R_max = 388  # Esfuerzo máximo

conflicto_minimo, cambios_realizados = resolver_modci(n, opiniones_1, opiniones_2, rigidez, R_max)
print(f"Conflicto mínimo alcanzado: {conflicto_minimo}")
print(f"Cambios realizados en cada grupo: {cambios_realizados}")