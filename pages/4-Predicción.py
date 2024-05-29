import streamlit as st
import pandas as pd
import numpy as np
import pickle


# Configurar la página
st.set_page_config(
    page_title="Home",
    page_icon= "img\Logo_solo_esfera.png"
)

st.sidebar.image("img/Logo_completo.png", width=200)

# Cargar el modelo de regresión logística
model_path = 'model\modelo_logistico.pkl'  
with open(model_path, 'rb') as model_file:
    model = pickle.load(model_file)

# Diccionarios de traducción
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

# Título de la aplicación
st.title("Formulario de Predicción de Riesgo")

# Crear el formulario con los campos necesarios
def crear_formulario():
    #Variables booleanas
    auto_propio = st.radio("¿Cuenta con vehículo propio?", ("Si", "No"))
    auto_propio_valor = True if auto_propio == "Si" else False

    casa_depto_propio = st.radio("¿Cuenta con vivienda propia?", ("Si", "No"))
    casa_depto_propio_valor = True if casa_depto_propio == "Si" else False

    quien_acompano = st.radio("¿Vino acompañado?", ('Si', 'No'))
    quien_acompano_valor = True if quien_acompano == "Si" else False

    dia_inicio_proceso = st.selectbox("Dia de la semana de inicio del proceso", (
    "Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"))
    dias_dict = {"Lunes": "1", "Martes": "2", "Miércoles": "3",
             "Jueves": "4", "Viernes": "5", "Sábado": "6", "Domingo": "7"}
    dia_valor = dias_dict.get(dia_inicio_proceso)

    telefono_trabajo = st.radio(
    "¿Brindó teléfono de trabajo cuando postuló?", ("Si", "No"))
    telefono_trabajo_valor = True if telefono_trabajo == "Si" else False

    telefono_casa = st.radio(
    "¿Brindó teléfono particular cuando postuló?", ("Si", "No"))
    telefono_casa_valor = True if telefono_casa == "Si" else False

    telefono_casa2 = st.radio(
    "¿Brindó otro teléfono cuando postuló?", ("Si", "No"))
    telefono_casa2_valor = True if telefono_casa2 == "Si" else False

    reg_residencia_diferente = st.radio(
    "La región de residencia entregada, ¿es distinta de donde vive?", ("Si", "No"))
    reg_residencia_diferente_valor = True if reg_residencia_diferente == "Si" else False

    reg_trabajo_diferente = st.radio(
    "La región de residencia del trabajo entregada, ¿es distinta de donde vive?", ("Si", "No"))
    reg_trabajo_diferente_valor = True if reg_trabajo_diferente == "Si" else False

    city_residencia_diferente = st.radio(
    "La ciudad de residencia entregada, ¿es distinta de donde vive?", ("Si", "No"))
    city_residencia_diferente_valor = True if city_residencia_diferente == "Si" else False

    city_trabajo_diferente = st.radio(
    "La ciudad de trabajo, ¿es distinta de donde vive?", ("Si", "No"))
    city_trabajo_diferente_valor = True if city_trabajo_diferente == "Si" else False

    live_trabajo_diferente = st.radio(
    "La dirección de trabajo, ¿es distinta de donde vive?", ("Si", "No"))
    live_trabajo_diferente_valor = True if live_trabajo_diferente == "Si" else False

    #Variables dummy
    tipo_contrato = st.selectbox("Tipo de préstamo", ("Préstamos en efectivo", "Préstamos renovables"))
    estatus_laboral = st.selectbox("Situación laboral actual", ('Empleado', 'Jubilado', 'Desempleado'))
    nivel_educacion = st.selectbox("Nivel de educación", ('Secundaria / secundaria especial', 'Educación superior', 'Superior incompleta', 'Secundaria inferior', 'Titulación académica'))
    estado_civil = st.selectbox("Estado civil", ('Soltero / no casado', 'Casado', 'Viudo', 'Separado'))
    forma_habitar = st.selectbox("Tipo de residencia", ("Casa/apartamento", "Apartamento alquilado", "Con los padres", "Oficina/Apartamento comercial"))
    ocupacion = st.selectbox("Tipo de trabajo", ('Obreros', 'Personal de base', 'Otro', 'Directivos', 'Conductores', 'Personal de ventas'))
    tipo_organizacion_trabajo = st.selectbox("Área de trabajo", ('Educación', 'Negocios', 'Otro', 'Construcción', 'Medicina', 'Autónomo', 'Transporte', 'Bienes raíces', 'Comercio', 'Industria', 'Fuerzas Armadas', 'Finanzas/Negocios', 'Gobierno'))
    tipo_cuenta = st.selectbox("¿Qué tipo de cuenta bancaria tiene el solicitante?", ("Cuenta de empresa", "No especifica", "Cuenta personal"))

    #Variables numéricas
    monto_credito = st.number_input("Monto del crédito solicitado")
    edad_cliente = st.number_input("Edad")
    n_familiares = st.number_input("¿Cuántas personas hay en su círculo familiar?")
    obs_30_circulo_social = st.number_input("¿Cuenta con personas dentro de su círculo social con deudas vigentes? Si cuenta, escriba la cantidad. En caso contrario, escriba 0.")
    solicitudes_al_bureau = st.number_input("Cantidad de solicitudes de crédito en el último año")
    n_hijos = st.number_input("Cantidad de hijos")
    ingresos_totales = st.number_input("Monto del ingreso total del cliente")
    prestamo_anual = st.number_input("Anualidad del crédito")
    precio_bienes = st.number_input("Precio de los bienes para los cuales se otorga el crédito")
    anios_empleado = st.number_input("Antigüedad en el empleo actual")


    # Crear un diccionario con los datos
    datos = {
        'auto_propio': auto_propio_valor,
        'casa_depto_propio': casa_depto_propio_valor,
        'quien_acompano': quien_acompano_valor,
        'dia_inicio_proceso': dia_valor,
        'telefono_trabajo': telefono_trabajo_valor,
        'telefono_casa': telefono_casa_valor,
        'telefono_casa2': telefono_casa2_valor,
        'reg_residencia_diferente': reg_residencia_diferente_valor,
        'reg_trabajo_diferente': reg_trabajo_diferente_valor,
        'city_residencia_diferente': city_residencia_diferente_valor,
        'city_trabajo_diferente': city_trabajo_diferente_valor,
        'live_trabajo_diferente': live_trabajo_diferente_valor,
        'tipo_contrato': tipo_contrato_to_english[tipo_contrato],
        'estatus_laboral': estatus_laboral_to_english[estatus_laboral],
        'nivel_educacion': nivel_educacion_to_english[nivel_educacion],
        'estado_civil': estado_civil_to_english[estado_civil],
        'forma_habitar': forma_habitar_to_english[forma_habitar],
        'ocupacion': ocupacion_to_english[ocupacion],
        'tipo_organizacion_trabajo': tipo_organizacion_trabajo_to_english[tipo_organizacion_trabajo],
        'tipo_cuenta': tipo_cuenta_bancaria_to_english[tipo_cuenta],
        'monto_credito': monto_credito,
        'edad_cliente': edad_cliente,
        'n_familiares': n_familiares,
        'obs_30_circulo_social': obs_30_circulo_social,
        'solicitudes_al_bureau': solicitudes_al_bureau,
        'n_hijos': n_hijos,
        'ingresos_totales': ingresos_totales,
        'prestamo_anual': prestamo_anual,
        'precio_bienes': precio_bienes,
        'anios_empleado': anios_empleado
    }
    
    return datos

datos = crear_formulario()

# Crear DataFrame
dataset = pd.DataFrame([datos])

# Validar el formulario
if not all(dataset.iloc[0].notnull()):
    st.warning("Por favor, completa todos los campos obligatorios.")
else:
    # Hacer la predicción
    prediction = model.predict(dataset)
    st.success("¡Formulario enviado correctamente!")
    st.write("Predicción:", prediction)