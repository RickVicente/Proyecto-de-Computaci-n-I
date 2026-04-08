from flask import Flask, request, jsonify, send_file, session, redirect
import sqlite3
import pymysql

def get_mysql_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='pc2',
        cursorclass=pymysql.cursors.DictCursor
    )
import os
import requests
from CodigosPython.ML_analisis_transformacion.analisis_imagen_actual import calcular_nivel_trafico

app = Flask(__name__)
# 🔐 CLAVE SECRETA OBLIGATORIA para encriptar las cookies de sesión (pon lo que quieras)
app.secret_key = "madrive_super_secreta_2025"

DB_NAME = "madrive_users.db"

# ─── RUTAS PARA SERVIR HTML ──────────────────────────────────
@app.route("/")
def index():
    # Si ya tiene una sesión iniciada, lo mandamos al mapa directo
    if "user_id" in session:
        return redirect("/mapa")

    if os.path.exists("login.html"):
        return send_file("login.html")
    return "Error: No se encuentra login.html", 404

@app.route("/mapa")
def mapa():
    # 🛑 SEGURIDAD: Comprobar si el que está pidiendo entrar está logueado
    if "user_id" not in session:
        # Si no lo está, lo mandamos expulsado al login ("/")
        return redirect("/")

    if os.path.exists("mapa.html"):
        return send_file("mapa.html")
    if os.path.exists("mio.html"):
        return send_file("mio.html")
    return "Error: No se encuentra mapa.html ni mio.html", 404

# ─── ENDPOINT DE LOGIN (Hardcodeado temporalmente) ────────────
@app.route("/api/login", methods=["POST"])
def login():
    datos = request.json
    email = datos.get("email")
    password = datos.get("password")

    if not email or not password:
        return jsonify({"success": False, "message": "Faltan datos."}), 400

    # 🛑 LOGIN HARCODEADO 🛑 (Sustituye a SQLite temporalmente)
    if email == "admin@madrive.es" and password == "123456":
        # ✅ GUARDAR LA SESIÓN DEL USUARIO (ID inventado 1)
        session["user_id"] = 1 
        
        return jsonify({"success": True, "message": "Login correcto.", "redirect": "/mapa"})
    else:
        # Credenciales erróneas
        return jsonify({"success": False, "message": "Usuario o contraseña incorrectos."}), 401

# ─── ENDPOINT DE IA (Predicción real) ────────────────────────────

# Importamos la función de predicción
import sys
from pathlib import Path

# Añadimos la ruta de ML_analisis_transformacion al path para poder importar predict.py
base_path = Path(__file__).resolve().parent
ml_path = base_path / "CodigosPython" / "ML_analisis_transformacion"
sys.path.append(str(ml_path))

try:
    from CodigosPython.ML_analisis_transformacion.predict import hacer_prediccion
    from CodigosPython.ML_analisis_transformacion.analisis_imagen_actual import calcular_nivel_trafico
except ImportError as e:
    print(f"⚠️ Aviso: no se pudo importar predict.py. ({e})")
    hacer_prediccion = None


