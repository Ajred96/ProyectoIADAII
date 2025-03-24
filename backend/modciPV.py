from utils import calcular_ci_esfuerzo

def modciPV(red_social, r_max):
    """
    Algoritmo voraz para minimizar el conflicto interno con un esfuerzo máximo permitido.

    Args:
        red_social (list of tuples): Lista de grupos (n_i, op1_i, op2_i, rigidez_i), donde:
            - n_i (int): Personas en el grupo.
            - op1_i, op2_i (float): Opinión inicial y objetivo.
            - rigidez_i (float): Factor de resistencia al cambio.
        r_max (float): Esfuerzo máximo disponible.

    Returns:
        tuple: (CI resultante, Esfuerzo total usado, Estrategia seleccionada)
            - CI resultante (float): Conflicto interno después de la moderación.
            - Esfuerzo total usado (float): Recursos empleados en la estrategia.
            - Estrategia seleccionada (list of int): Esfuerzo asignado a cada grupo.
    """
    
    ##Por definir
    return None, None, None