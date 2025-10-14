import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import joblib
from pathlib import Path

base_folder = Path("C:/Users/ricky/OneDrive/Escritorio/Camaras_Madrid")

# 1️⃣ Cargar dataset con tus etiquetas manuales
df = pd.read_csv(base_folder / "dataset.csv")

# Asegúrate de haber añadido una columna llamada 'nivel_trafico'
# con tus etiquetas (0 = nulo, 1 = bajo, 2 = medio, 3 = alto)

# 2️⃣ Preparar los datos
X = df[["camara", "coches", "camiones", "motos", "buses", "carretera", "fecha", "hora"]]
y = df["nivel_trafico"]

preprocessor = ColumnTransformer([
    ("camara", OneHotEncoder(), ["camara"])
], remainder="passthrough")

# 3️⃣ Crear modelo (red neuronal simple)
model = MLPClassifier(hidden_layer_sizes=(10,), max_iter=500, random_state=42)

pipeline = Pipeline([
    ("preprocess", preprocessor),
    ("model", model)
])

# 4️⃣ Entrenar y evaluar
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
pipeline.fit(X_train, y_train)
score = pipeline.score(X_test, y_test)

print(f"✅ Precisión del modelo: {score:.2f}")

# 5️⃣ Guardar modelo
joblib.dump(pipeline, base_folder / "modelo_trafico.pkl")
print("📦 Modelo guardado en:", base_folder / "modelo_trafico.pkl")