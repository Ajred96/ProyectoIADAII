import numpy as np

def calcular_conflicto(n, opiniones_1, opiniones_2):
    """Calcula el conflicto interno total de la red social."""
    total_agentes = sum(n)
    if total_agentes == 0:
        return 0
    conflicto = sum(n[i] * (opiniones_1[i] - opiniones_2[i])**2 for i in range(len(n)))
    return conflicto / total_agentes

def esfuerzo_necesario(op1, op2, rigidez, e):
    """Calcula el esfuerzo necesario para cambiar la opinión de e agentes."""
    esfuerzo = int(np.ceil(abs(op1 - op2) * rigidez * e))
    return esfuerzo

def resolver_modci(n, opiniones_1, opiniones_2, rigidez, R_max):
    """Resuelve el problema de minimización del conflicto interno usando programación dinámica."""
    num_grupos = len(n)

    # Inicializar DP con valores altos, pero no infinitos
    DP = np.full((R_max + 1, num_grupos + 1), float('inf'))
    decision = np.zeros((R_max + 1, num_grupos + 1), dtype=int)

    # 🔍 Verificar el conflicto inicial
    conflicto_inicial = calcular_conflicto(n, opiniones_1, opiniones_2)
    print(f"⚠️ Conflicto Inicial: {conflicto_inicial}")

    for r in range(R_max + 1):
        DP[r][0] = conflicto_inicial  # Base case: Sin esfuerzo, conflicto original

    # Llenado de la tabla DP
    for i in range(1, num_grupos + 1):  
        for r in range(R_max + 1):  
            DP[r][i] = DP[r][i-1]  # Opción sin cambios en este grupo
            
            for e in range(n[i-1] + 1):  
                costo = esfuerzo_necesario(opiniones_1[i-1], opiniones_2[i-1], rigidez[i-1], e)
                
                if costo <= r:
                    nuevo_n = n.copy()
                    nuevo_n[i-1] -= e  
                    
                    nuevo_conflicto = calcular_conflicto(nuevo_n, opiniones_1, opiniones_2)

                    posible_valor = DP[r - costo][i-1] - (conflicto_inicial - nuevo_conflicto)

                    if posible_valor < DP[r][i]:
                        DP[r][i] = posible_valor
                        decision[r][i] = e  

    # 🔍 Verificar el valor final en DP
    print(f"🔎 Valor esperado en DP[{R_max}][{num_grupos}]: {DP[R_max][num_grupos]}")
    
    # 🔍 Verificar la reconstrucción de la solución
    r = R_max
    cambios = [0] * num_grupos
    for i in range(num_grupos, 0, -1):
        cambios[i-1] = decision[r][i]
        r -= esfuerzo_necesario(opiniones_1[i-1], opiniones_2[i-1], rigidez[i-1], cambios[i-1])
        print(f"🔹 Decisión[{r}][{i}] = {decision[r][i]}")  

    return DP[R_max][num_grupos], cambios

# Datos de prueba
n = [7, 3, 6, 6, 5]  # Número de agentes por grupo
opiniones_1 = [-52, -44, -13, 24, 37]  # Opiniones sobre afirmación 1
opiniones_2 = [87, -27, 100, 40, -38]  # Opiniones sobre afirmación 2
rigidez = [0.372, 0.965, 0.439, 0.45, 0.18]  # Nivel de rigidez
R_max = 388  # Esfuerzo máximo

conflicto_minimo, cambios_realizados = resolver_modci(n, opiniones_1, opiniones_2, rigidez, R_max)

print(f"🚀 Conflicto mínimo alcanzado: {conflicto_minimo}")  # 🔥 ¿Llega a 5343?
print(f"🔹 Cambios realizados en cada grupo: {cambios_realizados}")
