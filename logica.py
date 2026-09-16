import os
import random
from datetime import datetime

WHITELIST_FILE = "whitelist.txt"
HISTORIAL_FILE = "historial_llamadas.txt"

def cargar_whitelist():
    if not os.path.exists(WHITELIST_FILE):
        iniciales = ["+5493815000000", "+5493816111111", "mama", "trabajo"]
        with open(WHITELIST_FILE, "w", encoding="utf-8") as f:
            for item in iniciales:
                f.write(item + "\n")
        return iniciales
    
    with open(WHITELIST_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def agregar_a_whitelist(nuevo_contacto):
    contactos = cargar_whitelist()
    if nuevo_contacto not in contactos:
        with open(WHITELIST_FILE, "a", encoding="utf-8") as f:
            f.write(nuevo_contacto + "\n")
        return True
    return False

def registrar_en_historial(identificador, veredicto):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linea_registro = f"[{fecha_hora}] Llamada de: {identificador} -> Estado: {veredicto}\n"
    with open(HISTORIAL_FILE, "a", encoding="utf-8") as archivo:
        archivo.write(linea_registro)

def procesar_llamada_inteligente(identificador_llamante, texto_respuesta, tiempo_latencia):
    whitelist = cargar_whitelist()
    
    # Capa 0: Lista Blanca Dinámica
    if identificador_llamante.lower() in [c.lower() for c in whitelist]:
        veredicto = "ACCESO DIRECTO: Contacto en Lista Blanca (Pasa sin filtros)"
        registrar_en_historial(identificador_llamante, veredicto)
        return veredicto

    texto_limpio = texto_respuesta.lower()

    # Capa 1: Análisis de Latencia
    if tiempo_latencia < 0.5:
        veredicto = "ALERTA ROJA: Posible Bot/IA -> [DEFENSA ACTIVA: Desafío lanzado]"
        registrar_en_historial(identificador_llamante, veredicto)
        return veredicto

    # Capa 2: Análisis de Entropía Lingüística
    muletillas_humanas = ["eh", "este", "mm", "hola?", "bueno", "ah", "che", "fijate"]
    tiene_muletilla = any(muletilla in texto_limpio for muletilla in muletillas_humanas)

    if tiempo_latencia < 1.0 and not tiene_muletilla and len(texto_limpio.split()) > 3:
        veredicto = "ALERTA AMARILLA: Discurso fluido sospechoso -> [DEFENSA ACTIVA]"
        registrar_en_historial(identificador_llamante, veredicto)
        return veredicto

    veredicto = "VERIFICADO: Patrón humano confirmado (Pasa la llamada)"
    registrar_en_historial(identificador_llamante, veredicto)
    return veredicto

def leer_historial():
    if not os.path.exists(HISTORIAL_FILE):
        return "No hay registros en el historial todavía."
    with open(HISTORIAL_FILE, "r", encoding="utf-8") as f:
        return f.read()

def generar_evento_llamada_simulado():
    """Genera datos simulados de llamadas entrantes para probar el servicio en segundo plano."""
    escenarios = [
        ("+5491177778888", "Le llamamos del departamento de promociones para ofrecerle...", 0.35),
        ("mama", "hola hijo, cómo estás?", 1.2),
        ("+5493819990000", "eh... hola, hablo con el titular de la línea?", 1.4),
        ("+5491100001111", "Estimado cliente su cuenta requiere confirmacion urgente", 0.4)
    ]
    return random.choice(escenarios)