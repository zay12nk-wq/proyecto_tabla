import streamlit as st
import pandas as pd
import os
import io

# =====================================================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================================================
st.set_page_config(
    page_title="Facturador y Liquidador de Retenciones",
    page_icon="🧾",
    layout="centered"
)

# Estilos CSS para simular una factura contable real
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .factura-box {
        background-color: #1e293b;
        padding: 25px;
        border-radius: 10px;
        border: 2px solid #334155;
        font-family: 'Courier New', Courier, monospace;
        margin-top: 20px;
    }
    .factura-linea {
        display: flex;
        justify-content: space-between;
        margin-bottom: 8px;
        font-size: 16px;
        color: #f8fafc;
    }
    .factura-total {
        display: flex;
        justify-content: space-between;
        margin-top: 15px;
        padding-top: 15px;
        border-top: 2px dashed #64748b;
        font-size: 20px;
        font-weight: bold;
        color: #22c55e;
    }
    .firma {
        position: fixed;
        bottom: 15px;
        right: 20px;
        color: #64748b;
        font-size: 13px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #f8fafc;'>🧾 Liquidador Contable de Facturas</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8;'>Cálculo dinámico de Impuestos y Retenciones en Colombia</p>", unsafe_allow_html=True)
st.markdown("---")

# =====================================================================
# CARGA DE DATOS
# =====================================================================
@st.cache_data
def cargar_tabla_maestra():
    nombre_archivo = "retenciones_colombia.xlsx"
    ruta = os.path.join(os.getcwd(), nombre_archivo)
    if not os.path.exists(ruta):
        st.error(f"❌ No se encontró la base de datos '{nombre_archivo}'.")
        st.stop()
    return pd.read_excel(ruta)

df = cargar_tabla_maestra()

# =====================================================================
# ENTRADAS PRINCIPALES DEL LIQUIDADOR
# =====================================================================
col1, col2 = st.columns(2)

with col1:
    subtotal = st.number_input("💰 Subtotal ($)", min_value=0.0, value=1000000.0, step=10000.0, format="%.0f")
    
    # Lista desplegable con los porcentajes de descuento que pediste
    opciones_descuento = {
        "Sin Descuento (0%)": 0.0,
        "Descuento del 1%": 0.01,
        "Descuento del 1.5%": 0.015,
        "Descuento del 2%": 0.02,
        "Descuento del 3%": 0.03,
        "Descuento del 4%": 0.04,
        "Descuento del 10%": 0.10,
        "Descuento del 20%": 0.20
    }
    descuento_seleccionado = st.selectbox("🏷️ Seleccione Porcentaje de Descuento", list(opciones_descuento.keys()))
    porcentaje_desc = opciones_descuento[descuento_seleccionado]

with col2:
    # Filtro de Ciudades para ICA
    ciudades_disponibles = sorted(df[df["Ciudad"] != "Retefuente Nacional"]["Ciudad"].unique())
    ciudad_sel = st.selectbox("🏙️ Jurisdicción para ICA", ciudades_disponibles)
    
    # Filtro de Conceptos para Retefuente Nacional
    conceptos_retefuente = df[df["Ciudad"] == "Retefuente Nacional"]["Concepto"].unique()
    retefuente_sel = st.selectbox("🧾 Concepto de Retefuente", conceptos_retefuente)

# =====================================================================
# PROCESAMIENTO MATEMÁTICO CONTABLE
# =====================================================================
# 1. Cálculo del valor del descuento en pesos basado en el porcentaje elegido
descuentos_pesos = subtotal * porcentaje_desc

# 2. Base Gravable
base_gravable = max(0.0, subtotal - descuentos_pesos)

# 3. IVA (19%)
iva_calculado = base_gravable * 0.19

# 4. Cálculo de Retefuente Nacional seleccionada
tarifa_retefuente = df[df["Concepto"] == retefuente_sel]["Tarifa"].values[0]
retefuente_calculada = base_gravable * tarifa_retefuente

# 5. Cálculo de Retención ICA
df_ica_ciudad = df[df["Ciudad"] == ciudad_sel]
concepto_ica = df_ica_ciudad["Concepto"].values[0] 
tarifa_ica = df_ica_ciudad["Tarifa"].values[0]
reteica_calculado = base_gravable * tarifa_ica

# 6. Cálculo de Retención IVA (Equivale al 15% del IVA facturado)
reteiva_calculado = iva_calculado * 0.15

# 7. Neto Total a Pagar
total_neto = base_gravable + iva_calculado - retefuente_calculada - reteica_calculado - reteiva_calculado

# =====================================================================
# ESTRUCTURA VISUAL EN FORMATO FACTURA
# =====================================================================
st.subheader("📊 Estructura de Liquidación Generada")

# Mostramos el porcentaje real al lado del texto para que sepa qué se aplicó
texto_descuento = f"(-) Descuentos ({porcentaje_desc*100}%):" if porcentaje_desc > 0 else "(-) Descuentos:"

st.markdown(f"""
<div class="factura-box">
    <div class="factura-linea"><span>Subtotal:</span> <span>${subtotal:,.0f}</span></div>
    <div class="factura-linea" style="color: #ef4444;"><span>{texto_descuento}</span> <span>-${descuentos_pesos:,.0f}</span></div>
    <div class="factura-linea" style="border-top: 1px solid #475569; padding-top: 5px; font-weight: bold;"><span>Base gravable:</span> <span>${base_gravable:,.0f}</span></div>
    <div class="factura-linea" style="color: #38bdf8;"><span>(+) IVA (19%):</span> <span>+${iva_calculado:,.0f}</span></div>
    <div class="factura-linea" style="color: #f97316;"><span>(-) Retención en la Fuente ({retefuente_sel.split()[-1]}):</span> <span>-${retefuente_calculada:,.0f}</span></div>
    <div class="factura-linea" style="color: #fbbf24;"><span>(-) Retención ICA ({ciudad_sel}):</span> <span>-${reteica_calculado:,.0f}</span></div>
    <div class="factura-linea" style="color: #f43f5e;"><span>(-) Retención IVA (15% del IVA):</span> <span>-${reteiva_calculado:,.0f}</span></div>
    <div class="factura-total"><span>(=) TOTAL NETO A PAGAR:</span> <span>${total_neto:,.0f}</span></div>
</div>
""", unsafe_allow_html=True)

# Información informativa sobre las tarifas aplicadas detrás de escena
with st.expander("🔍 Ver detalles de tarifas aplicadas"):
    st.write(f"**Tarifa ReteFuente:** {tarifa_retefuente * 100}%")
    st.write(f"**Tarifa ICA aplicada:** {concepto_ica} ({tarifa_ica if tarifa_ica >= 0.1 else tarifa_ica * 1000} x mil)")
    st.write(f"**Tarifa ReteIVA:** 15% sobre el valor del IVA")

# =====================================================================
# EXPORTACIÓN A EXCEL DEL REPORTE
# =====================================================================
st.markdown("---")
df_reporte = pd.DataFrame({
    "Concepto": ["Subtotal", f"Descuentos ({porcentaje_desc*100}%)", "Base Gravable", "IVA (19%)", f"Retención Fuente ({retefuente_sel})", f"Retención ICA ({ciudad_sel})", "Retención IVA (15%)", "Total Neto a Pagar"],
    "Valor ($)": [subtotal, -descuentos_pesos, base_gravable, iva_calculado, -retefuente_calculada, -reteica_calculado, -reteiva_calculado, total_neto]
})

buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
    df_reporte.to_excel(writer, index=False, sheet_name="Liquidacion_Factura")

st.download_button(
    label="📥 Descargar esta Factura en Excel",
    data=buffer.getvalue(),
    file_name="liquidacion_factura.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

st.markdown("""
<div class="firma">
Nohora Portillo
</div>
""", unsafe_allow_html=True)