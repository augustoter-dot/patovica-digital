from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Patovica Digital API")

# Habilitar CORS para permitir peticiones desde Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "estado": "Servidor Patovica Digital activo y blindado 🛡️",
        "status": "online"
    }

@app.post("/evaluar-llamada")
def evaluar_llamada(payload: dict):
    latencia = payload.get("latencia_ms", 0)
    muletillas = payload.get("muletillas_detectadas", False)

    if latencia > 400 or muletillas:
        return {"resultado": "BLOQUEADA", "motivo": "Posible voz sintética / Bot"}
    
    return {"resultado": "PERMITIDA", "motivo": "Llamada humana legítima"}