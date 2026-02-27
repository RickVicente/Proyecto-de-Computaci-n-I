import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

input_csv = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/2. datasetNormalizado.csv"
output_csv   = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/3. datasetNormalizadoSinImagen.csv"

df = pd.read_csv(input_csv, encoding='utf-8')

df = df.drop(columns=['url_camara','cars','bikes','trucks','buses','total'])

df.to_csv(output_csv, index=False)