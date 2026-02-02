from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os

app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP, allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class PlotRequest(BaseModel):
    plot_description: str

# Health check
@app.get("/")
def home():
    return {"message": "Backend is running correctly"}

# Generate AI image endpoint
@app.post("/generate")
def generate_design(request: PlotRequest):
    prompt = (
        request.plot_description +
        " realistic floor plan, exterior and interior design, professional architectural style, high quality"
    )

    try:
        # Call OpenAI DALL·E API
        response = openai.Image.create(
            prompt=prompt,
            n=1,               # number of images
            size="512x512"     # image size
        )

        image_url = response['data'][0]['url']  # URL returned by OpenAI

        return {
            "plot_received": request.plot_description,
            "image_url": image_url
        }

    except Exception as e:
        return {"error": str(e)}
