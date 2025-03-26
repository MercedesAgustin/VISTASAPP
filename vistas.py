import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
from datetime import datetime
import io


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


# Configurar la API de Gemini
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
else:
    model = None

# Nombre del archivo Excel
EXCEL_FILE = "expedientes.xlsx"

# Función para cargar datos existentes
def cargar_datos():
    try:
        return pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Fecha", "CUIJ", "Defensoria"])

# Función para guardar datos
def guardar_datos(df):
    df.to_excel(EXCEL_FILE, index=False)

# Función para convertir DataFrame a Excel en formato BytesIO
def convertir_a_excel(df):
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return output

# Interfaz de Streamlit
st.set_page_config(page_title="VISTASAPP", layout="wide")
st.title("📂 VISTASAPP")
st.title("Gestión de Expedientes Judiciales")
st.markdown("""
### Bienvenido a VISTASAPP
Registra y gestiona la derivación de expedientes judiciales de forma eficiente. 
""")

# Sección "Cómo funciona"
st.markdown("""
## ℹ️ ¿Cómo funciona?
1️⃣ Ingrese el CUIJ y seleccione la defensoría correspondiente.
2️⃣ Los datos se guardan en un archivo Excel.
3️⃣ Puede ver el reporte diario con la cantidad de expedientes por defensoría.
4️⃣ La IA genera un resumen automático de los expedientes procesados.
""")

# Entrada de datos
cui = st.text_input("Ingrese el CUIJ del expediente")
defensoria = st.selectbox("Seleccione la Defensoría", [f"Defensoría {i+1}" for i in range(10)])

if st.button("Registrar Expediente"):
    if cui:
        df = cargar_datos()
        nuevo_registro = pd.DataFrame({"Fecha": [datetime.today().strftime('%Y-%m-%d')], "CUIJ": [cui], "Defensoria": [defensoria]})
        df = pd.concat([df, nuevo_registro], ignore_index=True)
        guardar_datos(df)
        st.success("Expediente registrado correctamente.")
    else:
        st.warning("Por favor, ingrese un CUIJ válido.")

# Generar reporte diario
def generar_reporte():
    df = cargar_datos()
    if df.empty:
        return "No hay datos registrados aún."
    resumen = df.groupby("Defensoria").size().reset_index(name="Total Expedientes")
    total_expedientes = len(df)
    
    reporte = f"Resumen del día {datetime.today().strftime('%Y-%m-%d')}\n"
    reporte += resumen.to_string(index=False)
    reporte += f"\nTotal de expedientes procesados: {total_expedientes}\n"
    
    if model:
        ia_respuesta = model.generate_content(f"Analiza este reporte y sugiere mejoras:\n{reporte}")
        reporte += f"\n\nSugerencias de IA:\n{ia_respuesta.text}"
    
    return reporte

st.subheader("Reporte Diario")
if st.button("Generar Reporte"):
    reporte = generar_reporte()
    st.text_area("Reporte del día", reporte, height=300)

# Opción para descargar el archivo Excel
st.subheader("Descargar archivo Excel")
df = cargar_datos()
excel_file = convertir_a_excel(df)
st.download_button(
    label="Descargar Expedientes en Excel",
    data=excel_file,
    file_name=EXCEL_FILE,
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# Footer
st.markdown("---")
st.caption("Desarrollado por Merce | VISTASAPP 2025 ©")