import pandas as pd
import os
from tabulate import tabulate

# Obtener la ruta del directorio actual (donde se encuentra el script)
current_directory = os.path.dirname(os.path.abspath(__file__))

# Construir la ruta completa al archivo CSV
csv_file_path = os.path.join(current_directory,
'DinamicaEstructuraCh.csv')

# Verificar si el archivo existe en la ruta especificada
if not os.path.exists(csv_file_path):
    print(f"El archivo '{csv_file_path}' no se encontró.")
else:
    # Cargar el archivo CSV sin encabezado, cada fila tiene dos valores: inicio y fin
    df = pd.read_csv(csv_file_path, delimiter=';', header=None, names=['start', 'end'])

    # Convertir el DataFrame a una lista de tuplas numéricas
    formatted_ranges = [tuple(row) for row in df.astype(int).values.tolist()]

    # Imprimir la lista en el formato pedido sin espacios extra
    formatted_ranges_str = '[' + ','.join(f'({start},{end})' for start, end in formatted_ranges) + ']'
    print(formatted_ranges_str)