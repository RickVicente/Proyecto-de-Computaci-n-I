import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("C:/Users/ricky/OneDrive/Universidad/3º Año/1 - Proyecto de Computación I/Proyecto de Computacion/CodigosPython/datasets/3. datasetCompleto.csv")

df["datetime"] = pd.to_datetime(df["fecha_descarga"] + " " + df["hora_descarga"])
df["fecha"] = df["datetime"].dt.date

df_fecha = (
    df.groupby(["carretera", "fecha"])["nivel_ocupacion"]
      .mean()
      .reset_index()
)

# 👇 PROBABLEMENTE carretera ES STRING
subset = df_fecha[df_fecha["carretera"] == "651"]

# Limpieza mínima
subset = subset.dropna(subset=["nivel_ocupacion"])
subset["fecha"] = pd.to_datetime(subset["fecha"])

print("Filas a graficar:", len(subset))  # debug

plt.figure(figsize=(10, 4))
plt.plot(subset["fecha"], subset["nivel_ocupacion"], marker="o")

plt.title("Evolución del nivel de tráfico - 651")
plt.xlabel("Fecha")
plt.ylabel("Nivel de ocupación")
plt.grid(True)
plt.tight_layout()
plt.show()
