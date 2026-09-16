import time
from logica import procesar_llamada_inteligente

def iniciar_patovica_en_vivo():
    print("--- INICIANDO PATROVICA DIGITAL (ARQUITECTURA MODULAR) ---")
    
    # Simulamos una llamada entrante de un número desconocido
    identificador = "+5491177778888"
    print(f"\n--- Evaluando llamada entrante de: {identificador} ---")
    
    print("[!] El Patovica Digital abrió el canal de voz...")
    inicio = time.time()
    texto_usuario = input(">>> (Simulando tu voz en vivo) Escribí tu respuesta: ")
    fin = time.time()
    
    latencia = round(fin - inicio, 2)
    print(f"Texto analizado: '{texto_usuario}'")
    print(f"Latencia medida: {latencia} segundos")

    # Enviamos los datos al cerebro modular (logica.py)
    resultado = procesar_llamada_inteligente(identificador, texto_usuario, latencia)
    print(f"\nResultado final: {resultado}")
    print("[i] Revisá tu historial local. ¡Módulo separado con éxito!")

if __name__ == "__main__":
    iniciar_patovica_en_vivo()