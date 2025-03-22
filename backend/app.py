from flask import Flask, request, jsonify
from modciFB import modciFB
from modciPD3 import resolver_modci_dp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/procesar/fuerzaBruta', methods=['POST'])
def procesar_archivo():
    archivo = request.files.get('file')
    if not archivo:
        return jsonify({"error": "No se proporcionó un archivo"}), 400

    lineas = archivo.read().decode('utf-8').strip().split('\n')

    # Validar que hay al menos una línea
    if len(lineas) < 2:
        return jsonify({"error": "El archivo no tiene suficientes datos"}), 400

    try:
        n = int(lineas[0])
        if len(lineas) < n + 2:  # n líneas de datos + 1 para R_max
            return jsonify({"error": "El archivo no contiene todas las líneas esperadas"}), 400

        red_social = [(int(datos[0]), int(datos[1]), int(datos[2]), float(datos[3])) for datos in
                      (linea.split(',') for linea in lineas[1:n + 1])]
        r_max = int(lineas[n + 1])
    except ValueError:
        return jsonify({"error": "Error en el formato del archivo"}), 400

    ci, esfuerzo, estrategia = modciFB(red_social, r_max)

    respuesta = {"CI": ci, "Esfuerzo": esfuerzo, "Estrategia": estrategia}
    print("📢 Respuesta enviada al frontend:", respuesta)  # 👀 Agregar print para depuración

    return jsonify(respuesta)


@app.route('/procesar/voraz', methods=['POST'])
def procesar_voraz():
    print("📢 Se recibió una solicitud para el método voraz")
    return jsonify({"mensaje": "OK"}), 200


@app.route('/procesar/dinamico', methods=['POST'])
def procesar_dinamico():
    archivo = request.files.get('file')
    if not archivo:
        return jsonify({"error": "No se proporcionó un archivo"}), 400

    lineas = archivo.read().decode('utf-8').strip().split('\n')

    # Validar que hay al menos una línea
    if len(lineas) < 2:
        return jsonify({"error": "El archivo no tiene suficientes datos"}), 400

    try:
        # Leer la cantidad de grupos
        num_grupos = int(lineas[0])
        if len(lineas) < num_grupos + 2:  # num_grupos líneas de datos + 1 para R_max
            return jsonify({"error": "El archivo no contiene todas las líneas esperadas"}), 400

        # Inicializar listas para almacenar los datos
        n = []  # Número de agentes por grupo
        opiniones_1 = []  # Opiniones sobre afirmación 1
        opiniones_2 = []  # Opiniones sobre afirmación 2
        rigidez = []  # Nivel de rigidez

        # Procesar cada línea de datos
        for i in range(1, num_grupos + 1):
            datos = lineas[i].split(',')
            if len(datos) != 4:
                return jsonify({"error": f"Formato incorrecto en la línea {i + 1}"}), 400

            n.append(int(datos[0]))
            opiniones_1.append(int(datos[1]))
            opiniones_2.append(int(datos[2]))
            rigidez.append(float(datos[3]))

        # Leer el esfuerzo máximo (R_max)
        R_max = int(lineas[num_grupos + 1])

    except ValueError as e:
        return jsonify({"error": f"Error en el formato del archivo: {str(e)}"}), 400

    # Llamar a la función resolver_modci_dp con los datos extraídos
    conflicto_minimo, cambios_realizados = resolver_modci_dp(n, opiniones_1, opiniones_2, rigidez, R_max)

    if conflicto_minimo is None:
        return jsonify({"error": "No se pudo encontrar una solución válida"}), 400


    respuesta = {
        "CI": conflicto_minimo,  # Conflicto mínimo es equivalente a CI
        "Esfuerzo": sum(cambios_realizados),  # Esfuerzo total es la suma de los cambios
        "Estrategia": cambios_realizados  # La estrategia son los cambios realizados
    }
    print("📢 Respuesta enviada al frontend:", respuesta)  # 👀 Agregar print para depuración

    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True)
