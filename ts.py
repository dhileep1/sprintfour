import requests
import base64
from config import IMG_ROUTER

def test_image_router():
    url = "https://api.imagerouter.io/v1/openai/images/generations"
    payload = {
      "prompt": "A majestic dragon flying over a futuristic city, cinematic lighting, 8k",
      "model": "test/test"
    }
    headers = {
      "Authorization": f"Bearer {IMG_ROUTER}"
    }

    print("Requesting image from ImageRouter...")
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        print("Success!")
        # Typically image APIs return a URL or b64
        # Adjust based on what imagerouter actually returns
        print(data)
        
        # If it returns a URL:
        if "data" in data and len(data["data"]) > 0:
            img_url = data["data"][0].get("url")
            if img_url:
                print(f"Image URL: {img_url}")
                img_data = requests.get(img_url).content
                with open("test_imagerouter.jpg", "wb") as f:
                    f.write(img_data)
                print("Saved to test_imagerouter.jpg")
    else:
        print(f"Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    test_image_router()