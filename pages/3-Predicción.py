from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE
import os
import zipfile
import numpy as np
import pandas as pd
import streamlit as st
import random
import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent

# Add the project root directory to the system path
sys.path.append(str(project_root))


st.set_page_config(
    page_title="Home",
    page_icon= "img\Logo_solo_esfera.png"
)

st.sidebar.image("img/Logo_completo.png", width=200)

tipo_organizacion_trabajo_to_english = {
    "Fuerzas armadas": "Armed_forces",
    "Negocios": "Business",
    "Construcción": "Construction",
    "Educación": "Education",
    "Finanzas/Negocios": "Finance/Business",
    "Gobierno": "Government",
    "Industria": "Industry",
    "Medicina": "Medicine",
    "Otro": "Other",
    "Bienes raíces": "Real Estate",
    "Autónomo": "Self-employed",
    "Comercio": "Trade",
    "Transporte": "Transport"
}

tipo_contrato_to_english = {
    "Préstamos en efectivo": "Cash loans",
    "Préstamos renovables": "Revolving loans",
}
estatus_laboral_to_english = {
    "Empleado": "Working",
    "Jubilado": "Pensioner",
    "Desempleado": "Unemployed"
}
nivel_educacion_to_english = {
    "Secundaria / secundaria especial": "Secondary / secondary special",
    "Educación superior": "Higher education",
    "Superior incompleta": "Incomplete higher",
    "Secundaria inferior": "Lower secondary",
    "Titulación académica": "Academic degree"
}
estado_civil_to_english = {
    "Soltero / no casado": "Single / not married",
    "Casado": "Married",
    "Viudo": "Widow",
    "Separado": "Separated"
}
forma_habitar_to_english = {
    "Casa/apartamento": "House / apartment",
    "Apartamento alquilado": "Rented apartment",
    "Con los padres": "With parents",
    "Oficina/Apartamento comercial": "Office/Co-op apartment"
}

ocupacion_to_english = {
    "Obreros": "Laborers",
    "Personal de base": "Core staff",
    "Otro": "Other",
    "Directivos": "Managers",
    "Conductores": "Drivers",
    "Personal de ventas": "Sales staff"
}

tipo_cuenta_bancaria_to_english = {
    "Cuenta de empresa": "business_account",
    "No especifica": "not specified",
    "Cuenta personal": "personal_account"
}