@app.route("/predecir", methods=["POST"])
def predecir():
    if not hacer_prediccion:
        return jsonify({"error": "El servidor no tiene cargado el módulo predict.py."}), 500

    datos = request.json
    
    # 1. Preparar las 15 variables exactas que espera el modelo
    input_model = {
        "id_camara": int(datos.get("id_camara", 0)),
        "longitud": float(datos.get("longitud", 0.0)),
        "latitud": float(datos.get("latitud", 0.0)),
        "anio": int(datos.get("anio", 2026)),
        "mes": int(datos.get("mes", 1)),
        "dia": int(datos.get("dia", 1)),
        "hora": int(datos.get("hora", 12)),
        "minuto": int(datos.get("minuto", 0)),
        "carretera_numero": int(datos.get("carretera_numero", 0)),
        "carretera_letra_A": int(datos.get("carretera_letra_A", 0)),
        "carretera_letra_M": int(datos.get("carretera_letra_M", 0)),
        "carretera_letra_N": int(datos.get("carretera_letra_N", 0)),
        "franja_horaria_mañana": int(datos.get("franja_horaria_mañana", 0)),
        "franja_horaria_noche": int(datos.get("franja_horaria_noche", 0)),
        "franja_horaria_tarde": int(datos.get("franja_horaria_tarde", 0))
    }

    try:
        # 2. Llamar a la función importada de python
        nivel = hacer_prediccion(input_model)
        
        # 3. Mapear el nivel de tráfico a algo visual
        if nivel == 0:
            desc = "Tráfico Fluido"
            color = "#22cc44"  # Verde
        elif nivel == 1:
            desc = "Tráfico Denso"
            color = "#ffc107"  # Amarillo
        elif nivel == 2:
            desc = "Atasco"
            color = "#f57c00"  # Naranja
        else: # nivel 3
            desc = "Tráfico Muy Congestionado"
            color = "#d32f2f"  # Rojo

        return jsonify({
            "success": True,
            "nivel": nivel,
            "descripcion": desc,
            "color": color,
            "camara": input_model["id_camara"],
            "carretera": f"Cámara Analizada",
            "fecha": f"{input_model['dia']}/{input_model['mes']}/{input_model['anio']}",
            "hora": f"{input_model['hora']:02d}:{input_model['minuto']:02d}"
        })

    except Exception as e:
        print(f"Error prediciendo: {e}")
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/analizar_imagen", methods=["POST"])
def analizar_imagen():
    data = request.json
    img_url = data.get("url")

    if not img_url:
        return jsonify({"error": "No se proporcionó URL"}), 400

    temp_path = "temp.jpg"

    try:
        # Descargar imagen desde la DGT
        img_data = requests.get(img_url).content
        with open(temp_path, 'wb') as f:
            f.write(img_data)

        # 🔥 TU MODELO
        nivel, area_ratio = calcular_nivel_trafico(temp_path)

        if nivel == 0:
            desc = "Tráfico Fluido"
            color = "#22cc44"
        elif nivel == 1:
            desc = "Tráfico Denso"
            color = "#ffc107"
        elif nivel == 2:
            desc = "Atasco"
            color = "#f57c00"
        else:
            desc = "Muy Congestionado"
            color = "#d32f2f"

        return jsonify({
            "nivel": nivel,
            "descripcion": desc,
            "color": color,
            "ocupacion": float(area_ratio)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

try:
    from CodigosPython.ML_analisis_transformacion.descargar_imagenes import ejecutar_descarga
    from CodigosPython.ML_analisis_transformacion.transformacion_dataset import normalizar_dataset
except ImportError as e:
    print(f"⚠️ Aviso: no se pudo importar descargar_imagenes.py. ({e})")
    ejecutar_descarga = None
    normalizar_dataset = None

@app.route("/descargar_dataset", methods=["POST"])
def descargar_dataset():
    if "user_id" not in session:
        return jsonify({"error": "No autorizado"}), 401

    try:
        ejecutar_descarga()
        normalizar_dataset()

        return jsonify({
            "success": True,
            "message": "Dataset actualizado correctamente"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

DATASET_CSV = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/2. datasetNormalizado.csv"

@app.route("/reentrenar", methods=["POST"])
def reentrenar():
    try:
        import pandas as pd
        import xgboost as xgb

        df = pd.read_csv(DATASET_CSV)

        X = df.drop(columns=["id_entrada", "nivel_ocupacion"])
        y = df["nivel_ocupacion"]

        model = xgb.XGBClassifier()
        model.fit(X, y)

        model.save_model("xgboost_model.json")

        return jsonify({"success": True, "message": "Modelo reentrenado"})

    except Exception as e:
        return jsonify({"error": str(e)})

JSON_URL = "https://www.dgt.es/.content/.assets/json/camaras.json"

@app.route("/api/zonas", methods=["GET"])
def get_zonas():
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_zona, latitud, longitud, carretera, pk FROM zonas")
            rows = cursor.fetchall()
            zonas = []
            for row in rows:
                zonas.append({
                    "id": str(row['id_zona']),
                    "lat": float(row['latitud']) if row['latitud'] else 0.0,
                    "lon": float(row['longitud']) if row['longitud'] else 0.0,
                    "road": row['carretera'] or "",
                    "pk": row['pk'] or ""
                })
        conn.close()
        return jsonify({"success": True, "camaras": zonas})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/camaras_disponibles", methods=["GET"])
def camaras_disponibles():
    try:
        r = requests.get(JSON_URL, timeout=10)
        data = r.json()

        camaras = data.get("camaras", [])

        return jsonify({
            "success": True,
            "camaras": camaras
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/camaras_activas", methods=["GET"])
def camaras_activas():
    try:
        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT id_zona FROM zonas")
            ids = [str(row['id_zona']) for row in cursor.fetchall()]
        conn.close()
        return jsonify({"ids": ids})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/add_camara", methods=["POST"])
def add_camara():
    data = request.json

    cam_id = data.get("id")
    nombre = data.get("nombre", f"Camara {cam_id}")
    descripcion = data.get("descripcion", "")

    try:
        # 🔍 Buscar en JSON DGT
        r = requests.get(JSON_URL)
        camaras = r.json().get("camaras", [])

        cam = next((c for c in camaras if str(c["id"]) == str(cam_id)), None)

        if not cam:
            return jsonify({"error": "Cámara no encontrada en DGT"}), 404

        lat = float(cam["latitud"])
        lon = float(cam["longitud"])
        carretera = cam.get("carretera", "")
        pk = str(cam.get("pk", ""))

        conn = get_mysql_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT IGNORE INTO zonas (id_zona, latitud, longitud, carretera, pk, descripcion)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (cam_id, lat, lon, carretera, pk, descripcion))
        conn.commit()
        conn.close()

        return jsonify({"success": True, "message": "Cámara añadida"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Arranca Flask en el puerto 5000 (Ojo: tendrás que cambiar el puerto en mapa.html si el puerto cambió de 8000 a 5000)
    print("▶ Iniciando Servidor MaDrive en http://localhost:5000")
    print("▶ Usuario por defecto: admin@madrive.es / Clave: 123456")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
