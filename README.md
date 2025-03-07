# Ranker de Estrategias de Trading

Este proyecto permite rankear estrategias de trading basadas en métricas seleccionadas, utilizando un dashboard interactivo creado con Streamlit. Podés analizar métricas como Ret/DD Ratio, Profit Factor, Sharpe Ratio, y más, asignarles pesos personalizados, y obtener un ranking de las mejores estrategias. También genera gráficos y organiza las estrategias seleccionadas en una carpeta ordenada.

## Instalación

Sigue estos pasos para instalar y ejecutar el Ranker de Estrategias de Trading en tu computadora:

1. **Descarga el script de instalación**:
   - Descarga el archivo `install_setup.bat` desde este repositorio. Haz clic en el archivo y selecciona "Download" (o usa el enlace directo si lo subiste).

2. **Ejecuta el script**:
   - Haz doble clic en `install_setup.bat`. Este script:
     - Verificará si Python está instalado; si no, lo descargará e instalará.
     - Instalará las librerías necesarias (`pandas`, `matplotlib`, `numpy`, `streamlit`).
     - Creará la carpeta `C:\ESTRATEGIAS_RANKING` (o te preguntará si querés usarla si ya existe).
     - Descargará los scripts `dashboard.py` y `rankear_estrategias.py` desde este repositorio.
     - Creará un archivo de ejemplo `DatabankExport.csv` (si no existe).

3. **Responde a las preguntas del script**:
   - Si la carpeta `C:\ESTRATEGIAS_RANKING` ya existe, te preguntará si deseas usarla o crearla de nuevo.
   - Si los archivos `dashboard.py`, `rankear_estrategias.py`, o `DatabankExport.csv` ya existen, te preguntará si deseas sobrescribirlos.

4. **Inicia el dashboard**:
   - Abre una terminal (CMD o PowerShell).
   - Ejecuta el siguiente comando:

streamlit run C:\ESTRATEGIAS_RANKING\dashboard.py

- Esto abrirá el dashboard en tu navegador predeterminado (normalmente en `http://localhost:8501`).

## Uso

Una vez que el dashboard esté abierto en el navegador, podés:

- **Seleccionar métricas**: Elige las métricas para rankear (por ejemplo, `Ret/DD Ratio (IS)`, `Profit factor (IS)`, `Sharpe Ratio (IS)`).
- **Asignar pesos**: Ajusta los pesos para cada métrica (la suma debe ser 1.0).
- **Rankear estrategias**: Haz clic en "Rankear Estrategias" para ver:
- Una tabla con las 10 mejores estrategias.
- Gráficos individuales por métrica.
- Un gráfico normalizado comparando todas las métricas.
- **Resultados guardados**: Las mejores estrategias (archivos `.sqx`) se copiarán y renombrarán en la carpeta `C:\ESTRATEGIAS_RANKING\mejores_estrategias` con un número al inicio (por ejemplo, `01_StrategyX.sqx` para la mejor estrategia).

## Requisitos

- **Sistema operativo**: Windows (el script `.bat` está diseñado para Windows).
- **Conexión a internet**: Necesaria para descargar Python, las librerías, y los scripts desde GitHub.
- **Permisos**: Debes tener permisos para escribir en `C:\ESTRATEGIAS_RANKING`. Si hay problemas, ejecuta `install_setup.bat` como administrador.
- **Espacio en disco**: Aproximadamente 500 MB para Python y las librerías.

## Notas

- **Archivos `.sqx`**: Coloca tus archivos `.sqx` manualmente en `C:\ESTRATEGIAS_RANKING` para que el script los procese. Los nombres deben coincidir con los IDs en el archivo `DatabankExport.csv`.
- **Parámetros "menor es mejor"**: Las métricas como `Stagnation (IS)`, `Drawdown (IS)`, `Exposure (IS)`, `Avg. Loss (IS)`, y `Avg. Loss (OOS)` se rankean como "menor es mejor". Otras métricas (como `Ret/DD Ratio`) se rankean como "mayor es mejor".
- **Problemas comunes**:
- Si el navegador no se abre, ve a `http://localhost:8501` manualmente.
- Si `localhost:8501` no funciona, revisa la terminal para ver si Streamlit usó otro puerto (por ejemplo, `8502`).
- Si hay errores de instalación, verifica tu conexión a internet y permisos.

## Contribuciones

Este proyecto fue creado por [marianofx-sqx](https://github.com/marianofx-sqx). Si tenés sugerencias o mejoras, podés abrir un issue en este repositorio.

## Licencia

Este proyecto es de código abierto y puede ser usado libremente. No se proporciona ninguna garantía.
