import os
import time
import requests
from datetime import datetime
from pathlib import Path

# === CONFIGURACIÓN ===
# URLs de las cámaras
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

# 📁 Carpeta base (en el Escritorio)
desktop = Path("C:/Users/ricky/OneDrive/Escritorio")
base_folder = desktop / "Camaras_Madrid"

# Crear la carpeta principal y subcarpetas
for nombre in CAMERAS.keys():
    (base_folder / nombre).mkdir(parents=True, exist_ok=True)

# Intervalo de tiempo (en segundos)
INTERVALO = 20 * 60  # 10 minutos


def descargar_imagen(url, nombre_base):
    """Descarga una imagen y la guarda con fecha y hora en su subcarpeta."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Ruta específica de cada cámara
        folder = base_folder / nombre_base
        nombre_limpio = nombre_base.replace("?", "_").replace("&", "_").replace("=", "_")
        filename = folder / f"{nombre_limpio}_{timestamp}.jpg"

        with open(filename, "wb") as f:
            f.write(response.content)

        print(f"✅ Imagen guardada: {filename}")

    except Exception as e:
        print(f"❌ Error al descargar {nombre_base}: {e}")


def main():
    print(f"Iniciando monitoreo... guardando imágenes cada {INTERVALO/60} minutos.")
    while True:
        for nombre, url in CAMERAS.items():
            descargar_imagen(url, nombre)
        print("⏳ Esperando próxima captura...\n")
        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()