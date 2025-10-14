import easyocr
import cv2
import re
from pathlib import Path
import matplotlib.pyplot as plt

# Crear lector EasyOCR
reader = easyocr.Reader(['es'], gpu=False)

# Cargar imagen
image_path = Path("C:/Users/ricky/OneDrive/Escritorio/Camaras_Madrid/872/872_2025-10-11_11-28-09.jpg")
img = cv2.imread(str(image_path))
if img is None:
    raise FileNotFoundError(f"No se pudo abrir la imagen: {image_path}")

h, w, _ = img.shape

# --- 1️⃣ Recortes más amplios (para que funcione con varias cámaras) ---
zona_inferior = img[int(h*0.75):h, int(w*0.5):w]         # esquina inferior derecha

# --- 2️⃣ Escalado y gris para mejorar OCR ---
def prepare(region):
    region = cv2.resize(region, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)
    return gray

fecha_img = prepare(zona_inferior)

# --- 3️⃣ OCR en ambas zonas ---
fecha_results = reader.readtext(fecha_img)

# --- 4️⃣ Extraer textos detectados ---
def extract_text(results):
    return " ".join([text for (_, text, _) in results])

fecha_text = extract_text(fecha_results)

# Fecha/hora: 11-10-2025 13:22:32 o 11/10/2025 13:22
fecha_match = re.search(r'\d{2}[-/]\d{2}[-/]\d{4}\s\d{2}:\d{2}(?::\d{2})?', fecha_text)
fecha = fecha_match.group(0) if fecha_match else None

# --- 6️⃣ Mostrar resultados ---
print("\n--- OCR Resultados ---")
print(f"Texto crudo zona inferior: {fecha_text}")
print(f"Fecha/Hora detectada: {fecha}")

# --- 7️⃣ Mostrar regiones OCR ---
def show_image(img, title="Imagen"):
    plt.figure(figsize=(8, 6))
    if len(img.shape) == 3:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imshow(img_rgb)
    else:
        plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

show_image(fecha_img, "Zona inferior (Fecha/Hora)")