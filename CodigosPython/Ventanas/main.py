import streamlit as st

# python -m streamlit run CodigosPython/Ventanas/main.py

st.set_page_config(
    page_title="MaDrive · Sistema de Tráfico",
    layout="centered"
)

# ---------- ESTILOS ----------
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

# ---------- CONTENIDO ----------
st.markdown("<h1>MaDrive</h1>", unsafe_allow_html=True)

st.write("")
st.write("")

col1, col2 = st.columns(2)

with col1:
    if st.button("Predicción de Tráfico por Datos"):
        st.switch_page("pages/Prediccion_Normal.py")
    
    if st.button("Predicción de Tráfico Reducida"):
        st.switch_page("pages/Prediccion_Normal_Reducida.py")

with col2:
    if st.button("Predicción de Tráfico por Imágen"):
        st.switch_page("pages/Prediccion_Imagen.py")