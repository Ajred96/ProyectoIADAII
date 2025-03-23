from flask import Flask, request, jsonify
from modciFB import modciFB
from modciPD import modciPD
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def procesar_archivo(archivo):
    """Lee el archivo de texto y convierte los datos a la estructura esperada."""
    if not archivo:
        return None, jsonify({"error": "No se proporcionó un archivo"}), 400

    lineas = archivo.read().decode('utf-8').strip().split('\n')

    # Validar que hay al menos una línea
    if len(lineas) < 2:
        return None, jsonify({"error": "El archivo no tiene suficientes datos"}), 400

    try:
        n = int(lineas[0])
        if len(lineas) < n + 2:  # n líneas de datos + 1 para R_max
            return None, jsonify({"error": "El archivo no contiene todas las líneas esperadas"}), 400

        red_social = [(int(datos[0]), int(datos[1]), int(datos[2]), float(datos[3])) for datos in
                      (linea.split(',') for linea in lineas[1:n + 1])]
        r_max = int(lineas[n + 1])
    except ValueError:
        return None, jsonify({"error": "Error en el formato del archivo"}), 400

    return (red_social, r_max), None, None

@app.route('/procesar/<metodo>', methods=['POST'])
def procesar_metodo(metodo):
    archivo = request.files.get('file')
    datos, error_respuesta, codigo = procesar_archivo(archivo)
    if error_respuesta:
        return error_respuesta, codigo

    red_social, r_max = datos

    if metodo == 'fuerzaBruta':
        ci, esfuerzo, estrategia = modciFB(red_social, r_max)
    elif metodo == 'dinamico':
        # Convertir datos a listas separadas para modciPD
        n = [grupo[0] for grupo in red_social]
        opiniones_1 = [grupo[1] for grupo in red_social]
        opiniones_2 = [grupo[2] for grupo in red_social]
        rigidez = [grupo[3] for grupo in red_social]
        ci, estrategia = modciPD(n, opiniones_1, opiniones_2, rigidez, r_max)
        esfuerzo = sum(estrategia[i] * abs(opiniones_1[i] - opiniones_2[i]) * rigidez[i] for i in range(len(n)))
    elif metodo == 'voraz':
        return jsonify({"mensaje": "Método voraz aún no implementado"}), 200
    else:
        return jsonify({"error": "Método no válido"}), 400

    respuesta = {"CI": ci, "Esfuerzo": esfuerzo, "Estrategia": estrategia}
    print("📢 Respuesta enviada al frontend:", respuesta)  # 👀 Depuración
    return jsonify(respuesta)

if __name__ == '__main__':
    app.run(debug=True)
