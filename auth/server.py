import asyncio
import jwt
import datetime
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends, Query
from typing import List

SECRET_KEY = "clave_secreta_super_segura"  # ¡Cámbiala por una más segura!

app = FastAPI()
clients: List[WebSocket] = []  # Lista de clientes conectados


def create_token(username: str) -> str:
  """Genera un token JWT con expiración"""
  payload = {
    "sub": username,
    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
  }
  return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


async def verify_token(token: str):
  """Verifica y decodifica el token JWT"""
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return payload["sub"]  # Devuelve el usuario autenticado
  except jwt.ExpiredSignatureError:
    raise HTTPException(status_code=401, detail="Token expirado")
  except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Token inválido")


@app.post("/login")
async def login(username: str):
  """Simula un login y devuelve un token JWT"""
  token = create_token(username)
  return {"token": token}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
  """WebSocket protegido con autenticación JWT"""
  user = await verify_token(token)  # Valida el token antes de aceptar la conexión

  await websocket.accept()
  clients.append(websocket)
  print(f"🔐 Usuario autenticado: {user}")

  try:
    while True:
      await websocket.receive_text()  # Mantiene la conexión abierta
  except WebSocketDisconnect:
    print(f"❌ Usuario {user} desconectado")
  finally:
    try:
      clients.remove(websocket)
    except ValueError:
      pass  # Evita errores si el cliente ya fue eliminado


@app.post("/log")
async def receive_log(data: dict):
  """Recibe logs desde agentes y los envía en tiempo real a WebSockets"""
  log_message = data.get("message", "Sin datos")

  # Crear una copia de la lista para evitar modificaciones durante la iteración
  disconnected_clients = []
  for client in clients[:]:  # Iterar sobre una copia de la lista
    try:
      await client.send_text(log_message)
    except Exception as e:
      print(f"Cliente desconectado, eliminándolo de la lista: {e}")
      disconnected_clients.append(client)

  # Remover clientes desconectados de manera segura
  for client in disconnected_clients:
    clients.remove(client)

  return {"status": "Log recibido"}


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
