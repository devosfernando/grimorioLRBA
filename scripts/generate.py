import pandas as pd
import json
import os
import scripts.constants as constants

def excel_a_json(nombre_archivo_excel, nombre_archivo_json, nombre_hoja=0):
    print(f"Iniciando conversión de '{nombre_archivo_excel}' a '{nombre_archivo_json}'...")
    
    try:
        # 1. Leer el archivo de Excel usando pandas
        # El parámetro 'nombre_hoja' puede ser un nombre de hoja (string) o un índice (int)
        df = pd.read_excel(os.path.join(os.path.dirname(__file__), constants.DATA_FOLDER, nombre_archivo_excel), sheet_name=nombre_hoja)
        print(f"Datos leídos de la hoja: '{df.name if isinstance(nombre_hoja, str) else nombre_hoja}'")
        
        # 2. Convertir el DataFrame de pandas a un formato de lista de diccionarios (JSON)
        # 'records' genera una lista donde cada elemento es un diccionario que representa una fila
        datos_json = df.to_dict(orient='records')
        
        # 3. Escribir la lista de diccionarios en un archivo JSON
        with open(os.path.join(os.path.dirname(__file__), constants.DATA_FOLDER,nombre_archivo_json), 'w', encoding='utf-8') as f:
            # indent=4 para que el JSON sea legible (bonito)
            json.dump(datos_json, f, indent=4, ensure_ascii=False)
            
        print(f"✅ Conversión completada. Datos guardados en '{nombre_archivo_json}'.")
        
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró el archivo '{nombre_archivo_excel}'.")
    except ValueError as e:
        print(f"❌ ERROR: Problema con la lectura de la hoja o el archivo Excel. Detalle: {e}")
    except Exception as e:
        print(f"❌ ERROR Inesperado: {e}")

# --- Uso del script ---
# if __name__ == "__main__":
def initialize():
    archivo_excel_entrada = constants.TOTAL_XLSX
    archivo_json_salida = constants.DATA_JSON
    
    excel_a_json(archivo_excel_entrada, archivo_json_salida)