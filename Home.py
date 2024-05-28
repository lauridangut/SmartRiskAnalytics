import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon= "img\Logo_solo_esfera.png"
)

st.sidebar.image("img/Logo_completo.png", width=200)

st.header("SmartRisk Analytics")
st.subheader("Evalúa el riesgo crediticio de manera inteligente. ")

st.write("Nuestra aplicación te ofrece un análisis predictivo detallado para determinar la calificación de clientes de acuerdo al riesgo de incumplimiento de pago al solicitar préstamos. Obtén información clave en tiempo real para tomar decisiones financieras informadas y seguras. ¡Bienvenido a una nueva era en la gestión de riesgos financieros!")