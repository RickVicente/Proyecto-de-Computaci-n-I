import pandas as pd
from pathlib import Path
from detect_objects import detect_vehicles
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Carpeta principal
base_folder = Path("C:/Users/ricky/OneDrive/Escritorio/Camaras_Madrid")
codes_folder = Path("C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/PythonStuff")

def generar_dataset():
    registros = []
    
    for subcarpeta in base_folder.iterdir():
        if subcarpeta.is_dir():
            for imagen in subcarpeta.glob("*.jpg"):
                info = detect_vehicles(imagen)
                total = info["coches"] + info["camiones"] + info["buses"] + info["motos"]
                info["total_vehiculos"] = total
                info["camara"] = subcarpeta.name
                registros.append(info)

    df = pd.DataFrame(registros)
    df.to_csv(codes_folder / "dataset.csv", index=False, encoding="utf-8")
    print("✅ Dataset generado sin etiquetas:", codes_folder / "dataset.csv")

if __name__ == "__main__":
    generar_dataset()