from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logica import procesar_llamada_inteligente, cargar_whitelist, agregar_a_whitelist, leer_historial

app = FastAPI(
    title="Patovica Digital API",
    description="Motor backend de protección antiestafa en tiempo real para aplicaciones móviles y de escritorio.",
    version="1.0.0"
)

class EvaluacionRequest(BaseModel):
    identificador: str
    texto_respuesta: str
    latencia: float

class WhitelistRequest(BaseModel):
    contacto: str

@app.get("/")
def home():
    return {"estado": "Servidor Patovica Digital activo y blindado 🛡️"}

@app.post("/evaluar-llamada")
def evaluar_llamada(datos: EvaluacionRequest):
    try:
        veredicto = procesar_llamada_inteligente(
            datos.identificador, 
            datos.texto_respuesta, 
            datos.latencia
        )
        es_alerta = "ALERTA" in veredicto
        return {
            "status": "success",
            "identificador": datos.identificador,
            "veredicto": veredicto,
            "alerta_activa": es_alerta
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/whitelist")
def obtener_whitelist():
    return {"whitelist": cargar_whitelist()}

@app.post("/whitelist")
def agregar_contacto(datos: WhitelistRequest):
    exito = agregar_a_whitelist(datos.contacto)
    if exito:
        return {"status": "success", "mensaje": f"Contacto {datos.contacto} añadido con éxito."}
    return {"status": "exists", "mensaje": "El contacto ya se encuentra en la lista blanca."}

@app.get("/historial")
def ver_historial():
    return {"historial": leer_historial()}