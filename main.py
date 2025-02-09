import requests
import os

API_KEY = "-------------------------------------------------------------------"  # Replace with actual key safely

user_prompt = input('Enter prompt: ')

prompt_eng = ['A single right-foot', user_prompt,", side view",", in white background ", ', rubber shoes']

# Step 1: Generate Image
shoe_api = requests.post(
    "https://api.stability.ai/v2beta/stable-image/generate/core",
    headers={
        "authorization": f"{API_KEY}",
         "accept": "image/*"
    },
    files={"none": ''},
    data={
        "prompt": user_prompt + str(prompt_eng),
        "output_format": "webp",
    },
)

# Check if request was successful
if shoe_api.status_code == 200:
    with open("image.png", "wb") as file:
        file.write(shoe_api.content)
    print("Image generated successfully: image.png")
else:
    print("Error generating image:", shoe_api.text)
    raise Exception(shoe_api.text)

# Step 2: Convert Image to 3D Model
try:
    with open("image.png", "rb") as image_file:
        sf3d_api = requests.post(
            "https://api.stability.ai/v2beta/3d/stable-fast-3d",
            headers={
                "authorization": f"{API_KEY}",
                "accept": "model/gltf-binary",
            },
            files={"image": image_file},
        )

    if sf3d_api.status_code == 200:
        with open("shoe.glb", "wb") as file:
            file.write(sf3d_api.content)
        print("3D model generated successfully: shoe.glb")
    else:
        print("Error generating 3D model:", sf3d_api.text)
        raise Exception(sf3d_api.text)

except FileNotFoundError:
    print("Error: image.png not found. Ensure the image generation step was successful.")
    raise


# DISPLAY!
# Define file paths
image_path = "image.png"
glb_path = "shoe.glb"

# Open the image
if os.path.exists(image_path):
    os.startfile(image_path)  # Windows
    # os.system(f"open {image_path}")  # macOS
    # os.system(f"xdg-open {image_path}")  # Linux
    print(f"Opened image: {image_path}")
else:
    print(f"Image file not found: {image_path}")

# Open the 3D model
if os.path.exists(glb_path):
    os.startfile(glb_path)  # Windows
    # os.system(f"open {glb_path}")  # macOS
    # os.system(f"xdg-open {glb_path}")  # Linux
    print(f"Opened 3D model: {glb_path}")
else:
    print(f"3D model file not found: {glb_path}")
