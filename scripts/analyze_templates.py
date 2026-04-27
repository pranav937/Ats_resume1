import base64
import json
import requests
import os
from pathlib import Path

API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
BASE_DIR = Path(__file__).resolve().parents[1]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

images = ["img1.jpg", "img2.jpg", "img3.jpg"]
results = {}

if not API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY environment variable.")

for img in images:
    path = BASE_DIR / "assets" / "templates" / img
    if not path.exists():
        continue
    
    base64_image = encode_image(path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "google/gemini-2.0-flash-lite-001",
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe the layout of this resume template. Mention the number of columns, colors, typography hierarchy, where the name/header is, and any unique visual elements. Be purely descriptive."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        data = response.json()
        if 'choices' in data:
            results[img] = data['choices'][0]['message']['content']
        else:
            results[img] = json.dumps(data)
    except Exception as e:
        results[img] = str(e)
        
for img, desc in results.items():
    print(f"=== {img} ===")
    print(desc)
    print("\n")