import pandas as pd
import re

# Cargar el dataset original
full_dataset = pd.read_csv('full_dataset_ocupacion.csv')

# Función para extraer fecha y hora del nombre del archivo en image_path
def extraer_fecha_hora(image_path):
    # Buscar patrón de fecha y hora en el nombre del archivo
    match = re.search(r'(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})', image_path)
    if match:
        fecha = match.group(1)
        hora = match.group(2).replace('-', ':')  # Cambiar guiones por dos puntos en la hora
        return fecha, hora
    else:
        return None, None

# Aplicar la función al dataset
full_dataset[['fecha_descarga', 'hora_descarga']] = full_dataset['image_path'].apply(
    lambda x: pd.Series(extraer_fecha_hora(x))
)

# Guardar el nuevo CSV
full_dataset.to_csv('dataset_completo.csv', index=False)

print("CSV creado con fecha y hora actualizadas desde image_path.")
