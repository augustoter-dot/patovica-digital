from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import os

app = FastAPI(title="Patovica Digital API - Professional Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

WHITELIST_FILE = "whitelist.txt"
HISTORIAL_FILE = "historial_llamadas.txt"

def cargar_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        return ["+543815550000"]
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

@app.get("/whitelist")
def ver_whitelist():
    return {"whitelist": cargar_whitelist()}

@app.post("/whitelist/agregar")
def agregar_whitelist(payload: dict):
    nuevo_numero = payload.get("telefono", "").strip()
    if not nuevo_numero:
        return {"status": "error", "mensaje": "Número inválido"}
    
numeros = cargar_whitelist()
    if nuevo_numero not in numeros:
        with open(WHITELIST_FILE, "a", encoding="utf-8") as f:
            f.write(f"{nuevo_numero}\n")
        return {"status": "success", "mensaje": f"Número {nuevo_numero} agregado a la Lista Blanca"}
    
    return {"status": "info", "mensaje": "El número ya se encontraba en la Lista Blanca"}

@app.post("/evaluar-llamada")
def evaluar_llamada(payload: dict):
    telefono = payload.get("telefono", "Desconocido")
    latencia = payload.get("latencia_ms", 0)
    muletillas = payload.get("muletillas_detectadas", False)

    whitelist = cargar_whitelist()
    if telefono in whitelist:
        resultado = "PERMITIDA"
        motivo = "ACCESO DIRECTO: Contacto en Lista Blanca (Pasa sin filtros)"
        registrar_historial(telefono, resultado, motivo)
        return {"resultado": resultado, "motivo": motivo}

    if latencia > 400 or muletillas:
        resultado = "BLOQUEADA"
        motivo = "ALERTA ROJA: Posible Bot/IA -> [DEFENSA ACTIVA: Desafío lanzado]"
    else:
        resultado = "PERMITIDA"
        motivo = "VERIFICADO: Patrón de entropía humana confirmado (Pasa la llamada)"

    registrar_historial(telefono, resultado, motivo)
    return {"resultado": resultado, "motivo": motivo}

@app.get("/historial")
def ver_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return {"historial": []}
    with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
        lineas = [line.strip() for line in f.readlines()]
    return {"historial": lineas[-20:]}