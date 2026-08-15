import serial
import requests
import json
import time

PORT = "COM6"   # ou "COM3" sous Windows
BAUD = 115200

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

historique = []

def ask_ollama(temp, lum):
    prompt = f"""Tu es un système de détection d'anomalies IoT.
Historique récent : {historique}
Nouvelle mesure : température={temp}°C, luminosité={lum} lux.
Réponds UNIQUEMENT en JSON strict : {{"anomalie": true/false, "message": "explication courte"}}
"""
    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    })
    try:
        return json.loads(r.json()["response"])
    except Exception:
        return {"anomalie": False, "message": "erreur IA"}

def main():
    ser = serial.Serial(PORT, BAUD, timeout=2)
    print("Connecté à l'ESP32 sur", PORT)

    while True:
        ligne = ser.readline().decode("utf-8", errors="ignore").strip()
        if ligne.startswith("DATA;"):
            try:
                _, temp_str, lum_str = ligne.split(";")
                print("lum: " + lum_str)
                print("temp: " + temp_str)
                temp, lum = float(temp_str), float(lum_str)
            except ValueError:
                print("unexpected value from captor")
                continue

            historique.append({"temperature": temp, "luminosite": lum})
            if len(historique) > 20:
                historique.pop(0)

            jugement = ask_ollama(temp, lum)
            print("Jugement IA:", jugement)
            
            if not jugement or jugement.len() == 0:
                print("json not sended")
            else:
                response = "ANOMALIE:1" if jugement["anomalie"] else "ANOMALIE:0"
                print(response)
                ser.write(response.encode("utf-8"))

if __name__ == "__main__":
    main()