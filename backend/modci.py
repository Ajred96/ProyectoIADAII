import math
from itertools import product

def modciFB(red_social, r_max):
    n = len(red_social)
    mejor_estrategia = []
    mejor_ci = float('inf')
    mejor_esfuerzo = 0

    for estrategia in product(*(range(0, grupo[0] + 1) for grupo in red_social)):
        ci, esfuerzo = calcular_ci_esfuerzo(red_social, estrategia)
        if esfuerzo <= r_max and ci < mejor_ci:
            mejor_ci = ci
            mejor_esfuerzo = esfuerzo
            mejor_estrategia = estrategia

    return mejor_ci, mejor_esfuerzo, mejor_estrategia

def calcular_ci_esfuerzo(red_social, estrategia):
    ci_numerador = 0
    ci_denominador = 0
    esfuerzo_total = 0

    for i, (n_i, o1, o2, r) in enumerate(red_social):
        e_i = estrategia[i]
        esfuerzo_total += math.ceil(abs(o1 - o2) * r * e_i)
        ci_numerador += (n_i - e_i) * (o1 - o2) ** 2
        ci_denominador += (n_i - e_i)

    ci = ci_numerador / ci_denominador if ci_denominador > 0 else 0
    return ci, esfuerzo_total