dict_dataset = {
    'auto_propio': False,
    'casa_depto_propio': False,
    'quien_acompañó': False,
    'dia_inicio_proceso': 1,
    'telefono_trabajo': False,
    'telefono_casa': False,
    'telefono_casa2': False,
    'reg_residencia_diferente': False,
    'reg_trabajo_diferente': False,
    'city_residencia_diferente': False,
    'city_trabajo_diferente': False,
    'live_trabajo_diferente': False,
    # Tipo de credito al que postula
    'tipo_contrato_Cash loans': False,
    'tipo_contrato_Revolving loans': False,
    # Estatus laboral
    'estatus_laboral_Pensioner': False,
    'estatus_laboral_Unemployed': False,
    'estatus_laboral_Working': False,
    #  Nivel de educación
    'nivel_educacion_Academic  degree': False,
    'nivel_educacion_Higher education': False,
    'nivel_educacion_Incomplete higher': False,
    'nivel_educacion_Lower secondary': False,
    'nivel_educacion_Secondary / secondary special': False,
    #  Estado civil
    'estado_civil_Married': False,
    'estado_civil_Separated': False,
    'estado_civil_Single / not married': False,
    'estado_civil_Widow': False,
    # Tipo de vivienda donde habita
    'forma_habitar_House / apartment': False,
    'forma_habitar_Office/Co-op apartment': False,
    'forma_habitar_Rented apartment': False,
    'forma_habitar_With parents': False,
    # Tipo de ocupacion del postulante
    'ocupacion_Core staff': False,
    'ocupacion_Drivers': False,
    'ocupacion_Laborers': False,
    'ocupacion_Managers': False,
    'ocupacion_Other': False,
    'ocupacion_Sales staff': False,
    # Tipo de organizacion donde trabaja
    'tipo_organizacion_trabajo_Armed_forces': False,
    'tipo_organizacion_trabajo_Business': False,
    'tipo_organizacion_trabajo_Construction': False,
    'tipo_organizacion_trabajo_Education': False,
    'tipo_organizacion_trabajo_Finance/Business': False,
    'tipo_organizacion_trabajo_Government': False,
    'tipo_organizacion_trabajo_Industry': False,
    'tipo_organizacion_trabajo_Medicine': False,
    'tipo_organizacion_trabajo_Other': False,
    'tipo_organizacion_trabajo_Real Estate': False,
    'tipo_organizacion_trabajo_Self-employed': False,
    'tipo_organizacion_trabajo_Trade': False,
    'tipo_organizacion_trabajo_Transport': False,
    # Que tipo de cuenta bancaria tiene
    'tipo_cuenta_bancaria_business_account': False,
    'tipo_cuenta_bancaria_not specified': False,
    'tipo_cuenta_bancaria_personal_account': False,
    # Inputs numericos
    "monto_credito": 1,
    "edad_cliente": 1,
    "n_familiares": 1,
    "obs_30_circulo_social": 1,
    "solicitudes_al_bureau": 1,
    "n_hijos": 1,
    "ingresos_totales": 1,
    "prestamo_anual": 1,
    "precio_bienes": 1,
    "anios_empleado": 1,
}
# Creamos el dataset con los valores default
dataset = pd.DataFrame([dict_dataset])

# Print del df default
st.dataframe(dataset)

# Página para el formulario
st.subheader("Rellene el formulario completo para obtener la predicción")

# 1
auto_propio = st.radio("¿Cuenta con vehículo propio?", ("Si", "No"))
auto_propio_valor = True if auto_propio == "Si" else False
if not auto_propio:
    st.warning("Por favor, elija una opción.")
dataset["auto_propio"] = auto_propio_valor

# 2
casa_depto_propio = st.radio("¿Cuenta con vivienda propia?", ("Si", "No"))
casa_depto_propio_valor = True if casa_depto_propio == "Si" else False
if not casa_depto_propio:
    st.warning("Por favor, elija una opción.")
dataset["casa_depto_propio"] = casa_depto_propio_valor

# 3
quien_acompano = st.radio("¿Vino acompañado?", ('Si', 'No'))
quien_acompano_valor = True if quien_acompano == "Si" else False
if not quien_acompano:
    st.warning("Por favor, elija una opción.")
dataset["quien_acompañó"] = quien_acompano_valor
# 4
dia_inicio_proceso = st.selectbox("Dia de la semana de inicio del proceso", (
    "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"))
if not dia_inicio_proceso:
    st.warning("Por favor, elija un dia de la semana.")
dias_dict = {"Lunes": "1", "Martes": "2", "Miércoles": "3",
             "Jueves": "4", "Viernes": "5", "Sábado": "6", "Domingo": "7"}
dia_valor = dias_dict.get(dia_inicio_proceso)
dataset["dia_inicio_proceso"] = dia_valor
# 5
telefono_trabajo = st.radio(
    "¿Brindó teléfono de trabajo cuando postuló?", ("Si", "No"))
telefono_trabajo_valor = True if telefono_trabajo == "Si" else False
if not telefono_trabajo:
    st.warning("Por favor, elija una opción.")
dataset["telefono_trabajo"] = telefono_trabajo_valor
# 6
telefono_casa = st.radio(
    "¿Brindó teléfono particular cuando postuló?", ("Si", "No"))
telefono_casa_valor = True if telefono_casa == "Si" else False
if not telefono_casa:
    st.warning("Por favor, elija una opción.")
