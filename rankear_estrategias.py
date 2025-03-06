import pandas as pd
import os
import shutil

def rankear_estrategias(ruta_csv, sep=',', required_columns=None, pesos=None):
    """
    Rankea estrategias de trading desde un CSV y genera resultados y archivos .sqx renombrados.
    
    Args:
        ruta_csv (str): Ruta del archivo CSV (por ejemplo, "C:/ESTRATEGIAS_RANKING/DatabankExport.csv").
        sep (str): Delimitador del CSV (por defecto ',').
        required_columns (list): Lista de columnas para rankear (por defecto ['Ret/DD Ratio (IS)', 'Profit factor (IS)', 'Sharpe Ratio (IS)']).
        pesos (dict): Pesos para ponderar las columnas (por defecto {'Ret/DD Ratio (IS)': 0.5, 'Profit factor (IS)': 0.3, 'Sharpe Ratio (IS)': 0.2}).
    
    Returns:
        pd.DataFrame: DataFrame con las 100 mejores estrategias rankeadas.
    """
    if required_columns is None:
        required_columns = ['Ret/DD Ratio (IS)', 'Profit factor (IS)', 'Sharpe Ratio (IS)']
    if pesos is None:
        pesos = {
            'Ret/DD Ratio (IS)': 0.5,
            'Profit factor (IS)': 0.3,
            'Sharpe Ratio (IS)': 0.2
        }

    try:
        # Leer el CSV especificando el delimitador
        data = pd.read_csv(ruta_csv, sep=sep)
        
        # Verificar y limpiar las columnas disponibles
        print("Columnas disponibles en el CSV (sin espacios extra):")
        columns = [col.strip() for col in data.columns]
        print(columns)
        
        # Validar que las columnas seleccionadas sean numéricas
        non_numeric = [col for col in required_columns if not pd.api.types.is_numeric_dtype(data[col])]
        if non_numeric:
            raise ValueError(f"Las siguientes columnas no son numéricas y no se pueden rankear: {non_numeric}")
        
        # Asegurarnos de que las columnas existan
        missing_columns = [col for col in required_columns if col.strip() not in columns]
        if missing_columns:
            raise ValueError(f"Las siguientes columnas no se encontraron: {missing_columns}. Ajusta los nombres de las columnas en 'required_columns'.")
        
        # Añadir una columna de identificación usando la primera columna (Strategy Name)
        data['ID'] = data.iloc[:, 0]
        
        # Crear copias del DataFrame para los rankings individuales
        rankings = pd.DataFrame(index=data.index)
        
        # Rankear individualmente por cada parámetro
        for param in required_columns:
            # Asumimos "menor es mejor" para Stagnation (IS), Drawdown (IS), Exposure (IS), Avg. Loss (IS), y Avg. Loss (OOS), y "mayor es mejor" para otros
            ascending = param in ['Stagnation (IS)', 'Drawdown (IS)', 'Exposure (IS)', 'Avg. Loss (IS)', 'Avg. Loss (OOS)']
            rankings[f'Rank_{param}'] = data[param].rank(ascending=ascending, method='min')
        
        # Mostrar las 10 mejores estrategias por cada ranking individual con ID
        for param in required_columns:
            print(f"\nTop 10 estrategias por {param}:")
            print(data.iloc[rankings[f'Rank_{param}'].nsmallest(10).index][['ID', param]].sort_values(by=param, ascending=param in ['Stagnation (IS)', 'Drawdown (IS)', 'Exposure (IS)', 'Avg. Loss (IS)', 'Avg. Loss (OOS)']))
        
        # Calcular puntuación ponderada
        max_rank = len(data)
        data['Puntuacion_Ponderada'] = sum((max_rank - rankings[f'Rank_{param}']) / max_rank * pesos[param] for param in required_columns)
        
        # Ordenar por puntuación ponderada y tomar las 100 mejores
        top_100 = data.sort_values(by='Puntuacion_Ponderada', ascending=False).head(100)
        
        # Agregar columna de posición (empezando desde 1)
        top_100['Posicion'] = range(1, len(top_100) + 1)
        
        # Mostrar las 10 mejores estrategias de la lista definitiva con ID y Posicion
        print("\nTop 10 estrategias de la lista definitiva (ponderada):")
        print(top_100[['Posicion', 'ID'] + required_columns + ['Puntuacion_Ponderada']].head(10))
        
        # Guardar la lista definitiva de las 100 mejores en un nuevo CSV
        top_100.to_csv(os.path.join(os.path.dirname(ruta_csv), 'top_100_ponderado.csv'), index=False)
        print(f"\nLista de las 100 mejores estrategias guardada en {os.path.join(os.path.dirname(ruta_csv), 'top_100_ponderado.csv')}")
        
        # Crear carpeta mejores_estrategias si no existe
        carpeta_origen = os.path.dirname(ruta_csv)
        carpeta_destino = os.path.join(carpeta_origen, "mejores_estrategias")
        os.makedirs(carpeta_destino, exist_ok=True)  # Crea la carpeta si no existe
        
        # Borrar el contenido existente de la carpeta mejores_estrategias antes de copiar nuevos archivos
        if os.path.exists(carpeta_destino):
            for item in os.listdir(carpeta_destino):
                item_path = os.path.join(carpeta_destino, item)
                try:
                    if os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
                except Exception as e:
                    print(f"Error al borrar {item_path}: {e}")
        
        # Copiar y renombrar los archivos .sqx correspondientes con numeración al inicio
        archivos_sqx = [f for f in os.listdir(carpeta_origen) if f.endswith('.sqx')]
        
        for idx, row in top_100.iterrows():
            id_estrategia = row['ID'].replace(':', '_')  # Reemplazar ':' por '_' para coincidir con nombres de archivos
            posicion = row['Posicion']
            # Formatear la posición con dos dígitos (01, 02, ..., 100)
            posicion_str = f"{posicion:02d}"
            for archivo in archivos_sqx:
                if archivo.startswith(id_estrategia):
                    viejo_nombre = os.path.join(carpeta_origen, archivo)
                    nuevo_nombre = os.path.join(carpeta_destino, f"{posicion_str}_{id_estrategia}.sqx")
                    shutil.copy2(viejo_nombre, nuevo_nombre)  # Copiar y renombrar
                    print(f"Copiado y renombrado: {viejo_nombre} -> {nuevo_nombre}")
        
        print(f"\nSe han copiado y renombrado los archivos .sqx de las 100 mejores estrategias a {carpeta_destino}")
        return top_100

    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo en {ruta_csv}. Verifica la ruta. Detalle: {e}")
        return None
    except ValueError as e:
        print(f"Error de validación: {e}")
        return None
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
        return None

if __name__ == "__main__":
    # Ejemplo de ejecución directa
    rankear_estrategias("C:/ESTRATEGIAS_RANKING/DatabankExport.csv", sep=';')