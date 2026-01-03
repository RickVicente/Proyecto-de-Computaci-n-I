import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Ruta del CSV original
csv_path = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/5. dataset_transformado_DL.csv"

label_encoder = LabelEncoder()
# Cargar CSV
df = pd.read_csv(csv_path)

# -----------------------------
# Normalización Min-Max manual
# -----------------------------

df["id_camara"] = df["id_camara"] / 200000
df["cars"] = df["cars"] / 200
df["trucks"] = df["trucks"] / 50
df["buses"] = df["buses"] / 30
df["bikes"] = df["bikes"] / 50
df["total"] = df["total"] / 330

df["anio"] = df["anio"] / 2030
df["mes"] = df["mes"] / 12
df["dia"] = df["dia"] / 31
df["hora"] = df["hora"] / 23
df["minuto"] = df["minuto"] / 59
df["segundo"] = df["segundo"] / 59

df['carretera_numero'] = label_encoder.fit_transform(df['carretera_numero'])

df.drop(columns={"segundo"}, axis=1, inplace=True)
# df.drop(columns={"cars", "trucks", "buses", "bikes", "total", "segundo"}, axis=1, inplace=True)

df = df.sample(frac=1, random_state=42).reset_index(drop=True)

output_path = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/8. dataset_DL.csv"
df.to_csv(output_path, index=False)

print("CSV normalizado guardado en:")
print(output_path)