import requests
import base64
import os
import urllib.parse
from PIL import Image, ImageDraw, ImageFont

# Local Stable Diffusion URL
SD_API_URL = "http://127.0.0.1:7860/sdapi/v1/txt2img"

def create_local_placeholder(text: str, output_path: str):
    """Creates a local image with text using Pillow."""
    try:
        img = Image.new('RGB', (1080, 1920), color=(34, 34, 34))
        d = ImageDraw.Draw(img)
        
        # Try to use a default font
        try:
            # On Windows, Arial is usually available
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
            
        # Draw text in the middle
        text_to_draw = text[:50] + "..." if len(text) > 50 else text
        d.text((50, 960), text_to_draw, fill=(238, 238, 238), font=font)
        d.text((50, 1050), "(Local Fallback)", fill=(150, 150, 150), font=font)
        
        img.save(output_path)
        print(f"Local Pillow placeholder saved to {output_path}")
        return True
    except Exception as e:
        print(f"Pillow Fallback Failed: {e}")
        return False

def generate_image(prompt: str, output_path: str):
    """
    Generates an image using Local Stable Diffusion WebUI API.
    Falls back to Placehold.co, then to Local Pillow.
    """
    print(f"Generating image for: '{prompt[:30]}...'")
    
    # 1. Try Local SD
    payload = {
        "prompt": prompt,
        "negative_prompt": "ugly, low quality, blurry, watermark",
        "steps": 20,
        "width": 512,
        "height": 768,
        "cfg_scale": 7,
        "sampler_name": "DPM++ 2M Karras"
    }
    
    try:
        response = requests.post(SD_API_URL, json=payload, timeout=5) # Short timeout for check
        response.raise_for_status()
        data = response.json()
        
        if "images" in data and data["images"]:
            b64_data = data["images"][0]
            with open(output_path, "wb") as f:
                f.write(base64.b64decode(b64_data))
            print(f"Local SD Image saved to {output_path}")
            return True
    except:
        pass # Silently fail and go to next
        
    # 2. Try Placehold.co (Online Placeholder)
    try:
        snippet = urllib.parse.quote(prompt[:30])
        fallback_url = f"https://placehold.co/1080x1920/222222/EEEEEE/png?text={snippet}"
        headers_ua = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(fallback_url, headers=headers_ua, timeout=10) # 10s timeout
        response.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Placehold.co image saved to {output_path}")
        return True
    except:
        pass
        
    # 3. Final Local Fallback (Pillow)
    return create_local_placeholder(prompt, output_path)

if __name__ == "__main__":
    generate_image("Test prompt", "test_output.jpg")