import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon= "img\Logo_solo_esfera.png"
)

st.sidebar.image("img/Logo_completo.png", width=200)

st.header("Análisis descriptivo del perfil de clientes que postulan a créditos")

st.write("<iframe title='Dashboard c17-80m-final' width='1000' height='600' src='https://app.powerbi.com/view?r=eyJrIjoiNGVhMzQxMTMtMGM0ZC00M2JhLTk5NDQtM2Y1ZmE4MTM1YjFmIiwidCI6ImI1ZDc4OTI3LTI1ZDAtNDRhOS04MzcwLWQ4NmU1N2M3YmE5NiIsImMiOjR9' frameborder='0' allowFullScreen='true' style='display:block;margin:auto;'></iframe>", unsafe_allow_html=True)