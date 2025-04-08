import requests

def call_generate_schema_api(prompt: str) -> str:
    url = "http://127.0.0.1:8000/generate-schema"
    payload = {
        "instruction": prompt
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["schema"]
    except Exception as e:
        print("Error calling /generate-schema:", e)
        return ""