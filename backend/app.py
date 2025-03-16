from flask import Flask, request, jsonify
from modci import modciFB
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
    print("📢 Se recibió una solicitud para el método dinámico")
    return jsonify({"mensaje": "OK"}), 200


if __name__ == '__main__':
    app.run(debug=True)