dataset["telefono_casa"] = telefono_casa_valor
# 7
telefono_casa2 = st.radio(
    "¿Brindó otro teléfono cuando postuló?", ("Si", "No"))
telefono_casa2_valor = True if telefono_casa2 == "Si" else False
if not telefono_casa2:
    st.warning("Por favor, elija una opción.")
    dataset["telefono_casa2"] = telefono_casa2_valor
# 8
reg_residencia_diferente = st.radio(
    "La región de residencia entregada, ¿Es distinta de donde vive?", ("Si", "No"))
reg_residencia_diferente_valor = True if reg_residencia_diferente == "Si" else False
if not reg_residencia_diferente:
    st.warning("Por favor, elija una opción.")
dataset["reg_residencia_diferente"] = reg_residencia_diferente_valor

# 9
reg_trabajo_diferente = st.radio(
    "La región de residencia del trabajo entregada, ¿Es distinta de donde vive?", ("Si", "No"))
reg_trabajo_diferente_valor = True if reg_trabajo_diferente == "Si" else False
if not reg_trabajo_diferente:
    st.warning("Por favor, elija una opción.")
dataset["reg_trabajo_diferente"] = reg_trabajo_diferente_valor

# 10
city_residencia_diferente = st.radio(
    "¿La ciudad de residencia entregada es distinta de donde vive?", ("Si", "No"))
city_residencia_diferente_valor = True if city_residencia_diferente == "Si" else False
if not city_residencia_diferente:
    st.warning("Por favor, elija una opción.")
dataset["city_residencia_diferente"] = city_residencia_diferente_valor

# 11
city_trabajo_diferente = st.radio(
    "¿La ciudad de trabajo es distinta donde vive?", ("Si", "No"))
city_trabajo_diferente_valor = True if city_trabajo_diferente == "Si" else False
if not city_trabajo_diferente:
    st.warning("Por favor, elija una opción.")
dataset["city_trabajo_diferente"] = city_trabajo_diferente_valor

# 12
live_trabajo_diferente = st.radio(
    "¿La dirección de trabajo es distinta a donde vive?", ("Si", "No"))
live_trabajo_diferente_valor = True if live_trabajo_diferente == "Si" else False
if not live_trabajo_diferente:
    st.warning("Por favor, elija una opción.")
dataset["live_trabajo_diferente"] = live_trabajo_diferente_valor

# 13 y 14
# Tiene: Cash loans y Revolving loans
tipo_contrato = st.selectbox(
    "¿Qué tipo de prestamo solicita?", ("Préstamos en efectivo", "Préstamos renovables"))
if not tipo_contrato:
    st.warning("Por favor, elija una opción.")

tipo_contrato_true = tipo_contrato_to_english[tipo_contrato]
clave = f'tipo_contrato_{tipo_contrato_true}'
dataset[clave] = True
# 15, 16 y 17
# Tiene: Pensioner, Unemployed y Working
estatus_laboral = st.selectbox(
    "¿Cuál es su situación laboral actual?", ('Empleado', 'Jubilado', 'Desempleado'))
if not estatus_laboral:
    st.warning("Por favor, elija una opción.")
estatus_laboral_true = estatus_laboral_to_english[estatus_laboral]
clave = f'estatus_laboral_{estatus_laboral_true}'
dataset[clave] = True

# 18, 19, 20, 21 y 22
# Tiene: Academic degree, Higher education, Incomplete higher, Lower secondary, Secondary/ secondary special
nivel_educacion = st.selectbox("¿Cuál es su nivel de educación?", ('Secundaria / secundaria especial',
                               'Educación superior', 'Superior incompleta', 'Secundaria inferior', 'Titulación académica'))
if not nivel_educacion:
    st.warning("Por favor, elija una opción.")
nivel_educacion_true = nivel_educacion_to_english[nivel_educacion]
clave = f'nivel_educacion_{nivel_educacion_true}'
dataset[clave] = True

