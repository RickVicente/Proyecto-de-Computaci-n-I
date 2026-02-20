import os
import csv
import numpy as np
import pandas as pd
from ultralytics import YOLO
from pathlib import Path
from tqdm import tqdm

model = YOLO("yolov8x-seg.pt")
model.conf = 0.25

class_names = ["car", "truck", "bus", "bike"]

metadata_csv = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/1. fechas_imagenes.csv"
base_folder  = Path(r"C:/Users/ricky/OneDrive/Escritorio/Nuevas_Camaras_Madrid_Filtradas")
output_csv   = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/3. datasetCompleto.csv"

metadata_df = pd.read_csv(metadata_csv, dtype=str)[
    ["id_camara", "carretera", "fecha_descarga", "hora_descarga", "url_camara"]
]

def norm_path(p):
    return os.path.normpath(str(p)).lower()

metadata_df["_url_norm"] = metadata_df["url_camara"].fillna("").apply(norm_path)
metadata_df["_filename"] = metadata_df["url_camara"].fillna("").apply(lambda x: Path(x).name.lower())

def calcular_ocupacion_visual(result):
    masks = result.masks
    if masks is None:
        return 0.0

    mask_array = masks.data.cpu().numpy()
    cls_ids = result.boxes.cls.cpu().numpy()

    combined_mask = np.zeros(mask_array.shape[1:], dtype=bool)
    for i, cls_id in enumerate(cls_ids):
        cls_name = result.names[int(cls_id)]
        if cls_name in class_names:
            combined_mask |= mask_array[i] > 0.5

    return np.sum(combined_mask) / combined_mask.size


def nivel_ocupacion_por_area(area_ratio):
    if area_ratio < 0.02:
        return 0
    elif area_ratio < 0.07:
        return 1
    elif area_ratio < 0.15:
        return 2
    else:
        return 3

rows = []
entry_idx = 1

cam_folders = [f for f in os.listdir(base_folder) if (base_folder / f).is_dir()]

for cam_folder in tqdm(cam_folders, desc="Procesando cámaras"):
    cam_path = base_folder / cam_folder

    for img_name in os.listdir(cam_path):
        if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        img_path = cam_path / img_name
        img_norm = norm_path(img_path)
        img_filename = img_name.lower()

        # ---- buscar metadata ----
        match = metadata_df[metadata_df["_url_norm"] == img_norm]
        if match.empty:
            match = metadata_df[metadata_df["_filename"] == img_filename]
        if match.empty:
            match = metadata_df[metadata_df["id_camara"] == cam_folder]

        meta = match.iloc[0].to_dict() if not match.empty else {
            "id_camara": cam_folder,
            "carretera": "",
            "fecha_descarga": "",
            "hora_descarga": "",
            "url_camara": str(img_path)
        }

        # ---- inferencia YOLO ----
        try:
            result = model(str(img_path))[0]

            counts = {c: 0 for c in class_names}
            for box in result.boxes:
                cls = result.names[int(box.cls[0])]
                if cls in counts:
                    counts[cls] += 1

            area_ratio = calcular_ocupacion_visual(result)
            nivel = nivel_ocupacion_por_area(area_ratio)

        except Exception as e:
            print(f"⚠️ Error en {img_path}: {e}")
            counts = {c: 0 for c in class_names}
            nivel = 0

        # ---- guardar fila ----
        rows.append({
            "id_entrada": entry_idx,
            "id_camara": meta.get("id_camara", ""),
            "carretera": meta.get("carretera", ""),
            "fecha_descarga": meta.get("fecha_descarga", ""),
            "hora_descarga": meta.get("hora_descarga", ""),
            "url_camara": meta.get("url_camara", str(img_path)),

            "cars": counts["car"],
            "trucks": counts["truck"],
            "buses": counts["bus"],
            "bikes": counts["bike"],
            "total": sum(counts.values()),

            "nivel_ocupacion": nivel
        })

        entry_idx += 1

with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("Completado")
