from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

app = FastAPI(title="Patovica Digital API - Professional Edition")

# Habilitar CORS para Flutter Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Archivos de control local
WHITELIST_FILE = "whitelist.txt"
HISTORIAL_FILE = "historial_llamadas.txt"

def cargar_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return ["+543815550000"] # Ejemplo por defecto
    with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def registrar_historial(telefono: str, resultado: str, motivo: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registro = f"[{timestamp}] Tel: {telefono} | Veredicto: {resultado} | Motivo: {motivo}\n"
    with open(HISTORIAL_FILE, "a", encoding="utf-8") as f:
        f.write(registro)

@app.get("/")
def home():
    return {
        "estado": "Servidor Patovica Digital activo y blindado 🛡️",
        "status": "online"
    }

@app.post("/evaluar-llamada")
def evaluar_llamada(payload: dict):
    telefono = payload.get("telefono", "Desconocido")
    latencia = payload.get("latencia_ms", 0)
    muletillas = payload.get("muletillas_detectadas", False)

    # 1. Validación de Lista Blanca
    whitelist = cargar_whitelist()
    if telefono in whitelist:
        resultado = "PERMITIDA"
        motivo = "Número agendado en Lista Blanca 🟢"
        registrar_historial(telefono, resultado, motivo)
        return {"resultado": resultado, "motivo": motivo}

    # 2. Motor de Análisis de Amenazas (Latencia / IA)
    if latencia > 400 or muletillas:
        resultado = "BLOQUEADA"
        motivo = "Posible voz sintética / Bot (Anomalía detectada)"
    else:
        resultado = "PERMITIDA"
        motivo = "Llamada humana legítima"

    # Registrar en el historial persistente
    registrar_historial(telefono, resultado, motivo)
    
    return {"resultado": resultado, "motivo": motivo}

@app.get("/historial")
def ver_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return {"historial": []}
    with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f.readlines()]
    return {"historial": lineas[-20:]} # Devuelve las últimas 20 llamadas