import serial
import requests
import json
import time

PORT = "COM3"
BAUD = 115200

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "phi4-mini"

history = []

def ask_ollama(lum):
    prompt = f"""You are a AI anomaly detection system for the luminosity of the room,
compare the average of the recent history to the new value sent to you, return an anomaly if there are significant change with the sent value (~20%)
recent history : {history}
new measurement : luminosity={lum} lux.
answer ONLY   with a valid JSON object following this format, without text before or after :
{{"anomaly": True or False, "message": ~short explanation~}}
"anomaly" should be true if you detect significant change in data, else "anomaly" should be false
"""

    r = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2,
            "num_predict": 150,
            "num_ctx": 2048,
            "top_p": 0.9
        }
    })
    try:
        resultat = r.json()
        jugement = json.loads(resultat["response"])
        return jugement
    
        if "anomaly" not in jugement or "message" not in jugement:
            raise ValueError("Réponse incomplète")
        
    except Exception:
        return {"anomaly": False, "message": "erreur AI"}

def main():
    ser = serial.Serial(PORT, BAUD, timeout=2)
    print("Conection to ESP32 on", PORT)

    while True:
        ligne = ser.readline().decode("utf-8", errors="ignore").strip()
        if ligne.startswith("DATA;"):
            try:
                _, lum_str, empty = ligne.split(";")
                print("lum: " + lum_str)
                lum = float(lum_str)
            except ValueError:
                print("unexpected value from captor")
                continue
            
            #history 
            history.append({"luminosity": lum})
            if len(history) > 20:
                history.pop(0)
            
            #ask AI
            jugement = ask_ollama(lum)
            print("Jugement AI:", jugement)
            
            #Send answer to ESP32
            response = "ANOMALY:1" if jugement["anomaly"] else "ANOMALY:0"
            ser.write((response + "\n").encode("utf-8"))
            ser.flush()

if __name__ == "__main__":
    main()