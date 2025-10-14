from ultralytics import YOLO
import cv2
import pytesseract
import re
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# Carga modelo
model = YOLO("yolov8l.pt")

# Imagen de prueba
image_path = Path("C:/Users/ricky/OneDrive/Escritorio/Camaras_Madrid/1004/1004_2025-10-11_13-35-31.jpg")

# --- Detección YOLO ---
results = model(image_path, conf=0.5)
img = cv2.imread(str(image_path))
annotated = results[0].plot()
cv2.imshow("Detección YOLO", annotated)

# --- Regiones centradas y ampliadas ---
carretera_region = img[10:30, 80:150]
fecha_region = img[390:430, 600:830]

# 🔹 Escalar ligeramente para mejorar OCR (sin filtros de color/negro)
carretera_region = cv2.resize(carretera_region, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
fecha_region = cv2.resize(fecha_region, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

cv2.imshow("Zona Carretera (OCR)", carretera_region)
cv2.imshow("Zona Fecha/Hora (OCR)", fecha_region)

# --- OCR ---
carretera_text = pytesseract.image_to_string(carretera_region, config="--psm 7").strip()
fecha_text = pytesseract.image_to_string(fecha_region, config="--psm 7").strip()

# --- Extraer carretera ---
match = re.search(r'\b[A-Z]{1,2}-\d{1,3}\b', carretera_text)
carretera = match.group(0) if match else None

# --- Mostrar resultados ---
print("\n--- OCR Resultados ---")
print(f"Texto crudo carretera: {carretera_text}")
print(f"Carretera detectada: {carretera}")
print(f"Texto crudo fecha/hora: {fecha_text}")

cv2.waitKey(0)
cv2.destroyAllWindows()
