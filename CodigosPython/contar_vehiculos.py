import os
import csv
import pandas as pd
from ultralytics import YOLO
from pathlib import Path
from tqdm import tqdm

# Modelo
model = YOLO('yolov3u.pt')
model.conf = 0.25

# Rutas
metadata_csv = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/fechas_imagenes.csv"
base_folder   = Path(r"C:/Users/ricky/OneDrive/Escritorio/Nuevas_Camaras_Madrid_Filtradas")
output_csv    = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/dataset_num_vehiculos.csv"

# Clases
class_names = ["car", "truck", "bus", "bike"]

# Cargo metadatos (me quedo solo con las columnas que quieres)
metadata_df = pd.read_csv(metadata_csv, dtype=str)[["id_camara", "carretera", "fecha_descarga", "hora_descarga", "url_camara"]]

# Normalizar url_camara en el dataframe (sin modificar original, crear columna auxiliar)
def norm_path(p): 
    return os.path.normpath(str(p)).lower()

metadata_df["_url_norm"] = metadata_df["url_camara"].fillna("").apply(norm_path)
metadata_df["_filename"] = metadata_df["url_camara"].fillna("").apply(lambda x: Path(x).name.lower())

# Recojo imágenes, pero por cada imagen busco su fila correcta en metadata_df
image_info = []
for cam_folder in os.listdir(base_folder):
    cam_path = base_folder / cam_folder
    if not cam_path.is_dir():
        continue

    for img_name in os.listdir(cam_path):
        if not img_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        img_path = cam_path / img_name
        img_path_str = str(img_path)
        img_norm = norm_path(img_path_str)
        img_filename = img_name.lower()

        # 1) intentar coincidencia exacta por ruta normalizada
        match = metadata_df[metadata_df["_url_norm"] == img_norm]

        # 2) si no, intentar por nombre de fichero (puede ocurrir que rutas no sean idénticas)
        if match.empty:
            match = metadata_df[metadata_df["_filename"] == img_filename]

        # 3) si aún no hay coincidencia, intentar por id_camara (carpeta) - último recurso
        if match.empty:
            try:
                match = metadata_df[metadata_df["id_camara"] == str(int(cam_folder))]
            except:
                match = pd.DataFrame()  # vacío

        if not match.empty:
            meta_row = match.iloc[0].to_dict()
        else:
            # si no hay metadata, dejar campos vacíos
            meta_row = {
                "id_camara": cam_folder,
                "carretera": "",
                "fecha_descarga": "",
                "hora_descarga": "",
                "url_camara": ""
            }

        image_info.append((str(img_path), meta_row))

print(f"📸 Total de imágenes encontradas: {len(image_info)}")

# Inferencia y guardado
results_data = []
for entry_idx, (img_path, meta_row) in enumerate(tqdm(image_info, desc="Procesando imágenes"), start=1):
    # inferencia
    results = model(img_path)
    result = results[0]
    counts = {cls: 0 for cls in class_names}
    for box in result.boxes:
        cls_id = int(box.cls[0].item())
        cls_name = result.names[cls_id]
        if cls_name in counts:
            counts[cls_name] += 1

    # id_entrada según lo pediste: guardo id_camara (si existe) como id_entrada
    id_entrada_val = meta_row.get("id_camara", "") if meta_row.get("id_camara", "") != "" else entry_idx

    results_data.append({
        "id_entrada": id_entrada_val,
        "id_camara": meta_row.get("id_camara", ""),
        "carretera": meta_row.get("carretera", ""),
        "fecha_descarga": meta_row.get("fecha_descarga", ""),
        "hora_descarga": meta_row.get("hora_descarga", ""),
        "url_camara": meta_row.get("url_camara", ""),

        "cars": counts["car"],
        "trucks": counts["truck"],
        "buses": counts["bus"],
        "bikes": counts["bike"],
        "total": sum(counts.values())
    })

# Guardar CSV con el orden de columnas que quieres
fieldnames = [
    "id_entrada",
    "id_camara",
    "carretera",
    "fecha_descarga",
    "hora_descarga",
    "url_camara",
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
