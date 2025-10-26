import os
import time
import requests
import csv
from datetime import datetime
from pathlib import Path
import cv2
import numpy as np
import re

# ==========================
# CONFIGURACIÓN
# ==========================

JSON_URL = "https://www.dgt.es/.content/.assets/json/camaras.json"

CAMERAS = {
    "169709": "https://infocar.dgt.es/etraffic/data/camaras/169709.jpg?t=1759834159649",
    "169708": "https://infocar.dgt.es/etraffic/data/camaras/169708.jpg?t=1759834159649",
    "826": "https://infocar.dgt.es/etraffic/data/camaras/826.jpg?t=1759834225500",
    "1160": "https://infocar.dgt.es/etraffic/data/camaras/1160.jpg?t=1759834275729",
    "1676": "https://infocar.dgt.es/etraffic/data/camaras/1676.jpg?t=1759834314977",
    "1690": "https://infocar.dgt.es/etraffic/data/camaras/1690.jpg?t=1759834314977",
    "696": "https://infocar.dgt.es/etraffic/data/camaras/696.jpg?t=1759834334403",
    "598": "https://infocar.dgt.es/etraffic/data/camaras/598.jpg?t=1759833949373",
    "972": "https://infocar.dgt.es/etraffic/data/camaras/972.jpg?t=1759834549446",
    "967": "https://infocar.dgt.es/etraffic/data/camaras/967.jpg?t=1759834616716",
    "866": "https://infocar.dgt.es/etraffic/data/camaras/866.jpg?t=1759834632512",
    "877": "https://infocar.dgt.es/etraffic/data/camaras/877.jpg?t=1759834647410",
    "169741": "https://infocar.dgt.es/etraffic/data/camaras/169741.jpg?t=1759834658332",
    "864": "https://infocar.dgt.es/etraffic/data/camaras/864.jpg?t=1759834676245",
    "971": "https://infocar.dgt.es/etraffic/data/camaras/971.jpg?t=1759834562471",
    "651": "https://infocar.dgt.es/etraffic/data/camaras/651.jpg?t=1759834201645",
    "771": "https://infocar.dgt.es/etraffic/data/camaras/771.jpg?t=1759836052767",
    "773": "https://infocar.dgt.es/etraffic/data/camaras/773.jpg?t=1759836066876",
    "926": "https://infocar.dgt.es/etraffic/data/camaras/926.jpg?t=1759836128476",
    "1010": "https://infocar.dgt.es/etraffic/data/camaras/1010.jpg?t=1759836140679",
    "1004": "https://infocar.dgt.es/etraffic/data/camaras/1004.jpg?t=1759836140679",
    "731": "https://infocar.dgt.es/etraffic/data/camaras/731.jpg?t=1759836179328",
    "1125": "https://infocar.dgt.es/etraffic/data/camaras/1125.jpg?t=1759836204192",
    "791": "https://infocar.dgt.es/etraffic/data/camaras/791.jpg?t=1759836223066",
    "799": "https://infocar.dgt.es/etraffic/data/camaras/799.jpg?t=1759836245366",
    "169372": "https://infocar.dgt.es/etraffic/data/camaras/169372.jpg?t=1759836024932",
    "634": "https://infocar.dgt.es/etraffic/data/camaras/634.jpg?t=1760080607575",
    "660": "https://infocar.dgt.es/etraffic/data/camaras/660.jpg?t=1760080639359",
    "668": "https://infocar.dgt.es/etraffic/data/camaras/668.jpg?t=1760080677092",
    "798": "https://infocar.dgt.es/etraffic/data/camaras/798.jpg?t=1760080721584",
    "866": "https://infocar.dgt.es/etraffic/data/camaras/866.jpg?t=1760081080580",
    "872": "https://infocar.dgt.es/etraffic/data/camaras/872.jpg?t=1760081121352",
    "868": "https://infocar.dgt.es/etraffic/data/camaras/868.jpg?t=1760081126624",
    "873": "https://infocar.dgt.es/etraffic/data/camaras/873.jpg?t=1760081077226",
    "1161": "https://infocar.dgt.es/etraffic/data/camaras/1161.jpg?t=1760081224769",
    "1162": "https://infocar.dgt.es/etraffic/data/camaras/1162.jpg?t=1760081228225",
    "1158": "https://infocar.dgt.es/etraffic/data/camaras/1158.jpg?t=1760081233373",
    "897": "https://infocar.dgt.es/etraffic/data/camaras/897.jpg?t=1760081239666",
    "174942": "https://infocar.dgt.es/etraffic/data/camaras/174942.jpg?t=1760081301918",
    "174943": "https://infocar.dgt.es/etraffic/data/camaras/174943.jpg?t=1760081369602",
    "174945": "https://infocar.dgt.es/etraffic/data/camaras/174945.jpg?t=1760081332946",
    "673": "https://infocar.dgt.es/etraffic/data/camaras/673.jpg?t=1760081474663",
    "677": "https://infocar.dgt.es/etraffic/data/camaras/677.jpg?t=1760081492738",
    "1097": "https://infocar.dgt.es/etraffic/data/camaras/1097.jpg?t=1760081497164",
    "705": "https://infocar.dgt.es/etraffic/data/camaras/705.jpg?t=1760081557152",
    "726": "https://infocar.dgt.es/etraffic/data/camaras/726.jpg?t=1760081590777",
    "175471": "https://infocar.dgt.es/etraffic/data/camaras/175471.jpg?t=1760174424650",
}

