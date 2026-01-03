import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.pipeline import Pipeline
from imblearn.over_sampling import SMOTE
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from xgboost import XGBClassifier

metadata_csv = r"C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/6. dataset_ML_reducido.csv"

data = pd.read_csv(metadata_csv, encoding="utf-8")

X = data.drop(columns=["id_entrada", "nivel_ocupacion"])
y = data["nivel_ocupacion"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

modelos = {

        "Random Forest": Pipeline([
        ("smote", SMOTE(
            sampling_strategy={2: 3000, 3: 1500},
            random_state=42
        )),
        ("rf", RandomForestClassifier(
            n_estimators=500,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            class_weight="balanced",
            random_state=42
        ))
    ]),

    "XGBoost": Pipeline([
        ("smote", SMOTE(
            sampling_strategy={2: 3000, 3: 1500},
            random_state=42
        )),
        ("xgb", XGBClassifier(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            eval_metric="logloss",
            random_state=42
        ))
    ]),

    "Naive Bayes": Pipeline([
        ("scaler", StandardScaler()),
        ("nb", GaussianNB())
    ]),

    "XGBoost": XGBClassifier(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.8,
        colsample_bytree=0.8,
        eval_metric="logloss",
        random_state=42
    )
}

resultados = {}

for nombre, modelo in modelos.items():
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    resultados[nombre] = acc

    print(f"Modelo: {nombre} - Accuracy: {acc:.4f}")

mejor_modelo_nombre = max(resultados, key=resultados.get)
mejor_modelo = modelos[mejor_modelo_nombre]

print("\n=== Mejor modelo encontrado ===")
print(f"Modelo: {mejor_modelo_nombre}")
print(f"Accuracy: {resultados[mejor_modelo_nombre]:.4f}")

modelo_final = mejor_modelo
joblib.dump(modelo_final, "modelo_ML_reducido.pkl")
print("\nModelo exportado como 'mejor_modelo.pkl'")