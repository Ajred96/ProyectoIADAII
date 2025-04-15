from utils import calcular_ci_esfuerzo, extraer_datos_red
import math

import math

def utilidad_base(o1, o2, rigidez):
    """
    Heurística base: |o1 - o2| / rigidez.
    Prioriza grupos con alta diferencia de opiniones y baja rigidez.
    """
    rigidez = max(rigidez, 1e-6)  # Evita divisiones por valores muy pequeños
    diferencia = abs(o1 - o2)
    return diferencia / rigidez

def modciPV(red_social, R_max):
    """
    Resuelve el problema ModCI usando un enfoque voraz.
    
    Args:
        red_social (list): Lista de tuplas (n_i, o1_i, o2_i, r_i).
        R_max (int): Esfuerzo máximo permitido.
    
    Returns:
        tuple: (conflicto, esfuerzo, estrategia).
    """
    n, opiniones_1, opiniones_2, rigidez = extraer_datos_red(red_social)
    num_grupos = len(red_social)
    estrategia = [0] * num_grupos
    esfuerzo_restante = R_max

    # Calcular utilidades para cada grupo
    utilidades = []
    for i in range(num_grupos):
        if n[i] == 0:
            continue
        
        utilidad = utilidad_base(opiniones_1[i], opiniones_2[i], rigidez[i])
        esfuerzo_por_agente = max(1, math.ceil(abs(opiniones_1[i] - opiniones_2[i]) * rigidez[i]))
        utilidades.append((utilidad, i, esfuerzo_por_agente))

    # Ordenar por utilidad descendente
    utilidades.sort(reverse=True, key=lambda x: x[0])

    # Asignar agentes a moderar
    for _, i, esfuerzo_unitario in utilidades:
        if esfuerzo_restante <= 0:
            break
        
        max_posible = min(n[i], esfuerzo_restante // esfuerzo_unitario)
        if max_posible > 0:
            estrategia[i] = max_posible
            esfuerzo_restante -= max_posible * esfuerzo_unitario

    return calcular_ci_esfuerzo(red_social, estrategia) + (estrategia,)