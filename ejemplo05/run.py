import csv
import json
import requests

# ---------------------- CONVERSIÓN DE CSV A JSON ----------------------

# Nombre del archivo CSV de origen y el archivo JSON de salida
csv_file_path = "atp_tennis.csv"
json_file_path = "datos.json"

# Lista donde almacenaremos los documentos convertidos
data = []

# Lectura del archivo CSV con codificación adecuada para evitar errores de caracteres
with open(csv_file_path, mode="r", encoding="latin-1") as csv_file:
    reader = csv.DictReader(csv_file)  # Convierte las filas en diccionarios
    for row in reader:
        data.append(row)  # Agrega cada fila a la lista de datos

# Estructurar el JSON con la clave "docs" para que sea compatible con CouchDB
json_data = {"docs": data}

# Guarda los datos en formato JSON con indentación para mayor legibilidad
with open(json_file_path, mode="w", encoding="utf-8") as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"Conversión completada. Archivo JSON guardado en '{json_file_path}'")

# ---------------------- SUBIDA A COUCHDB ----------------------

# Cargar datos desde archivo
with open(json_file_path, 'r', encoding="utf-8") as f:
    data = json.load(f)

# ------------------ SUBIDA MASIVA A 'persona005' USANDO _bulk_docs ------------------
base_datos_bulk = "persona005"
url_bulk = f"http://127.0.0.1:5984/{base_datos_bulk}/_bulk_docs"
headers = {'Content-Type': 'application/json'}

# Enviar datos en un solo lote
response_bulk = requests.post(url_bulk, headers=headers, json=data)
print(f"Subida masiva a {base_datos_bulk}: {response_bulk.status_code}")
print(response_bulk.json())  # Mostrar respuesta de CouchDB

# ------------------ SUBIDA INDIVIDUAL A 'persona006' DOCUMENTO POR DOCUMENTO ------------------
base_datos_individual = "persona006"
url_individual = f"http://127.0.0.1:5984/{base_datos_individual}"

# Enviar cada documento por separado
for doc in data['docs']:
    response_individual = requests.post(url_individual, json=doc)
    print(f"Insertando {doc.get('nombre', 'sin nombre')} en {base_datos_individual} | Estado: {response_individual.status_code}")
