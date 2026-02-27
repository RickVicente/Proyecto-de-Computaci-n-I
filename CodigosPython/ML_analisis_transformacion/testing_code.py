import pandas as pd
from sklearn.preprocessing import MinMaxScaler, LabelEncoder

label_encoder = LabelEncoder()
scalerX = MinMaxScaler()

dataset1 = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/2. datasetNormalizado.csv"
output_csv   = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/3. datasetNormalizadoSinImagen.csv"

df = pd.read_csv(dataset1, encoding='utf-8')

newDf = df.drop(columns=['url_camara'])

newDf.to_csv(output_csv, index=False)