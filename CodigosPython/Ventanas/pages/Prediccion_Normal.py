import streamlit as st
from datetime import datetime, date, time
import joblib
import numpy as np

# python -m streamlit run CodigosPython/Ventanas/ventana1.py

# streamlit run ventana1.py
modelo = joblib.load("ModelosIA/modelo_ML.pkl")

st.set_page_config(page_title="Registro de Tráfico", layout="centered")

st.markdown("""
<style>
/* Fondo y tipografía */
body {
    background-color: #f5f5f5;
    font-family: 'Arial', sans-serif;
}

/* Título principal */
h1 {
    color: #b22222; /* rojo Madrid */
    font-weight: bold;
    text-align: center;
}

/* Botones */
.stButton>button {
    background-color: #b22222;
    color: white;
    font-size: 16px;
    border-radius: 8px;
    padding: 10px 20px;
    border: none;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #8b0000;
    cursor: pointer;
}

/* Columnas */
.stColumns>div {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.1);
}

/* Resumen de predicción */
.stMarkdown h3 {
    color: #b22222;
    margin-top: 15px;
}

.stMarkdown p {
    font-size: 15px;
}

</style>
""", unsafe_allow_html=True)

# Título
st.title("Análisis de Tráfico Madrid")

col1, col2, col3 = st.columns([1, 1, 1.3])

with col1:
    camara = st.selectbox(
        "Número de cámara",
        options=[
            598, 634, 651, 660, 668, 673, 677, 696, 705, 726,
            731, 771, 773, 791, 798, 799, 826, 864, 866, 868,
            872, 873, 877, 897, 926, 967, 971, 972, 1004, 1010,
            1097, 1125, 1158, 1160, 1161, 1162, 1676, 1690, 169372, 169708,
            169709, 169741, 174942, 174943, 174945, 175471
        ]
    )

    num_coches = st.number_input(
        "Número de coches",
        min_value=0,
        step=1
    )

    num_camiones = st.number_input(
        "Número de camiones",
        min_value=0,
        step=1
    )

    num_buses = st.number_input(
        "Número de buses",
        min_value=0,
        step=1
    )

    num_motos = st.number_input(
        "Número de motos",
        min_value=0,
        step=1
    )

with col2:
    # Fecha
    fecha = st.date_input(
        "Fecha",
        format="DD/MM/YYYY"
    )

    # Hora
    hora = st.time_input(
        "Hora",
        value=time(12, 0, 0)
    )

    # Número de carretera
    num_carretera = st.selectbox(
        "Número de carretera", [
            40, 2, 5, 6, 4, 42, 614, 1, 3, 50
        ]
    )

    # Tipo de carretera
    tipo_carretera = st.selectbox(
        "Tipo de carretera",
        options=["A", "M", "N"]
    )

def franja_horaria(hora):
    mañana = int(6 <= hora <= 11)
    tarde = int(12 <= hora <= 17)
    noche = int(18 <= hora <= 23)
    return mañana, tarde, noche

niveles_trafico = {
    0: "No tráfico",
    1: "Poco tráfico",
    2: "Tráfico moderado",
    3: "Tráfico alto"
}

with col3:
    # Botón de envío
    if st.button("Predecir Nivel de Ocupación"):
        fecha_hora = datetime.combine(fecha, hora)

        anio = fecha.year
        mes = fecha.month
        dia = fecha.day

        hora_h = hora.hour
        minuto = hora.minute
        segundo = hora.second
        
        total_veh = num_coches+num_camiones+num_buses+num_motos

        carretera_a = int(tipo_carretera == "A")
        carretera_m = int(tipo_carretera == "M")
        carretera_n = int(tipo_carretera == "N")

        mañana, tarde, noche = franja_horaria(hora_h)
        
        # Crear array de predicción
        X = np.array([[
            camara,
            num_coches,
            num_camiones,
            num_buses,
            num_motos,
            total_veh,
            anio, 
            mes,
            dia,
            hora_h,
            minuto,
            num_carretera,
            carretera_a,
            carretera_m,
            carretera_n,
            mañana,
            noche,
            tarde
        ]])
        
        # Predicción
        prediccion = modelo.predict(X)
        nivel = niveles_trafico.get(prediccion[0], "Desconocido")
        
        st.success("Datos guardados correctamente")
        st.write("### Resumen")
        st.write(f"Cámara Seleccionada: {camara}")
        st.write(f"Número de Coches: {num_coches}, Camiones: {num_camiones}, Buses: {num_buses}, Motos: {num_motos} - Total: {total_veh}")
        st.write(f"Fecha y hora: {fecha_hora.strftime('%d/%m/%Y %H:%M:%S')}")
        st.write(f"Carretera: {tipo_carretera}-{num_carretera}")

        colores = {
            "No tráfico": "#2E8B57",
            "Poco tráfico": "#FFD700",
            "Tráfico moderado": "#FFA500", 
            "Tráfico alto": "#B22222"
        }
        color = colores.get(nivel, "#000000")

        # Mostrar la predicción en grande
        st.markdown(f"""
            <h1 style="text-align:center; color:{color}; font-size:48px; margin-top:20px;">
            {nivel}
            </h1>
        """, unsafe_allow_html=True)