desktop = Path("C:/Users/ricky/OneDrive/Escritorio")
base_folder = desktop / "Camaras_Madrid"
csv_path = Path("C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/fechas_imagenes.csv")

# Crear carpetas
for nombre in CAMERAS.keys():
    (base_folder / nombre).mkdir(parents=True, exist_ok=True)

# Crear CSV si no existe
if not csv_path.exists():
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "camera_id",
            "carretera",
            "fecha_json",
            "hora_json",
            "fecha_descarga",
            "hora_descarga",
            "file_path"
        ])

# Intervalo (17.5 minutos)
INTERVALO = 17.5 * 60


# ==========================
# FUNCIONES
# ==========================

def cargar_datos_json(url):
    """Descarga y prepara el diccionario con metadatos de las cámaras."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # El JSON tiene una clave "camaras" que contiene la lista
        if isinstance(data, dict) and "camaras" in data:
            camaras = data["camaras"]
        elif isinstance(data, list):
            camaras = data
        else:
            print("⚠️ Estructura JSON no esperada (no hay 'camaras').")
            return {}

        cam_data = {}
        for cam in camaras:
            cam_id = cam.get("id")
            if cam_id:
                cam_data[cam_id] = cam

        print(f"📥 JSON cargado correctamente con {len(cam_data)} cámaras.")
        return cam_data

    except Exception as e:
        print(f"⚠️ No se pudo cargar el JSON: {e}")
        return {}


def add_timestamp_to_image(image_bytes, timestamp):
    """Añade texto con fecha/hora a la imagen descargada."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.0
    color = (255, 255, 255)
    thickness = 2
    text_x = 10
    text_y = img.shape[0] - 20

    cv2.putText(img, timestamp, (text_x + 2, text_y + 2), font, font_scale, (0, 0, 0), thickness + 1)
    cv2.putText(img, timestamp, (text_x, text_y), font, font_scale, color, thickness)

    _, buffer = cv2.imencode(".jpg", img)
    return buffer.tobytes()


def descargar_imagen(url, camera_id, cam_data):
    """Descarga una imagen de cámara y la guarda con su metadata."""
    try:
        meta = cam_data.get(camera_id, {})
        carretera = meta.get("carretera", "desconocida")
        fecha_json = meta.get("fecha", "N/A")
        if " " in fecha_json:
            fecha_json, hora_json = fecha_json.split(" ")
        else:
            hora_json = "N/A"

        response = requests.get(url, timeout=10)
        response.raise_for_status()

        ahora = datetime.now()
        fecha = ahora.strftime("%Y-%m-%d")
        hora = ahora.strftime("%H:%M:%S")
        timestamp = f"{fecha}_{hora.replace(':', '-')}"  # para nombre del archivo

        image_with_text = add_timestamp_to_image(response.content, f"{fecha} {hora}")

        folder = base_folder / camera_id
        filename = folder / f"{camera_id}_{timestamp}.jpg"
        with open(filename, "wb") as f:
            f.write(image_with_text)

        with open(csv_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([camera_id, carretera, fecha_json, hora_json, fecha, hora, str(filename)])

        print(f"✅ Imagen guardada y registrada: {filename}")

    except Exception as e:
        print(f"❌ Error al descargar {camera_id}: {e}")


# ==========================
# BUCLE PRINCIPAL
# ==========================

def main():
    print(f"Iniciando monitoreo... guardando imágenes cada {INTERVALO/60:.1f} minutos.\n")

    while True:
        cam_data = cargar_datos_json(JSON_URL)

        for cam_id, url in CAMERAS.items():
            descargar_imagen(url, cam_id, cam_data)

        print("\n⏳ Esperando próxima captura...\n")
        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()