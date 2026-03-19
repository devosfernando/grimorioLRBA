import streamlit as st
import os
import io
import contextlib
import scripts.artifact as artifact
import scripts.excel as excel
import scripts.generate as generate
import scripts.request_multi as request_multi
import scripts.clone_glo as clone_glo
import scripts.pom as pom

# --- CLASE PARA CAPTURA EN TIEMPO REAL ---
class StreamlitLogWriter(io.StringIO):
    def __init__(self, placeholder):
        super().__init__()
        self.placeholder = placeholder
        self.output_text = ""

    def write(self, s):
        # Limpiamos un poco el texto para que no se vea la ruta completa de Windows
        s = s.replace(os.getcwd(), "...")
        self.output_text += s
        self.placeholder.code(self.output_text)
        return super().write(s)

def ejecutar_proceso_principal(cookie, log_placeholder, metrics):
    stream_writer = StreamlitLogWriter(log_placeholder)
    m1, m2, m3 = metrics # Desempaquetamos las columnas de métricas
    
    try:
        # FASE 1: Artifactory y Configuración
        with contextlib.redirect_stdout(stream_writer):
            m3.markdown("🟡 **Estado:** Consultando API ARTIFACTORY...")
            print("--- Iniciando Procesamiento LRA ---")
            artifact.initialize()
            m1.metric("Archivos", "213k+", "Artifactory")
            
            excel.initialize()
            generate.initialize()
            m2.metric("Carpetas", "Procesadas", "Filtros OK")
            print("🚀 Iniciando peticiones paralelas (Fase silenciosa en consola web)...")

        # FASE 2: Request Multi (Fuera del redirect para estabilidad)
        m3.markdown("🟡 **Estado:** Realizando consultas en consola LRBA..")
        request_multi.initialize(cookie)

        # FASE 3: Clonado y Análisis final
        with contextlib.redirect_stdout(stream_writer):
            m3.markdown("🟡 **Estado:** Analizando POMs...")
            print("✅ Peticiones finalizadas. Iniciando clonado y análisis...")
            clone_glo.initialize()
            pom.initialize()
            
            print("\n[OK] Análisis completado con éxito.")
            m3.markdown("🟢 **Estado:** Finalizado")
            
        return True

    except Exception as e:
        with contextlib.redirect_stdout(stream_writer):
            print(f"\n[ERROR] Fallo en la ejecución: {str(e)}")
        m3.markdown("🔴 **Estado:** Error")
        return False

# --- CONFIGURACIÓN DE LA INTERFAZ ---
st.set_page_config(page_title="LRA Colombia Automation Tool", layout="wide", page_icon="📊")

# Título con estilo
st.markdown("# 🛠️ Grimorio LRA Colombia")
st.markdown("### Automatización de arquitectura LRA Batch Colombia")
st.divider()

# --- ÁREA DE MÉTRICAS (Resumen visual) ---
st.subheader("📊 Resumen del Proceso")
col_metrics = st.columns(3)
# Creamos placeholders para actualizar las métricas en tiempo real
m1 = col_metrics[0].empty()
m2 = col_metrics[1].empty()
m3 = col_metrics[2].empty()

m1.metric("Archivos", "0", "Pendiente")
m2.metric("Carpetas", "0", "Pendiente")
m3.markdown("⚪ **Estado:** Esperando ejecución")

st.divider()

with st.sidebar:
    st.header("🔑 Autenticación")
    input_cookie = st.text_area("Cookie de Sesión LRBA", placeholder="GCP_...", height=150)
    st.info("Asegúrate de que la cookie esté vigente en la consola de Chrome.")
    st.divider()
    boton_run = st.button("🚀 Iniciar Ejecución Full", use_container_width=True, disabled=not input_cookie)

# --- CONSOLA DE SALIDA ---
st.subheader("🖥️ Detalle de Ejecución")
with st.expander("Ver logs del sistema", expanded=True):
    log_area = st.empty()

# --- LÓGICA DE EJECUCIÓN Y DESCARGA ---
if boton_run:
    with st.status("⚙️ Trabajando en el análisis...", expanded=True) as status:
        # Pasamos las métricas como argumentos para que se actualicen desde adentro
        exito = ejecutar_proceso_principal(input_cookie, log_area, [m1, m2, m3])
        
        if exito:
            status.update(label="✅ Análisis completo", state="complete", expanded=False)
        else:
            status.update(label="❌ Error en el proceso", state="error", expanded=True)
  
    if exito:
        st.toast("¡Archivo generado con éxito!", icon="🎉")
        st.success("### 🎉 ¡Proceso completado!")
        
        ruta_excel = os.path.join("scripts", "reporte_versions.xlsx") 
        
        if os.path.exists(ruta_excel):
            with open(ruta_excel, "rb") as f:
                st.download_button(
                    label="📥 Descargar Reporte Final (Excel)",
                    data=f,
                    file_name="Reporte_LRA_Colombia.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    type="primary" # Resalta el botón en color azul
                )
        else:
            st.error("No se encontró el archivo Excel. Verifica la ruta en `constants.py`.")