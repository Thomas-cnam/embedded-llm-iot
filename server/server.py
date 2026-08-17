import serial
import requests
import json
import time

PORT = "COM6"
BAUD = 115200

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"

historique = []

def ask_ollama(temp, lum):
    prompt = f"""Tu es un système de détection d'anomalies IoT, par rapport à l'historique,
remonte une anomalie (true) s'il y a des changements significants entre la nouvelle température ou nouvelle luminosité :

Historique récent : {historique}
Nouvelle mesure : température={temp}°C, luminosité={lum} lux.
Réponds UNIQUEMENT avec un objet JSON valide suivant ce format, sans aucun texte avant ou après :
{{"anomalie": True or False, "message": ~explication courte~}}
"""
    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2,
            "num_predict": 150
        }
    })
    try:
        resultat = r.json()
        jugement = json.loads(resultat["response"])
        return jugement
    
        if "anomalie" not in jugement or "message" not in jugement:
            raise ValueError("Réponse incomplète")
        
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
            
            response = "ANOMALIE:1" if jugement["anomalie"] else "ANOMALIE:0"
            print(response)
            ser.write((response + "\n").encode("utf-8"))
            ser.flush()

if __name__ == "__main__":
    main()