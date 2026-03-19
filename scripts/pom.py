import os
import xml.etree.ElementTree as ET
import pandas as pd
import scripts.constants as constants

# --- Funciones de Extracción XML (Sin Cambios) ---

def extraer_version_pom(ruta_archivo):
    """
    Analiza un archivo pom.xml y extrae la etiqueta <version>.
    PRIORIZA la versión de <parent> sobre la versión directa del proyecto.
    """
    try:
        namespace = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
        
        # 1. BUSCAR PRIMERO la versión dentro de <parent> (PRIORIDAD)
        parent_element = root.find('mvn:parent', namespace)
        if parent_element is not None:
            parent_version_element = parent_element.find('mvn:version', namespace)
            if parent_version_element is not None:
                return parent_version_element.text
        
        # 2. Si <parent> no existe o no tiene versión, buscar la versión directa del proyecto
        version_element = root.find('mvn:version', namespace)
        if version_element is not None:
            return version_element.text
        
        # 3. Si no se encontró ninguna versión
        return "No encontrada"

    except ET.ParseError:
        return "Error de parsing XML"
    except Exception as e:
        return f"Error: {e}"

# --- Función de Búsqueda y Reporte (MODIFICADA) ---

def buscar_poms_y_reportar(ruta_inicio='./source'):
    """
    Busca recursivamente archivos pom.xml, genera un reporte con el nombre
    del directorio limpio y lo exporta a un archivo Excel.
    """
    
    # Esto convierte './source' en la ruta completa real (ej: C:/Users/.../source)
    ruta_absoluta = os.path.join(os.path.abspath(ruta_inicio),"scripts")
    print("-----------------------RUTA__--------------------",ruta_absoluta)
    reporte = []
    
    # Recorre recursivamente los directorios
    for root, dirs, files in os.walk(ruta_absoluta):
        for file in files:
            if file == 'pom.xml':
                ruta_completa = os.path.join(root, file)
                version = extraer_version_pom(ruta_completa)
                
                # *** CAMBIO CLAVE AQUÍ ***
                # Usamos os.path.basename(root) para obtener solo el nombre del directorio
                nombre_proyecto = os.path.basename(root)
                
                reporte.append({
                    "Directorio": nombre_proyecto, 
                    "Version": version
                })

    # --- EXPORTACIÓN A EXCEL ---
    nombre_archivo_excel = constants.REPORTE_VERSIONES_XLSX

    if not reporte:
        print("No se encontraron archivos pom.xml en la ruta especificada. No se generará el Excel.")
        return

    # 1. Convertir la lista de diccionarios a un DataFrame de Pandas
    df = pd.DataFrame(reporte)

    # 2. Exportar el DataFrame a un archivo Excel (.xlsx)
    try:
        df.to_excel(os.path.join(os.path.dirname(__file__), constants.DATA_FOLDER, nombre_archivo_excel), index=False, engine='openpyxl')
        print("-" * 50)
        print(f"✅ Reporte generado con éxito en: {nombre_archivo_excel}")
        print("-" * 50)
    except Exception as e:
        print(f"❌ Error al intentar guardar el archivo Excel: {e}")

    # --- MOSTRAR RESULTADOS EN CONSOLA ---
    print("\n## 📄 Reporte de Versiones de Proyectos Maven (pom.xml) ##")
    for item in reporte:
        print("-" * 50)
        print(f"Directorio: {item['Directorio']}")
        print(f"Versión:    {item['Version']}")
    
    print("-" * 50)
    print(f"\nTotal de archivos pom.xml encontrados: {len(reporte)}")


def initialize(): 
# if __name__ == "__main__":
    buscar_poms_y_reportar('.')