# Gateway

This folder contain the Python script that are to be run locally and serve to gateway between the ESP32 and the LLM.

The gateway do :

- Read peripherals value from PC port
- Log the value from ESP32
- send an API request to LLM with the designated prompt
- log LLM answer
- Log a short LLM answer to the port depending if the anomaly is detected 

for now the prompt sent to the LLM was :

You are a AI anomaly detection system for the luminosity of the room,
compare the average of the recent history to the new value sent to you, return an anomaly if there are significant change with the sent value (~20%)
recent history : {history}
new measurement : luminosity={lum} lux.
answer ONLY   with a valid JSON object following this format, without text before or after :
{{"anomaly": True or False, "message": ~short explanation~}}
"anomaly" should be true if you detect significant change in data, else "anomaly" should be false

note that the suggested deviation was ~20% and can be modified later