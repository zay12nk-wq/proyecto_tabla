import streamlit as st
import pandas as pd
import os
import io

# =====================================================================
# CONFIGURACIÓN DE LA PÁGINA (Estilo Dashboard Premium)
# =====================================================================
st.set_page_config(
    page_title="Sistema Maestro de Retenciones",
    page_icon="💼",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilos CSS Avanzados para una Interfaz Impecable
st.markdown("""
<style>
    /* Ocultar elementos nativos para dar apariencia de Software Privado */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Contenedor de Métrica Principal */
    .kpi-container {
        background-color: #0f172a;
        padding: 24px;
        border-radius: 12px;
        text-align: center;
        border: 1px solid #1e293b;
        margin: 20px 0;
    }
    .kpi-title {
        color: #94a3b8;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    .kpi-value {
        font-size: 38px;
        color: #22c55e;
        font-weight: bold;
        margin-top: 8px;
    }
    
    /* Firma de Autor Fija */
    .firma {
        position: fixed;
        bottom: 15px;
        right: 20px;
        color: #64748b;
        font-size: 13px;
        font-style: italic;
        font-family: sans-serif;
        z-index: 100;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #f8fafc;'>💼 Sistema Contable de Retenciones</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Consola de Cálculo Tributario - Tabla Maestra Oficial</p>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================================
# CARGA SEGURA Y AUTOMATIZADA DE DATOS (Optimización por Caché)
# =====================================================================
@st.cache_data
def cargar_tabla_maestra():
    nombre_archivo = "retenciones_colombia.xlsx"
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    
    if not os.path.exists(ruta):
        st.error(f"❌ Error del Sistema: No se encontró la base de datos '{nombre_archivo}' en la raíz del repositorio.")
        st.stop()
        
    return pd.read_excel(ruta)

df = cargar_tabla_maestra()

# =====================================================================
# ENTRADAS DE USUARIO (Formularios Reactivos)
# =====================================================================
col1, col2 = st.columns(2)

with col1:
    valor = st.number_input(
        "💰 Base Gravable para el Cálculo ($)", 
        min_value=0, 
        value=1000000, 
        step=100000,
        format="%d"
    )

with col2:
    # Agrupar las ubicaciones/ciudades disponibles de forma ordenada
    ubicaciones = sorted(df["Ciudad"].unique())
    seleccion = st.selectbox("🏙️ Seleccione Jurisdicción / Tipo", ubicaciones)

# Filtrar matriz de datos según la selección del usuario
df_filtrado = df[df["Ciudad"] == seleccion].copy()

# =====================================================================
# LÓGICA DE FORMATEO CONTABLE AVANZADO
# =====================================================================
def formatear_tarifa_dinamica(t):
    # Formateo inteligente según el tipo de tarifa en tu documento
    if t < 0.1:
        return f"{t * 1000:.2f} x mil"
    else:
        return f"{t * 100:.1f}%"

# Operaciones Matemáticas
df_filtrado["Retención"] = df_filtrado["Tarifa"] * valor

# Formateo estético para la UI de cara al usuario
df_filtrado["Tarifa Aplicada"] = df_filtrado["Tarifa"].apply(formatear_tarifa_dinamica)
df_filtrado["Valor Retenido ($)"] = df_filtrado["Retención"].apply(lambda x: f"${x:,.0f}")

# Ordenar de mayor a menor retención económica
df_filtrado = df_filtrado.sort_values(by="Retención", ascending=False)

# =====================================================================
# PRESENTACIÓN DE RESULTADOS (Dashboard)
# =====================================================================
total_acumulado = df_filtrado["Retención"].sum()

# Renderizado del KPI de Impacto Total
st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-title">Monto de Retenciones Consolidadas</div>
    <div class="kpi-value">${total_acumulado:,.0f}</div>
</div>
""", unsafe_allow_html=True)

st.subheader("📊 Desglose de Conceptos Aplicables")

# Mostrar la tabla maestra procesada de forma limpia
st.dataframe(
    df_filtrado[["Concepto", "Tarifa Aplicada", "Valor Retenido ($)"]],
    use_container_width=True,
    hide_index=True
)

# =====================================================================
# COMPONENTE DE EXPORTACIÓN (Descargas en Tiempo Real)
# =====================================================================
st.markdown("---")
st.subheader("📥 Generar Reporte Corporativo")

# Limpieza de columnas para el reporte Excel de salida
df_reporte = df_filtrado[["Concepto", "Tarifa Aplicada", "Retención"]].copy()
df_reporte.columns = ["Concepto Tributario", "Tarifa", "Valor Retenido ($)"]

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df_reporte.to_excel(writer, index=False, sheet_name="Resumen de Retenciones")

# Botón de Descarga Seguro
st.download_button(
    label="⬇️ Descargar Reporte en Excel",
    data=buffer.getvalue(),
    file_name=f"reporte_retenciones_{seleccion.lower().replace(' ', '_')}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# =====================================================================
# SELLO DE AUTORÍA
# =====================================================================
st.markdown("""
<div class="firma">
Nohora Portillo
</div>
""", unsafe_allow_html=True)