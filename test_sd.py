import requests
import base64

def test_local_sd():
    url = "http://127.0.0.1:7860/sdapi/v1/txt2img"
    payload = {
        "prompt": "a beautiful mountain landscape, sdxl style, high resolution",
        "steps": 5,
        "width": 512,
        "height": 512
    }
    
    print("Testing local Stable Diffusion API on http://127.0.0.1:7860...")
    try:
        response = requests.post(url, json=payload, timeout=600)
        if response.status_code == 200:
            print("Success! Image generated.")
            data = response.json()
            # Save the first image
            img_data = base64.b64decode(data['images'][0])
            with open("test_local_sd.png", "wb") as f:
                f.write(img_data)
            print("Saved to test_local_sd.png")
        else:
            print(f"Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_local_sd()
