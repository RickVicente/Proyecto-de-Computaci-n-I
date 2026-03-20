from flask import Flask, request, jsonify, send_file, session, redirect
import sqlite3
import os

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

if __name__ == '__main__':
    # Arranca Flask en el puerto 5000 (Ojo: tendrás que cambiar el puerto en mapa.html si el puerto cambió de 8000 a 5000)
    print("▶ Iniciando Servidor MaDrive en http://localhost:5000")
    print("▶ Usuario por defecto: admin@madrive.es / Clave: 123456")
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
