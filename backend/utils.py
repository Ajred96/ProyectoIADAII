import math

def calcular_conflicto(red_social, estrategia=None):
    """
    Calcula el nivel de conflicto interno de una red social, considerando una estrategia de moderación opcional.
    
    Args:
        red_social (list): Lista de tuplas (n_i, o1_i, o2_i, r_i), donde:
            - n_i: Número de agentes en el grupo.
            - o1_i, o2_i: Opiniones sobre las dos afirmaciones.
            - r_i: Rigidez del grupo (no se usa directamente en el cálculo del conflicto).
        estrategia (list, optional): Lista con el número de agentes moderados por grupo. Si es None, 
                                    se asume que no se modera a ningún agente.
    
    Returns:
        float: Valor del conflicto interno (CI).
    """
    if not red_social:
        return 0.0

    ci_numerador = 0.0
    for i, (n, o1, o2, _) in enumerate(red_social):
        agentes_no_moderados = n - (estrategia[i] if estrategia else 0)
        diferencia_cuadrado = (o1 - o2) ** 2
        ci_numerador += agentes_no_moderados * diferencia_cuadrado

    return ci_numerador / len(red_social)

def calcular_esfuerzo(red_social, estrategia):
    """
    Calcula el esfuerzo total requerido para aplicar una estrategia de moderación.
    
    Args:
        red_social (list): Lista de tuplas (n_i, o1_i, o2_i, r_i).
        estrategia (list): Lista con el número de agentes moderados por grupo.
    
    Returns:
        int: Esfuerzo total requerido.
    """
    esfuerzo_total = 0
    for i, (_, o1, o2, r) in enumerate(red_social):
        e = estrategia[i]
        esfuerzo_total += math.ceil(abs(o1 - o2) * r * e)
    return esfuerzo_total

def calcular_ci_esfuerzo(red_social, estrategia):
    """
    Calcula tanto el conflicto interno como el esfuerzo total de una estrategia.
    
    Args:
        red_social (list): Lista de tuplas (n_i, o1_i, o2_i, r_i).
        estrategia (list): Lista con el número de agentes moderados por grupo.
    
    Returns:
        tuple: (conflicto, esfuerzo), donde:
            - conflicto (float): Valor del conflicto interno.
            - esfuerzo (int): Esfuerzo total requerido.
    """
    conflicto = calcular_conflicto(red_social, estrategia)
    esfuerzo = calcular_esfuerzo(red_social, estrategia)
    return conflicto, esfuerzo

def extraer_datos_red(red_social):
    """
    Extrae y devuelve los datos de la red social en listas separadas.
    
    Args:
        red_social (list): Lista de tuplas (n_i, o1_i, o2_i, r_i).
    
    Returns:
        tuple: (n, opiniones_1, opiniones_2, rigidez), donde:
            - n (list): Número de agentes por grupo.
            - opiniones_1 (list): Opiniones sobre la afirmación 1.
            - opiniones_2 (list): Opiniones sobre la afirmación 2.
            - rigidez (list): Rigidez de cada grupo.
    """
    n = [grupo[0] for grupo in red_social]
    opiniones_1 = [grupo[1] for grupo in red_social]
    opiniones_2 = [grupo[2] for grupo in red_social]
    rigidez = [grupo[3] for grupo in red_social]
    return n, opiniones_1, opiniones_2, rigidez