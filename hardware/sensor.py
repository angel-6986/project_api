import requests
import random
import time
import json

API_URL = "https://project-api-am.onrender.com/api/v1/sensors/data"
def simulate_hardware():
    print("Starting hardware simulation... Press Ctrl+C to stop")

    try:
        while True:
            # fake data
            simulated_temp = round(random.uniform(20.0, 35.5), 2)

            #package data as python directory(acts like json)
            payload = {
                "sensor_id": "ESP32_NODE_01",
                "temperature": simulated_temp,
                "status": "active"
            }
            #send the post request to api
            print(f"Sending data: {payload}...")
            response = requests.post(API_URL, json=payload)

            #print API response
            print(f"Server responded: {response.status_code} - {response.json()}\n")

            #wait 3 seconds for next reading
            time.sleep(3)
        
    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")

if __name__ == "__main__":
    simulate_hardware()