import os
import pandas as pd
import numpy as np
from ultralytics import YOLO
from tqdm import tqdm
import torch

input_csv = "full_dataset.csv"
output_csv = "dataset_completo.csv"
class_names = ["car", "truck", "bus", "bike"]

model = YOLO("yolov8x-seg.pt")  
model.conf = 0.25

# === FUNCIONES AUXILIARES ===
def calcular_ocupacion_visual(result, classes_of_interest):
    """Calcula el porcentaje del área de la imagen ocupado por vehículos."""
    masks = result.masks
    if masks is None:
        return 0.0

    mask_array = masks.data.cpu().numpy()  
    cls_ids = result.boxes.cls.cpu().numpy()

    combined_mask = np.zeros(mask_array.shape[1:], dtype=bool)
    for i, cls_id in enumerate(cls_ids):
        cls_name = result.names[int(cls_id)]
        if cls_name in classes_of_interest:
            combined_mask |= mask_array[i] > 0.5

    area_total = combined_mask.size
    area_vehiculos = np.sum(combined_mask)
    return area_vehiculos / area_total


def nivel_ocupacion_por_area(area_ratio):
    """Convierte el porcentaje de área ocupada en nivel 0–3."""
    if area_ratio < 0.02:
        return 0  
    elif area_ratio < 0.07:
        return 1  
    elif area_ratio < 0.15:
        return 2  
    else:
        return 3  


# === CARGAR CSV EXISTENTE ===
df = pd.read_csv(input_csv)
print(f"📄 CSV original cargado: {len(df)} filas")

# === CALCULAR OCUPACIÓN VISUAL POR IMAGEN ===
niveles = []

for img_path in tqdm(df["image_path"], desc="Analizando imágenes con YOLOv8-seg"):
    try:
        results = model(img_path)
        result = results[0]
        area_ratio = calcular_ocupacion_visual(result, class_names)
        nivel = nivel_ocupacion_por_area(area_ratio)
    except Exception as e:
        print(f"⚠️ Error procesando {img_path}: {e}")
        area_ratio = 0.0
        nivel = 0

    niveles.append(nivel)

# === AÑADIR COLUMNAS AL DATAFRAME ===
df["nivel_ocupacion"] = niveles

# === GUARDAR NUEVO CSV ===
df.to_csv(output_csv, index=False, encoding="utf-8")
print(f"✅ Nuevo CSV guardado en: {output_csv}")