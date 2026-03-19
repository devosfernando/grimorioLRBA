
# 🛠️ Grimorio LRA Colombia

Este proyecto centraliza los scripts de procesamiento y validación para la arquitectura **LRA (Lightweight Runtime Architecture)**, permitiendo una ejecución estandarizada, visual y eficiente de los componentes de arquitectura.

---

## 📖 Descripción General
El objetivo de esta herramienta es automatizar las tareas de revisión de versiones, procesamiento de datos y validación de componentes **UUAA**. Facilita la migración y la ejecución de pruebas mediante una interfaz amigable que encapsula la lógica compleja de los scripts de Python.

---

## 📂 Estructura del Proyecto
* **`app.py`**: Interfaz gráfica principal (Frontend) construida con **Streamlit**.
* **`scripts/`**: Directorio con la lógica core y funciones de procesamiento.
    * `request.py`: Manejo de peticiones y autenticación (Línea 24 para Cookies).
* **`requirements.txt`**: Listado de dependencias necesarias.(pip install -r requirements.txt)

---

## ⚠️ Pasos Críticos para la Ejecución

Para que el script funcione correctamente, es obligatorio cumplir con los siguientes requisitos de autenticación:

1. **Token de Artifactory:** Antes de ejecutar, debes contar con el token de Artifactory guardado en las variables de entorno de tu equipo con el nombre: `ARTIFACTORY_ACCESS_TOKEN`.
2. **Cookie de Sesión LRBA:** Se debe generar e insertar la cookie de sesión de la consola de LRBA siguiendo los pasos detallados abajo.
3. **Comando de ejecución:** El script principal se ejecuta mediante:
   ```bash
   echo "y" | streamlit run app.py


4. **PASOS PARA LA GENERACIÓN E INSERCION DE COOKIE DE SESION LRBA**

        1. SE DEBE INGRESAR A LA SIGUIENTE URL: https://bbva-lrba.appspot.com/#/live-02/cross/status/.
        2. DESDE AQUI DAR CLICK DERECHO Y SELECCIONAR INSPECCIONAR.
        3. DIRIGIRSE AL APARTDO LLAMADO "NETWORK" Y REALIZAR UNA CONSULTA EN LA PÁGINA DE CROSS O CUALQUIERA DEL LUGAR.
        4. EN EL APARTADO NETWORK DIRIGIRSE A LA PRIMER CONSULTA, NORMALMENTE UNA LLAMADA STATUS? Y SELECCIONARLA.
        5. EXTRAER O COPIAR DEL APARTADO REQUEST HEADERS EL HEADER LLAMADO: "COOKIE" NORMALMENTE INICIA CON LAS LETRAS GCP_.
        6. COPIAR ESTE CONTENIDO EN EL ARCHIVO scripts/request.py QUE SE ENCUENTRA EN LA CARPETA SCRIPTS EN LA LINEA 24 ELIMINANDO LA LINEA QUE ESTABA PREVIAMENTE ESCRITA.
