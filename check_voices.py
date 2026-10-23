import requests

# Paste your API Key here
API_KEY = "40fd4ec864c4787fc9d8e22fb9d183762c30d8f584b0d2c3ccfc7bd1e739da75"

url = "https://api.elevenlabs.io/v1/voices"
headers = {"xi-api-key": API_KEY}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    voices = response.json()['voices']
    print("\n--- YOUR FREE VOICE IDs ---")
    for voice in voices:
        print(f"Name: {voice['name']} | ID: {voice['voice_id']}")
else:
    print(f"Error: {response.text}")