import pandas as pd

# Cargar el CSV
df = pd.read_csv('C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/dataset_completo.csv')  # Cambia por la ruta del archivo

# Crear un nuevo id secuencial (1, 2, 3, ...)
df['id_entrada'] = range(1, len(df) + 1)

# Guardar el resultado
df.to_csv('datasetCompleto.csv', index=False)

print(df.head())