from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import base64
import os

app = FastAPI()

# ✅ Allow Netlify frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Utility: convert image → base64
def image_to_base64(path: str):
    with open(path, "rb") as img:
        return "data:image/png;base64," + base64.b64encode(img.read()).decode("utf-8")


@app.post("/generate")
async def generate(
    plot_size: str = Form(...),
    style: str = Form(...),
    facing: str = Form(...)
):
    """
    MVP backend:
    - Returns sample images as Base64
    - Returns vastu score
    """

    # ⚠️ These image files MUST exist in repo
    floor_plan = image_to_base64("floor_plan.png")
    interior = image_to_base64("interior.png")
    exterior = image_to_base64("exterior.png")

    # Simple vastu logic (MVP)
    vastu_map = {
        "East": 90,
        "North": 85,
        "West": 75,
        "South": 70
    }

    vastu_score = vastu_map.get(facing, 80)

    return {
        "floor_plan": floor_plan,
        "interior": interior,
        "exterior": exterior,
        "vastu_score": vastu_score
    }


@app.get("/")
def health_check():
    return {"status": "Backend is running"}
