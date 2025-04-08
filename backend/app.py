from flask import Flask, request, jsonify
from flask_cors import CORS
from modciFB import modciFB
from modciPD import modciPD
from modciPV import modciPV
from utils import calcular_conflicto
import os
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

def guardar_resultado(ci, esfuerzo, estrategia, filename, metodo):
    """Guarda el resultado en un archivo con el formato requerido."""
    nombre_base = os.path.splitext(filename)[0]
    nombre_salida = f"{nombre_base}_{metodo}.txt"

    with open(nombre_salida, 'w') as f:
        f.write(f"{ci}\n")
        f.write(f"{esfuerzo}\n")
        for mod in estrategia:
            f.write(f"{mod}\n")
    
    print(f"📁 Resultado guardado en: {nombre_salida}")
    
    
def ejecutar_metodo(metodo, red_social, r_max, nombre_archivo):
    """Ejecuta el método seleccionado y devuelve el resultado."""
    try:
        tiempo_inicial = time.time()
        if metodo == 'fuerzaBruta':
            ci, esfuerzo, estrategia = modciFB(red_social, r_max)
        elif metodo == 'dinamico':
            ci, esfuerzo, estrategia = modciPD(red_social, r_max)  # Ahora retorna los mismos 3 valores
        elif metodo == 'voraz':
            ci, esfuerzo, estrategia = modciPV(red_social, r_max)
        else:
            return jsonify({"error": "Método no válido"}), 400
        tiempo = round(time.time() - tiempo_inicial, 4)
        guardar_resultado(ci, esfuerzo, estrategia, nombre_archivo, metodo)
        respuesta = {"CI": ci, "Esfuerzo": esfuerzo, "Estrategia": estrategia, "Tiempo": tiempo}
        print("📢 Respuesta enviada al frontend:", respuesta)  # Depuración
        return jsonify(respuesta)
    except Exception as e:
        return jsonify({"error": f"Error al ejecutar el método: {str(e)}"}), 500
    


@app.route('/procesar/<metodo>', methods=['POST'])
def procesar_metodo(metodo):
    """Recibe el archivo y ejecuta el método seleccionado."""
    archivo = request.files.get('file')
    datos, error_respuesta, codigo = procesar_archivo(archivo)
    if error_respuesta:
        return error_respuesta, codigo

    red_social, r_max = datos

    nombre_base = os.path.splitext(archivo.filename)[0]

    try:
        tiempo_inicial = time.time()
        if metodo == 'fuerzaBruta':
            ci, esfuerzo, estrategia = modciFB(red_social, r_max)
        elif metodo == 'dinamico':
            ci, esfuerzo, estrategia = modciPD(red_social, r_max)
        elif metodo == 'voraz':
            ci, esfuerzo, estrategia = modciPV(red_social, r_max)
        else:
            return jsonify({"error": "Método no válido"}), 400

        tiempo = round(time.time() - tiempo_inicial, 4)
        respuesta = {"CI": ci, "Esfuerzo": esfuerzo, "Estrategia": estrategia, "Tiempo": tiempo}

        nombre_archivo = f"../BateriaPruebas_Proyecto1_2025-I/ResultadosPruebas/{nombre_base}_{metodo}.txt"
        with open(nombre_archivo, 'w') as f:
            f.write(f"{ci}\n")
            f.write(f"{esfuerzo}\n")
            for valor in estrategia:
                f.write(f"{valor}\n")

        print("📢 Respuesta enviada al frontend:", respuesta)
        return jsonify(respuesta)
    except Exception as e:
        return jsonify({"error": f"Error al ejecutar el método: {str(e)}"}), 500
    
@app.route('/calcular_ci', methods=['POST'])
def calcular_ci_inicial():
    """Recibe el archivo y calcula el conflicto interno."""
    archivo = request.files.get('file')
    datos, error_respuesta, codigo = procesar_archivo(archivo)
    if error_respuesta:
        return error_respuesta, codigo

    red_social, _ = datos
    estrategia_str = request.form.get('estrategia')  # 👈 aquí el cambio
    estrategia = eval(estrategia_str) if estrategia_str else None  # o usa json.loads si es JSON puro

    ci = calcular_conflicto(red_social, estrategia)
    return jsonify({"CI": ci})

if __name__ == '__main__':
    app.run(debug=True)
