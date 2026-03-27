import requests
import base64
import os
import urllib.parse
from PIL import Image, ImageDraw, ImageFont
import time

from config import SD_LOCAL_URL

def create_local_placeholder(text: str, output_path: str):
    """Creates a local image with text using Pillow as a final fallback."""
    try:
        # 1080x1920 (Shorts format)
        img = Image.new('RGB', (1080, 1920), color=(34, 34, 34))
        d = ImageDraw.Draw(img)
        
        try:
            # Try to find a font, fallback to default
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
            
        text_to_draw = text[:50] + "..." if len(text) > 50 else text
        d.text((50, 960), text_to_draw, fill=(238, 238, 238), font=font)
        d.text((50, 1050), "(Local Checkpoint Fallback)", fill=(150, 150, 150), font=font)
        
        img.save(output_path)
        print(f"Local Pillow placeholder saved to {output_path}")
        return True
    except Exception as e:
        print(f"Pillow Fallback Failed: {e}")
        return False

def generate_image(prompt: str, output_path: str):
    """
    Generates an image using Local Stable Diffusion API.
    Falls back to Placehold.co, then to Local Pillow.
    """
    print(f"Generating image for: '{prompt[:100]}...'")
    
    # 1. Try Local Stable Diffusion
    sd_url = f"{SD_LOCAL_URL}/sdapi/v1/txt2img"
    payload = {
        "prompt": prompt,
        "negative_prompt": "blurry, low quality, distorted, watermark, text",
        "steps": 20,
        "width": 512,
        "height": 512,
        "cfg_scale": 7,
        "sampler_name": "Euler a"
    }
    
    try:
        # Large timeout because CPU generation takes time
        print(f"Connecting to Local SD at {SD_LOCAL_URL} (CPU Mode - this may take 3-5 mins)...")
        response = requests.post(sd_url, json=payload, timeout=600)
        
        if response.status_code == 200:
            data = response.json()
            if "images" in data and len(data["images"]) > 0:
                img_data = base64.b64decode(data['images'][0])
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"Local Stable Diffusion image saved to {output_path}")
                return True
        print(f"Local SD Failed (Status {response.status_code}): {response.text[:200]}")
    except Exception as e:
        print(f"Local SD Request Failed: {e}")
        
    # 2. Try Placehold.co (Online Placeholder)
    print("Falling back to Placehold.co...")
    try:
        snippet = urllib.parse.quote(prompt[:30])
        fallback_url = f"https://placehold.co/1080x1920/222222/EEEEEE/png?text={snippet}"
        headers_ua = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(fallback_url, headers=headers_ua, timeout=10)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Placehold.co image saved to {output_path}")
        return True
    except Exception as e:
        print(f"Placehold.co Failed: {e}")
        
    # 3. Final Local Fallback (Pillow)
    return create_local_placeholder(prompt, output_path)

if __name__ == "__main__":
    # Test generation
    generate_image("A futuristic city in the clouds, digital art", "test_pipeline.jpg")