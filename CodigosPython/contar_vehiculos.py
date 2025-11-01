import os
import csv
import pandas as pd
from ultralytics import YOLO
from pathlib import Path
from tqdm import tqdm  # barra de progreso
import torch

model = YOLO('yolov3.pt')  # se descargará automáticamente
model.conf = 0.25

metadata_csv = "fechas_imagenes.csv"
base_folder = Path("C:/Users/ricky/OneDrive/Escritorio/Nuevas_Camaras_Madrid_Filtradas")
output_csv = "full_dataset.csv"

class_names = ["car", "truck", "bus", "bike"]

# === CARGAR METADATOS ===
metadata_df = pd.read_csv(metadata_csv)[["id_camara", "carretera", "fecha_descarga", "hora_descarga", "url_camara"]]

# === RECOGER TODAS LAS IMÁGENES ===
image_info = []  
for cam_folder in os.listdir(base_folder):
    cam_path = base_folder / cam_folder
    if not cam_path.is_dir():
        continue

    cam_metadata = metadata_df[metadata_df["id_camara"] == int(cam_folder)]
    meta_row = cam_metadata.iloc[0].to_dict() if not cam_metadata.empty else {
        "id_camara": cam_folder,
        "carretera": "",
        "fecha_descarga": "",
        "hora_descarga": "",
        "url_camara": ""
    }

    for img_name in os.listdir(cam_path):
        if img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            img_path = cam_path / img_name
            image_info.append((str(img_path), meta_row))

print(f"📸 Total de imágenes encontradas: {len(image_info)}")

# === INFERENCIA EN BATCH ===
results_data = []
for entry_id, (img_path, meta_row) in enumerate(tqdm(image_info, desc="Procesando imágenes"), start=1):
    
    results = model(img_path)
    result = results[0]  
    counts = {cls: 0 for cls in class_names}

    for box in result.boxes:
        cls_id = int(box.cls[0].item())
        cls_name = result.names[cls_id]
        if cls_name in counts:
            counts[cls_name] += 1

    results_data.append({
        "id_entrada": entry_id,
        **meta_row,
        "image_path": img_path,
        "cars": counts["car"],
        "trucks": counts["truck"],
        "buses": counts["bus"],
        "bikes": counts["bike"],
        "total": sum(counts.values())
    })

# === GUARDAR CSV ===
fieldnames = [
    "id_entrada",
    "id_camara",
    "carretera",
    "fecha_descarga",
    "hora_descarga",
    "url_camara",
    "image_path",
    "cars",
    "trucks",
    "buses",
    "bikes",
    "total"
]

with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(results_data)

print(f"✅ Procesado completado. CSV generado en: {output_csv}")
