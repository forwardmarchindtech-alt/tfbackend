from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import requests
import base64
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load OpenAI API Key from Render secret
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Request model
class PlotRequest(BaseModel):
    plot_description: str

@app.get("/")
def home():
    return {"message": "Backend is running correctly"}

@app.post("/generate")
def generate_design(request: PlotRequest):
    prompt_base = request.plot_description + " realistic professional architectural design, high quality"

    # Types of images to generate
    types = ["Floor Plan", "Exterior", "Interior"]
    result_images = {}

    try:
        for t in types:
            # Customize prompt per type
            prompt = f"{prompt_base}, {t}"
            
            # Call OpenAI DALL·E
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="512x512"
            )
            
            image_url = response['data'][0]['url']
            # Fetch image bytes and convert to base64
            img_data = requests.get(image_url).content
            img_base64 = base64.b64encode(img_data).decode("utf-8")
            
            result_images[t] = img_base64

        return {
            "plot_received": request.plot_description,
            "images": result_images
        }

    except Exception as e:
        return {"error": str(e)}
