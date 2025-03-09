import asyncio
import base64
import json
from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

# Lista de clientes WebSocket conectados
clients: List[WebSocket] = []

def decode_base64_json(encoded_str: str) -> dict:
  """Decodifica un JSON completo en Base64"""
  try:
    decoded_bytes = base64.b64decode(encoded_str)
    decoded_json = json.loads(decoded_bytes.decode("utf-8"))
    return decoded_json
  except Exception:
    return {"error": "Error al decodificar JSON en Base64"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
  """WebSocket para enviar eventos en tiempo real al dashboard"""
  await websocket.accept()
  clients.append(websocket)
  try:
    while True:
      await asyncio.sleep(1)  # Mantiene la conexión abierta
  except Exception as e:
    print(f"Error en WebSocket: {e}")
  finally:
    # Se elimina el cliente al cerrarse la conexión
    clients.remove(websocket)

@app.post("/log")
async def receive_log(encoded_data: str):
  """Recibe un JSON en Base64, lo decodifica y lo envía en tiempo real a WebSockets"""
  decoded_json = decode_base64_json(encoded_data)  # Decodificar JSON completo
  
  # Si hubo un error en la decodificación, no procesamos el mensaje
  if "error" in decoded_json:
    return {"status": "Error", "message": decoded_json["error"]}

  # Extraer el mensaje dentro del JSON decodificado
  log_message = decoded_json.get("message", "Sin datos")
  
  disconnected_clients = []
  for client in clients:
    try:
      await client.send_text(log_message)  # Enviar mensaje decodificado a WebSockets
    except Exception as e:
      print(f"Cliente desconectado, eliminándolo de la lista: {e}")
      disconnected_clients.append(client)

  # Eliminar clientes que ya no están disponibles
  for client in disconnected_clients:
    clients.remove(client)

  return {"status": "Log recibido", "decoded": decoded_json}

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
