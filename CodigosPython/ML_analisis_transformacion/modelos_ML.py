import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier
import joblib

metadata_csv = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/dataset_transformado_ML.csv"

data = pd.read_csv(metadata_csv, encoding='utf-8')

target_column = "nivel_ocupacion"
X = data.drop(columns=[target_column])  
y = data[target_column]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

modelos = {
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "Naive Bayes": GaussianNB(),
    "XGBoost": XGBClassifier(eval_metric='mlogloss', use_label_encoder=False)
}

resultados = {}

for nombre, modelo in modelos.items():
    if nombre in ["KNN", "Naive Bayes"]:
        modelo.fit(X_train_scaled, y_train)
        y_pred = modelo.predict(X_test_scaled)
    else:
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    resultados[nombre] = acc
    print(f"Modelo: {nombre} - Accuracy: {acc}")

mejor_modelo = max(resultados, key=resultados.get)
print("\n=== Mejor modelo encontrado ===")
print(f"Modelo: {mejor_modelo} - Accuracy: {resultados[mejor_modelo]}")

modelo_final = modelos[mejor_modelo]
joblib.dump(modelo_final, "mejor_modelo_ML.pkl")
print("\nModelo exportado como 'mejor_modelo.pkl'")