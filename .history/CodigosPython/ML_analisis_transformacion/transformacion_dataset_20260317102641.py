import pandas as pd
<<<<<<< HEAD

# Dataset original
metadata_csv = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasetCompleto.csv"
=======
import joblib
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

label_encoder = LabelEncoder()
scalerX = MinMaxScaler()

metadata_csv = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/1. datasetCompleto.csv"
output_csv   = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/2. datasetNormalizado.csv"
>>>>>>> a66f306294db34458acb6ea05ffe9bc1f5174696

df = pd.read_csv(metadata_csv, encoding='utf-8')

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

<<<<<<< HEAD
# One-hot encoding para la franja horaria
=======
>>>>>>> a66f306294db34458acb6ea05ffe9bc1f5174696
df = pd.get_dummies(df, columns=['franja_horaria'])
cols_one_hot = ['franja_horaria_mañana','franja_horaria_noche','franja_horaria_tarde']
df[cols_one_hot] = df[cols_one_hot].astype(int)

<<<<<<< HEAD
# Eliminar columnas innecesarias
df = df.drop(columns=['carretera','fecha_descarga','hora_descarga','url_camara']) # Quitar url_camara si se necesita cargar el dataset para CNN

# Guardar dataset transformado
df.to_csv("dataset_transformado_ML.csv", index=False)
=======
df = df.drop(columns=['cars','trucks','buses','bikes','total','url_camara','carretera','fecha_descarga','hora_descarga','segundo'])

df['carretera_numero'] = label_encoder.fit_transform(df['carretera_numero'])

variables = ['id_camara','latitud','longitud','anio','mes','dia','hora','minuto','carretera_numero']
df[variables] = scalerX.fit_transform(df[variables])

df = df.sample(frac=1).reset_index(drop=True)

joblib.dump(scalerX, "scaler.pkl")
df.to_csv(output_csv, index=False)
>>>>>>> a66f306294db34458acb6ea05ffe9bc1f5174696
