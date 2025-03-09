# Dependencias:
#   sudo apt -y install python3-fastapi
#


import asyncio
from fastapi import FastAPI, WebSocket
from typing import List

app = FastAPI()

# Lista de clientes WebSocket conectados
clients: List[WebSocket] = []

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
  """Recibe logs desde agentes y los envía en tiempo real a WebSockets"""
  log_message = data.get("message", "Sin datos")
  disconnected_clients = []

  for client in clients:
    try:
      await client.send_text(log_message)  # Envía el evento a los clientes WebSocket
    except Exception as e:
      print(f"Cliente desconectado, eliminándolo de la lista: {e}")
      disconnected_clients.append(client)

  # Eliminar clientes que ya no están disponibles
  for client in disconnected_clients:
    clients.remove(client)

  return {"status": "Log recibido"}

if __name__ == "__main__":
  import uvicorn
  # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
  uvicorn.run(app, host="0.0.0.0", port=8000)  # SIN reload
  # http://localhost:8000/docs para accceder a la documentación de la api tipo Swagger
  # http://localhost:8000/redoc para otro tipo de API
  # Para conectarse mediante websocket: wscat -c ws://localhost:8000/ws
