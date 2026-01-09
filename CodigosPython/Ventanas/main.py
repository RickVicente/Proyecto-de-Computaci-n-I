import streamlit as st

st.set_page_config(
    page_title="MaDrive · Sistema de Tráfico",
    layout="centered"
)

# ---------- ESTILOS ----------
st.markdown("""
<style>

/* FONDO GENERAL */
body {
    background: radial-gradient(circle at top, #7a0c0c, #3b0000);
    font-family: 'Segoe UI', sans-serif;
}

/* TÍTULO */
.title-container {
    text-align: center;
    margin-bottom: 50px;
}
            
.stApp {
    background: radial-gradient(circle at top, #b11212, #4a0000);
}

.title-container h1 {
    color: white;
    font-size: 42px;
    font-weight: 700;
}

/* TARJETAS */
.card {
    background-color: white;
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.35);
    transition: 0.3s;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.card:hover {
    transform: translateY(-6px);
    box-shadow: 0px 10px 30px rgba(0,0,0,0.45);
}

.card-icon img {
    width: 100%;
    height: 160px;
    object-fit: cover;
    border-radius: 12px;
    margin-bottom: 20px;
}

/* TEXTO TARJETAS */
.card h3 {
    color: #1a1a1a;
    margin-bottom: 10px;
}

.card p {
    color: #444;
    font-size: 14px;
    line-height: 1.5;
}

/* BOTONES */
.stButton {
    display: flex;
    justify-content: center;
}

.stButton>button {
    background-color: #003DA5;
    color: white;
    font-size: 15px;
    border-radius: 12px;
    padding: 10px 28px;
    border: none;
    margin-top: 20px;
}

.stButton>button:hover {
    background-color: #002D7A;
}

</style>
""", unsafe_allow_html=True)

# ---------- CONTENIDO ----------

st.markdown("""
<div class="title-container">
    <h1>MaDrive</h1>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <div>
            <div class="card-icon">
                <img src="https://static01.nyt.com/images/2019/01/22/upshot/22up-traffic1/merlin_144908511_f611b394-7ae4-4e80-a860-9442f5b88656-superJumbo.jpg">
            </div>
            <h3>Predicción por Datos</h3>
            <p>Análisis completo del tráfico a partir de datos (fecha, carretera y vehículos)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Acceder", key="datos"):
        st.switch_page("pages/Prediccion_Normal.py")

with col2:
    st.markdown("""
    <div class="card">
        <div>
            <div class="card-icon">
                <img src="https://www.cea-online.es/images/blog/22/radar-movil.jpg">
            </div>
            <h3>Predicción Reducida</h3>
            <p>Análisis de tráfico a partir de datos más accesibles (fecha y carretera)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Acceder", key="reducida"):
        st.switch_page("pages/Prediccion_Normal_Reducida.py")

with col3:
    st.markdown("""
    <div class="card">
        <div>
            <div class="card-icon">
                <img src="https://cdn-hbdfp.nitrocdn.com/aqwwCdQcyoPaaMoOGgnYhTzgFTaTbLCY/assets/images/optimized/rev-39612a9/www.spottersecurity.com/wp-content/uploads/2024/07/CCTV-traffic-and-transportation-1.png">
            </div>
            <h3>Predicción por Imagen</h3>
            <p>Análisis de imágenes de tráfico con datos correspondientes.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Acceder", key="imagen"):
        st.switch_page("pages/Prediccion_Imagen.py")
