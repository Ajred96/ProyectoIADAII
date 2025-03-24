from flask import Flask, request, jsonify
from flask_cors import CORS
from modciFB import modciFB
from modciPD import modciPD
from modciPV import modciPV
import time

app = Flask(__name__)
CORS(app)

def procesar_archivo(archivo):
    """Lee el archivo de texto y convierte los datos a la estructura esperada."""
    if not archivo:
        return None, jsonify({"error": "No se proporcionó un archivo"}), 400

    try:
        lineas = archivo.read().decode('utf-8').strip().split('\n')
        if len(lineas) < 2:
            raise ValueError("El archivo no tiene suficientes datos")

        n = int(lineas[0])
        if len(lineas) < n + 2:
            raise ValueError("El archivo no contiene todas las líneas esperadas")

        red_social = [
            (int(datos[0]), int(datos[1]), int(datos[2]), float(datos[3])) 
            for datos in (linea.split(',') for linea in lineas[1:n + 1])
        ]
        r_max = int(lineas[n + 1])

        return (red_social, r_max), None, None

    except (ValueError, IndexError):
        return None, jsonify({"error": "Error en el formato del archivo"}), 400

def ejecutar_metodo(metodo, red_social, r_max):
    """Ejecuta el método seleccionado y devuelve el resultado."""
    try:
        tiempo_inicio = time.time()
        if metodo == 'fuerzaBruta':
            ci, esfuerzo, estrategia = modciFB(red_social, r_max)
        elif metodo == 'dinamico':
            ci, esfuerzo, estrategia = modciPD(red_social, r_max)  # Ahora retorna los mismos 3 valores
        elif metodo == 'voraz':
            ci, esfuerzo, estrategia = modciPV(red_social, r_max)
        else:
            return jsonify({"error": "Método no válido"}), 400
        tiempo = round(time.time() - tiempo_inicio, 4)
        respuesta = {"CI": ci, "Esfuerzo": esfuerzo, "Estrategia": estrategia, "Tiempo": tiempo}
        print("📢 Respuesta enviada al frontend:", respuesta)  # Depuración
        return jsonify(respuesta)
    
    except Exception as e:
        return jsonify({"error": f"Error al ejecutar el método: {str(e)}"}), 500

@app.route('/procesar/<metodo>', methods=['POST'])
def procesar_metodo(metodo):
    """Recibe el archivo y ejecuta el método seleccionado."""
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

    ci, esfuerzo, estrategia = resolver_modci(red_social, r_max)

    respuesta = {"CI": ci, "Esfuerzo": esfuerzo, "Estrategia": estrategia}
    print("📢 Respuesta enviada al frontend:", respuesta)  # 👀 Agregar print para depuración

    return jsonify(respuesta)


if __name__ == '__main__':
    app.run(debug=True)
