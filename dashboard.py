import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from rankear_estrategias import rankear_estrategias  # Importa la función del script principal

# Título del dashboard
st.title("Ranker de Estrategias de Trading")

# Cargar el CSV
ruta_csv = "C:/ESTRATEGIAS_RANKING/DatabankExport.csv"
if os.path.exists(ruta_csv):
    data = pd.read_csv(ruta_csv, sep=';')
    columns = [col.strip() for col in data.columns]

    # Detectar solo columnas numéricas para usar como métricas (excluir explícitamente no numéricas y específicas)
    numeric_columns = [col for col in columns if pd.api.types.is_numeric_dtype(data[col]) and col not in ['Strategy Name', 'TimeFrame (IS)', 'Mini equity chart (IS)', 'Mini equity chart (OOS)']]

    # Selección de parámetros (solo columnas numéricas)
    st.header("Selecciona las métricas para rankear")
    params = st.multiselect("Métricas disponibles", numeric_columns, default=['Ret/DD Ratio (IS)', 'Profit factor (IS)', 'Sharpe Ratio (IS)'])

    # Pesos para los parámetros seleccionados, con valores iniciales predeterminados
    st.header("Asigna pesos (suma = 1)")
    pesos = {}
    total_pesos = 0
    initial_weights = {
        'Ret/DD Ratio (IS)': 0.5,
        'Profit factor (IS)': 0.3,
        'Sharpe Ratio (IS)': 0.2
    }
    for param in params:
        # Usar los pesos iniciales predeterminados si están definidos, o 0.1 como valor por defecto para otras métricas
        default_weight = initial_weights.get(param, 0.1)
        peso = st.slider(f"Peso para {param}", 0.0, 1.0, default_weight)
        pesos[param] = peso
        total_pesos += peso

    if total_pesos != 1.0:
        st.error("La suma de los pesos debe ser 1.0. Ajusta los valores.")
    else:
        if st.button("Rankear Estrategias"):
            # Lógica para ejecutar el ranking
            result = rankear_estrategias(ruta_csv, sep=';', required_columns=params, pesos=pesos)
            if result is not None:
                st.write("Top 10 estrategias definitivas:")
                st.write(result.head(10))

                # 1. Gráficos individuales por parámetro (valores originales, cada métrica en su escala)
                st.subheader("Gráficos individuales por métrica (valores originales, escala natural)")
                for param in params:
                    fig, ax = plt.subplots(figsize=(12, 6))
                    top_10_param = result.sort_values(by=param, ascending=param in ['Stagnation (IS)', 'Drawdown (IS)', 'Exposure (IS)', 'Avg. Loss (IS)', 'Avg. Loss (OOS)']).head(10)
                    x = np.arange(len(top_10_param))
                    ax.bar(x, top_10_param[param], width=0.5)
                    ax.set_ylabel(param)
                    ax.set_title(f'Top 10 Estrategias por {param} (Valores Originales)')
                    ax.set_xticks(x)
                    ax.set_xticklabels(top_10_param['ID'], rotation=45, ha='right')
                    plt.tight_layout()
                    st.pyplot(fig)

                # 2. Gráfico normalizado (escala 0-1, como estaba originalmente)
                st.subheader("Gráfico Normalizado (escala 0-1)")
                top_10_definitiva = result.head(10)
                normalized_metrics = {}
                for metric in params:
                    min_val = top_10_definitiva[metric].min()
                    max_val = top_10_definitiva[metric].max()
                    if max_val != min_val:
                        normalized_metrics[metric] = (top_10_definitiva[metric] - min_val) / (max_val - min_val)
                    else:
                        normalized_metrics[metric] = top_10_definitiva[metric] - min_val
                
                x = np.arange(len(top_10_definitiva))
                width = 0.25
                
                fig, ax = plt.subplots(figsize=(12, 6))
                offset = width * (len(params) - 1) / 2
                for i, metric in enumerate(params):
                    ax.bar(x - offset + i * width, normalized_metrics[metric], width, label=metric)
                
                ax.set_ylabel('Valores Normalizados (0-1)')
                ax.set_title('Top 10 Estrategias Definitivas - Métricas Clave (Normalizadas)')
                ax.set_xticks(x)
                ax.set_xticklabels(top_10_definitiva['ID'], rotation=45, ha='right')
                ax.set_ylim(0, 1)
                ax.legend()
                
                ax.text(0.02, 0.98, 'Nota: Las métricas están normalizadas a una escala de 0 a 1 para comparación visual.', 
                        transform=ax.transAxes, fontsize=10, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.5))
                
                plt.tight_layout()
                st.pyplot(fig)

                # 3. Leyenda de parámetros con "menor es mejor"
                st.info("Parámetros rankeados como 'menor es mejor': Stagnation (IS), Drawdown (IS), Exposure (IS), Avg. Loss (IS), Avg. Loss (OOS).")

                # 4. Leyenda sobre las estrategias guardadas
                st.info("Las estrategias se han guardado en la carpeta 'mejores_estrategias' con un número añadido al inicio de los nombres de los archivos .sqx (por ejemplo, 01_Strategy X.Y:ZZZ.sqx) para indicar el orden de calidad, donde 1 es la mejor estrategia, 2 la segunda mejor, y así sucesivamente.")

                st.success("Rankings generados y archivos .sqx copiados/renombrados en C:/ESTRATEGIAS_RANKING/mejores_estrategias")
            else:
                st.error("Error al procesar el ranking. Verifica los mensajes en la terminal o los parámetros seleccionados.")
else:
    st.error("No se encontró el archivo DatabankExport.csv en C:/ESTRATEGIAS_RANKING")