import joblib
import pandas as pd
from pathlib import Path

base_folder = Path("C:/Users/ricky/OneDrive/Escritorio/Camaras_Madrid")
modelo = joblib.load(base_folder / "modelo_trafico.pkl")

def predecir_nivel_trafico(camara, coches, camiones, motos, buses, carrretera, fecha, hora):
    X = pd.DataFrame([{
        "camara": camara,
        "coches": coches,
        "camiones": camiones,
        "motos": motos,
        "buses": buses,
        "carretera": carrretera,
        "fecha": fecha,
        "hora": hora
    }])
    nivel = modelo.predict(X)[0]
    return int(nivel)

if __name__ == "__main__":
    # Ejemplo de uso:
    nivel = predecir_nivel_trafico("MIRAFLORES", 5, 1, 0, 2, "A-1", "2024-06-10", "14:30:00")
    print(f"Predicción de nivel de tráfico: {nivel}")