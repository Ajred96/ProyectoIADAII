import math

def calcular_conflicto(red_social, estrategia=None):
    """
    Calcula el nivel de conflicto considerando la estructura de la red social.
    
    Args:
    - red_social: Lista de tuplas (n, o1, o2, r) donde:
        - n  -> número de agentes en el grupo
        - o1 -> opinión inicial del grupo
        - o2 -> opinión de referencia
        - r  -> rigidez del grupo (no se usa aquí)
    - estrategia: (Opcional) Lista con la cantidad de agentes moderados en cada grupo.
    
    Returns:
    - conflicto: Nivel de conflicto calculado.
    - total_agentes: Número total de agentes considerados.
    """
    ci_numerador = 0
    ci_denominador = len(red_social)
    for i, (n, o1, o2, _) in enumerate(red_social):  
        moderados = estrategia[i] if estrategia else 0
        agentes_restantes = n - moderados
        diferencia_cuadrado = (o1 - o2) ** 2

        ci_numerador += agentes_restantes * diferencia_cuadrado

    conflicto = ci_numerador / ci_denominador if ci_denominador > 0 else 0
    return conflicto, ci_denominador

def esfuerzo_necesario(op1, op2, rigidez, e):
    """
    Calcula el esfuerzo necesario para moderar e agentes en función de la rigidez y diferencia de opiniones.
    """
    return int(math.ceil(abs(op1 - op2) * rigidez * e))

def extraer_datos_red(red_social):
    """
    Extrae y devuelve las listas necesarias desde red_social.
    
    Args:
    - red_social: Lista de tuplas (n, o1, o2, r).
    
    Returns:
    - n: Lista con la cantidad de agentes por grupo.
    - opiniones_1: Lista con las opiniones iniciales de cada grupo.
    - opiniones_2: Lista con las opiniones de referencia de cada grupo.
    - rigidez: Lista con la rigidez de cada grupo.
    """
    n = [grupo[0] for grupo in red_social]
    opiniones_1 = [grupo[1] for grupo in red_social]
    opiniones_2 = [grupo[2] for grupo in red_social]
    rigidez = [grupo[3] for grupo in red_social]
    
    return n, opiniones_1, opiniones_2, rigidez

def calcular_ci_esfuerzo(red_social, estrategia):
    """
    Calcula el nivel de conflicto y el esfuerzo total dados una red social y una estrategia de moderación.
    """
    esfuerzo_total = sum(
        esfuerzo_necesario(o1, o2, r, estrategia[i]) 
        for i, (_, o1, o2, r) in enumerate(red_social)
    )

    # Usamos calcular_conflicto para obtener el conflicto
    ci, _ = calcular_conflicto(red_social, estrategia)
    
    return ci, esfuerzo_total