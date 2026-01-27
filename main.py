from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from io import BytesIO
from PIL import Image
import base64

app = FastAPI()

# Allow requests from your frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For MVP, allow all
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hugging Face API token (replace with your own)
HF_TOKEN = "YOUR_HUGGING_FACE_API_TOKEN"

# Function to call Hugging Face API
def generate_image(prompt):
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    API_URL = "https://api-inference.huggingface.co/models/gsdf/Counterfeit-V2.5"
    
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Hugging Face returns bytes
    image_bytes = response.content
    img = Image.open(BytesIO(image_bytes))
    
    # Convert to base64 string to send to frontend
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{img_str}"

# API Endpoint
@app.post("/generate")
def generate_design(plot_size: str = Form(...), style: str = Form(...), facing: str = Form(...)):
    # Create prompts
    floor_prompt = f"2D architectural floor plan, top-down, {plot_size} plot, 2BHK, clean lines"
    interior_prompt = f"{style} Indian interior design, living room, realistic lighting"
    exterior_prompt = f"{style} Indian house exterior, front elevation, {plot_size} plot, realistic rendering"
    
    # Generate images
    floor_img = generate_image(floor_prompt)
    interior_img = generate_image(interior_prompt)
    exterior_img = generate_image(exterior_prompt)
    
    # Simple Vastu logic
    vastu_score = 85 if facing in ["East", "North"] else 70
    
    return {
        "floor_plan": floor_img,
        "interior": interior_img,
        "exterior": exterior_img,
        "vastu_score": vastu_score
    }
