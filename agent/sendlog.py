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
  "clave1": "valor1",
  "clave2": "valor2"
}

# Construir la URL dinámicamente
vURL = f"{vProto}://{vIP}:{vPuerto}{vCarpeta}"

# Enviar la alerta con la URL construida dinámicamente
requests.post(vURL, json=vLogJSON)
