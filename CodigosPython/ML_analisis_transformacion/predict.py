import xgboost as xgb
import pandas as pd

# Crear objeto modelo
model = xgb.XGBClassifier()   # o XGBRegressor según tu caso

# Cargar el modelo
model.load_model("C:\Users\ricky\OneDrive\Universidad\3º Año\1 - Proyecto de Computación I\Proyecto de Computacion\ModelosIA\xgboost_model.json")

data = pd.DataFrame({
    "id_camara":[10],
    "longitud":[5.2],
    "lagitud":[1],
    "anio":[],
    "mes":[],
    "dia":[],
    "hora":[],
    "minuto":[],
    "carretera_letra_A":[],
    "carretera_letra_M":[],
    "carretera_letra_N":[],
    "franja_horaria_mañana":[],
    "franja_horaria_noche":[],
    "franja_horaria_tarde":[]
})

pred = model.predict(data)
print(pred)