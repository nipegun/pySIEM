import time
import json
import base64
import requests

FASTAPI_URL = "http://127.0.0.1:8000/log"  # Cambia por la IP del servidor FastAPI
LOG_FILE = "/var/log/auth.log"

def encode_base64(text):
  """Codifica un string en Base64"""
  return base64.b64encode(text.encode()).decode()

def send_log(message):
  """Envía el log a FastAPI en formato JSON Base64"""
  payload = {"message": encode_base64(message)}
  try:
    response = requests.post(FASTAPI_URL, json=payload)
    if response.status_code == 200:
      print("[✓] Log enviado correctamente")
    else:
      print("[!] Error enviando log:", response.text)
  except requests.exceptions.RequestException as e:
    print("[!] No se pudo conectar a FastAPI:", e)

def tail_log():
  """Monitorea el archivo de log en busca de nuevos eventos"""
  with open(LOG_FILE, "r") as f:
    f.seek(0, 2)  # Ir al final del archivo
    while True:
      line = f.readline()
      if not line:
        time.sleep(1)
        continue
      send_log(line.strip())  # Enviar línea de log

if __name__ == "__main__":
  print("📡 Agente SIEM corriendo en Debian...")
  tail_log()
