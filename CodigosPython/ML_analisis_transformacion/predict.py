import xgboost as xgb
import joblib
import pandas as pd

# Crear objeto modelo
model = xgb.XGBClassifier()   # o XGBRegressor según tu caso

# Cargar el modelo
model.load_model("ModelosIA\\xgboost_model.json")

scaler = joblib.load("ModelosIA\\scaler.pkl")

print(scaler.feature_names_in_)

data = pd.DataFrame([{
    "id_camara": 10,
    "longitud": 1,
    "latitud": 1,
    "anio": 2026,
    "mes": 3,
    "dia": 12,
    "hora": 14,
    "minuto": 30,
    "carretera_numero": 1,
    "carretera_letra_A": 1,
    "carretera_letra_M": 0,
    "carretera_letra_N": 0,
    "franja_horaria_mañana": 0,
    "franja_horaria_noche": 0,
    "franja_horaria_tarde": 1
}])

cols_scaler = scaler.feature_names_in_

# normalizar solo esas
scaled = scaler.transform(data[cols_scaler])

scaled_df = pd.DataFrame(scaled, columns=cols_scaler)

# columnas que no se normalizan
extra = data.drop(columns=cols_scaler)

# unir todo
data_final = pd.concat([scaled_df, extra], axis=1)

# asegurar orden correcto de columnas
data_final = data_final[model.get_booster().feature_names]

# predecir
pred = model.predict(data_final)

print(pred)