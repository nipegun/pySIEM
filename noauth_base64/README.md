# pySIEM recibiendo datos en base64

## Para enviarle datos:

```
curl -X POST "http://localhost:8000/log" -H "Content-Type: application/json" -d '"eyJtZXNzYWdlIjogIkhvbGEgTXVuZG8ifQ=="'
```

⚠️ Nota: El JSON Base64 se envía como un string directamente en el cuerpo (con comillas "" alrededor de la cadena Base64).
