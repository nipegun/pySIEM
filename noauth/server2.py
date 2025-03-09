import asyncio
import base64
from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

# Lista de clientes WebSocket conectados
clients: List[WebSocket] = []

def decode_base64(encoded_str: str) -> str:
  """Decodifica una cadena en Base64"""
  try:
    return base64.b64decode(encoded_str).decode("utf-8")
  except Exception:
    return "Error al decodificar Base64"

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
async def receive_log(data: dict):
  """Recibe logs en Base64, los decodifica y los envía en tiempo real a WebSockets"""
  encoded_message = data.get("message", "")
  decoded_message = decode_base64(encoded_message)  # Decodificar mensaje
  
  disconnected_clients = []
  for client in clients:
    try:
      await client.send_text(decoded_message)  # Enviar mensaje decodificado a WebSockets
    except Exception as e:
      print(f"Cliente desconectado, eliminándolo de la lista: {e}")
      disconnected_clients.append(client)

  # Eliminar clientes que ya no están disponibles
  for client in disconnected_clients:
    clients.remove(client)

  return {"status": "Log recibido", "decoded": decoded_message}

if __name__ == "__main__":
  import uvicorn
  # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
  uvicorn.run(app, host="0.0.0.0", port=8000)  # SIN reload