# 23, 24, 25 y 26
estado_civil = st.selectbox("¿Cuál es su estado civil?",
                            ('Soltero / no casado', 'Casado', 'Viudo', 'Separado'))
if not estado_civil:
    st.warning("Por favor, elija una opción.")
estado_civil_true = estado_civil_to_english[estado_civil]
clave = f'estado_civil_{estado_civil_true}'
dataset[clave] = True

# 27, 28, 29 y 30
forma_habitar = st.selectbox("¿En qué tipo de residencia habita?", ("Casa/apartamento",
                             "Apartamento alquilado", "Con los padres", "Oficina/Apartamento comercial"))
if not forma_habitar:
    st.warning("Por favor, elija una opción.")
forma_habitar_true = forma_habitar_to_english[forma_habitar]
clave = f'forma_habitar_{forma_habitar_true}'
dataset[clave] = True

# 31, 32, 33, 34, 35 y 36
ocupacion = st.selectbox("¿Qué tipo de trabajo tiene?", ('Obreros', 'Personal de base',
                         'Otro', 'Directivos', 'Conductores', 'Personal de ventas'))
if not ocupacion:
    st.warning("Por favor, elija una opción.")
ocupacion_true = ocupacion_to_english[ocupacion]
clave = f'ocupacion_{ocupacion_true}'
dataset[clave] = True

# 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48 y 49
tipo_organizacion_trabajo = st.selectbox("¿En qué área trabaja?", ('Educación', 'Negocios', 'Otro', 'Construcción', 'Medicina',
                                         'Autónomo', 'Transporte', 'Bienes raíces', 'Comercio', 'Industria', 'Fuerzas Armadas', 'Finanzas/Negocios', 'Gobierno'))
if not tipo_organizacion_trabajo:
    st.warning("Por favor, elija una opción.")
tipo_organizacion_trabajo_true = tipo_organizacion_trabajo_to_english[
    tipo_organizacion_trabajo]
clave = f'tipo_organizacion_trabajo_{tipo_organizacion_trabajo_true}'
dataset[clave] = True

# 50, 51 y 52
tipo_cuenta = st.selectbox("¿Qué tipo de cuenta bancaria tiene el solicitante?",
                           ("Cuenta de empresa", "No especifica", "Cuenta personal"))
if not tipo_cuenta:
    st.warning("Por favor, elija una opción.")
tipo_cuenta_bancaria_true = tipo_cuenta_bancaria_to_english[tipo_cuenta]
clave = f'tipo_cuenta_bancaria_{tipo_cuenta_bancaria_true}'
dataset[clave] = True

# 53
monto_credito = st.number_input("¿Cuál es el monto del crédito que solicita?")
dataset["monto_credito"] = monto_credito
if not monto_credito:
    st.warning("Por favor, un monto valido.")

# 54
edad_cliente = st.number_input("¿Cuál es su edad?")
dataset["edad_cliente"] = edad_cliente
if not monto_credito:
    st.warning("Por favor, indique su edad.")

# 55
n_familiares = st.number_input("¿Cuántas personas hay en su círculo familiar?")
dataset["n_familiares"] = n_familiares
if not monto_credito:
    st.warning(
        "Por favor, indique la cantidad de personas en su circulo familiar.")

# 56
obs_30_circulo_social = st.number_input(
    "¿Cuenta con personas dentro de su círculo social con deudas vigentes? Si cuenta, escriba la cantidad. Caso contrario, escriba 0.")
dataset["obs_30_circulo_social"] = obs_30_circulo_social
if not obs_30_circulo_social:
    st.warning(
        "Por favor, indique la cantidad de personas en su circulo social con deudas vigentes.")

# 57
solicitudes_al_bureau = st.number_input(
    "Cantidad de solicitudes de crédito en el último año")
