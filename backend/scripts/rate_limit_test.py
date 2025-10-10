import requests
import time

for i in range(12):
    response = requests.get("http://localhost:8000/api/health")
    print(f"Request {i+1}: Status {response.status_code}")
    time.sleep(1) # Send requests faster than the window to trigger limit