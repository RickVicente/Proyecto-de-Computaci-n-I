import pandas as pd

# Dataset original
df = pd.read_csv("dataset_completo.csv")

# Separar fecha y hora
df[['anio', 'mes', 'dia']] = df['fecha_descarga'].str.split('-', expand=True)
df[['hora', 'minuto', 'segundo']] = df['hora_descarga'].str.split(':', expand=True)

# Extraer letra y número de carretera
df['carretera_letra'] = df['carretera'].str.extract(r'([A-Z]+)')
df['carretera_numero'] = df['carretera'].str.extract(r'(\d+)')

# Convertir columnas numéricas a int
df[['anio','mes','dia','hora','minuto','segundo','carretera_numero']] = df[['anio','mes','dia','hora','minuto','segundo','carretera_numero']].astype(int)

# One-hot encoding para la letra de la carretera
df = pd.get_dummies(df, columns=['carretera_letra'])
cols_one_hot = ['carretera_letra_A', 'carretera_letra_M', 'carretera_letra_N']
df[cols_one_hot] = df[cols_one_hot].astype(int)

# Crear categorías de franjas horarias
def franja_horaria(hora):
    if 6 <= hora <= 11:
        return 'mañana'
    elif 12 <= hora <= 17:
        return 'tarde'
    elif 18 <= hora <= 23:
        return 'noche'
    else:
        return 'madrugada'

df['franja_horaria'] = df['hora'].apply(franja_horaria)

# One-hot encoding para la franja horaria
df = pd.get_dummies(df, columns=['franja_horaria'])
cols_one_hot = ['franja_horaria_mañana','franja_horaria_noche','franja_horaria_tarde']
df[cols_one_hot] = df[cols_one_hot].astype(int)

# Eliminar columnas innecesarias
df = df.drop(columns=['carretera','fecha_descarga','hora_descarga','url_camara', 'image_path'])

# Guardar dataset transformado
df.to_csv("dataset_transformado.csv", index=False)