dataset["solicitudes_al_bureau"] = solicitudes_al_bureau
if not obs_30_circulo_social:
    st.warning(
        "Por favor, indique la cantidad de solicitudes de crédito en el último año.")

# 58
n_hijos = st.number_input("¿Cuántos hijos tiene?")
dataset["n_hijos"] = n_hijos
if not obs_30_circulo_social:
    st.warning("Por favor, indique la cantidad de hijos que tiene.")

# 59
ingresos_totales = st.number_input("Monto del ingreso total del cliente")
dataset["ingresos_totales"] = ingresos_totales
if not obs_30_circulo_social:
    st.warning("Por favor, indique el monto del ingreso total del cliente.")

# 60
prestamo_anual = st.number_input("Anualidad del crédito")
dataset["prestamo_anual"] = prestamo_anual
if not prestamo_anual:
    st.warning("Por favor, indique la anualidad del crédito.")

# 61
precio_bienes = st.number_input(
    "Precio de los bienes para los cuales se otorga el crédito")
dataset["precio_bienes"] = precio_bienes
if not precio_bienes:
    st.warning(
        "Por favor, indique el precio de los bienes para los cuales se otorga el crédito.")

# 62
anios_empleado = st.number_input("Antigüedad en el empleo actual")
dataset["anios_empleado"] = anios_empleado
if not anios_empleado:
    st.warning("Por favor, indique la antigüedad en el empleo actual.")
    if auto_propio and casa_depto_propio and quien_acompano and dia_inicio_proceso and telefono_trabajo and telefono_casa and telefono_casa2 and reg_residencia_diferente and reg_trabajo_diferente and city_residencia_diferente and city_trabajo_diferente and live_trabajo_diferente and tipo_contrato and estatus_laboral and nivel_educacion and estado_civil and forma_habitar and ocupacion and tipo_organizacion_trabajo and tipo_cuenta and monto_credito and edad_cliente and n_familiares and obs_30_circulo_social and solicitudes_al_bureau and n_hijos and ingresos_totales and prestamo_anual and precio_bienes and anios_empleado:
        st.success("¡Formulario enviado correctamente!")
else:
    st.warning("Por favor, completa todos los campos obligatorios.")

# Salida del dataset luego del formulario
st.dataframe(dataset)

# Instanciamos el modelo

# Opcion 1
df = pd.read_csv(
    "C:/Users/Acer/Documents/Repositorios_Github/SmartRisk_NC/data/csv/df_concat_a.csv")
# Cargamos el datasetpip 2
# df = pd.read_csv("../../data/csv/df_concat_a.csv")
# df = df.drop(columns="Unnamed: 0")

# Oversampling
smote = SMOTE(random_state=16)

# Definimos target y predictoras
X = df.drop(columns=["sk_id_curr", "target"])
y = df["target"]

# Balanceamos las clases
X_balanced, y_balanced = smote.fit_resample(X, y)

# Hacemos el train test split
X_train, X_test, y_train, y_test = train_test_split(
    X_balanced, y_balanced, test_size=0.20, random_state=16)

# Instanciamos la regresion logística y la ajustamos
reg = LogisticRegression(max_iter=1000).fit(X_train, y_train)

# Preprocesamiento del nuevo registro antes de predecir
sc = StandardScaler().fit(X_train)

# Transformamos la nueva fila utilizando los parámetros de escalado
new_row_scaled = sc.transform(dataset)

# Hacemos la predicción
y_pred_new = reg.predict(new_row_scaled)

# Printeamos el resultado previo
st.write(y_pred_new)

# Conectamos la predicción al botón


def main():
    if st.button("Predecir"):
        prediccion = y_pred_new

        if prediccion == 0:
            st.write("Cliente no riesgoso, aprobar solicitud.")
        else:
            st.write("Cliente RIESGOSO !!, no aprobar solicitud.")

        st.write(f"Predicción: {prediccion}")


if __name__ == "__main__":
    main()