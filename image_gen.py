import requests
import base64
import os
import urllib.parse
from config import GOOGLE_API_KEY # Keeping for fallback if user switches back

# Local Stable Diffusion URL
# The user's setup runs on port 7860
SD_API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

def generate_image(prompt: str, output_path: str):
    """
    Generates an image using Local Stable Diffusion WebUI API.
    """
    print(f"Generating image via Local SD for: '{prompt[:30]}...'")
    
    payload = {
        "prompt": prompt,
        "negative_prompt": "ugly, low quality, blurry, watermark",
        "steps": 20,
        "width": 512, # CPU friendly resolution
        "height": 768, # Shorts aspect ratio
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M Karras"
    }
    
    try:
        response = requests.post(SD_API_URL, json=payload, timeout=120) # Long timeout for CPU
        response.raise_for_status()
        data = response.json()
        
        if "images" in data and data["images"]:
            b64_data = data["images"][0]
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(b64_data))
            print(f"Local SD Image saved to {output_path}")
            return True
        else:
            print("Local SD response invalid.")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Local Stable Diffusion.")
        print("Please ensure 'webui-user.bat' is running in 'stable-diffusion-webui' folder.")
    except Exception as e:
        print(f"Local SD Gen Failed: {e}")
        
    # Fallback to Placeholder
    print("Falling back to Placeholder...")
    try:
        snippet = urllib.parse.quote(prompt[:30])
        fallback_url = f"https://placehold.co/512x768/222222/EEEEEE/png?text={snippet}"
        headers_ua = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(fallback_url, headers=headers_ua, timeout=30)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Placeholder image saved to {output_path}")
        return True
    except Exception as e2:
        print(f"Even fallback failed: {e2}")
        return False

if __name__ == "__main__":
    generate_image("A cyberpunk city vertical", "test_local_sd.png")