from PIL import Image, ImageDraw, ImageFont
import random, os
from datetime import datetime, timedelta

os.makedirs("dataset_fechas", exist_ok=True)

font = ImageFont.truetype("arial.ttf", 32)

for i in range(2000):
    # Fondo gris o negro
    bg = Image.new("RGB", (300, 80), color=(random.randint(0,30),)*3)
    draw = ImageDraw.Draw(bg)
    
    # Fecha aleatoria
    fecha = (datetime.now() - timedelta(days=random.randint(0, 365)))
    texto = fecha.strftime("%d-%m-%Y %H:%M:%S")
    
    # Dibujar con color aleatorio
    draw.text((10, 20), texto, font=font, fill=(random.randint(200,255),)*3)
    
    # Añadir ruido o variaciones
    if random.random() > 0.5:
        bg = bg.rotate(random.uniform(-2, 2))
    
    bg.save(f"dataset_fechas/{i:04d}_{texto.replace(':','-')}.png")