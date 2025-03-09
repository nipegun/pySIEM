import json
import base64
import sys
import requests
from urllib.parse import quote

# Verificar que se pasaron los 4 argumentos requeridos
if len(sys.argv) != 5:
  print("Uso: python sendlog.py <protocolo> <ip> <puerto> <carpeta>")
  sys.exit(1)

# Definir las variables a partir de los argumentos pasados al script
#vProto =   sys.argv[1]
vProto =   "http"
#vIP =      sys.argv[2]
vIP =      "localhost"
#vPuerto =  sys.argv[3]
vPuerto =  8000
#vCarpeta = sys.argv[4]
vCarpeta = "/log"

# Popular el log
vLogJSON = {
  "Fecha": "a2024m01d28@21:36:28-GMT+1",
  "Datos": "HolaMundo!"
}

# Construir la URL dinámicamente
vURL = f"{vProto}://{vIP}:{vPuerto}{vCarpeta}"

# Codificar el json
vDatos = json.dumps(vLogJSON)
vJSONenBase64 = base64.b64encode(vDatos.encode()).decode()

# Enviar la alerta con la URL construida dinámicamente
requests.post(vURL, json=vJSONenBase64)

