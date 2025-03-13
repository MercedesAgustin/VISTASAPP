import streamlit as st
import pandas as pd
from datetime import datetime

# Inicializar un DataFrame vacío
expedientes_df = pd.DataFrame(columns=["CUIJ", "Defensoria", "Fecha"])

# Función para guardar los datos en un archivo Excel
def guardar_datos(df):
    today = datetime.now().strftime("%Y-%m-%d")
    archivo = f"expedientes_{today}.xlsx"
    df.to_excel(archivo, index=False, engine='openpyxl')
    st.success(f"Datos guardados en {archivo}")

# Título de la app
st.title("VISTASAPP - Gestión de Expedientes Judiciales")

# Ingresar datos
cui = st.text_input("Ingrese el CUIJ del expediente:")
defensoria = st.selectbox("Seleccione la defensoria:", ["Defensoria 1", "Defensoria 2", "Defensoria 3", "Defensoria 4", "Defensoria 5", "Defensoria 6", "Defensoria 7", "Defensoria 8", "Defensoria 9", "Defensoria 10"])

# Botón para agregar un expediente
if st.button("Agregar Expediente"):
    if cui:
        # Agregar datos al DataFrame
        expedientes_df.loc[len(expedientes_df)] = [cui, defensoria, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        st.write(f"Expediente {cui} derivado a {defensoria}.")
    else:
        st.error("Por favor, ingrese un CUIJ válido.")

# Mostrar tabla de expedientes
st.subheader("Expedientes Derivados")
st.write(expedientes_df)

# Generar archivo Excel
if st.button("Generar Reporte Diario"):
    if len(expedientes_df) > 0:
        guardar_datos(expedientes_df)
    else:
        st.error("No hay expedientes para generar el reporte.")
