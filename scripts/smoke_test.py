import requests
import time
import sys

BASE_URL = "http://localhost:8001"

def wait_for_server():
    print("Waiting for server to start...")
    for _ in range(15):
        try:
            r = requests.get(BASE_URL, timeout=3)
            if r.status_code == 200:
                print("Server is up!")
                return True
        except requests.exceptions.RequestException:
            time.sleep(1)
    print("Server failed to start.")
    return False

def test_full_loop():
    print("\nTesting Full Simulation Loop...")
    try:
        response = requests.post(f"{BASE_URL}/simulation/full_loop", timeout=10)
        response.raise_for_status()
        data = response.json()
        print("Success!")
        print(f"Mission ID: {data['id']}")
        print(f"Outcome: {data['outcome']}")
        print(f"XP Awarded: {data['xp_awarded']}")
        print("Log:")
        for line in data.get('log', []):
            print(f"  {line}")
    except Exception as e:
        print(f"test_full_loop failed: {e}")

if __name__ == "__main__":
    if wait_for_server():
        test_full_loop()
    else:
        sys.exit(1)
