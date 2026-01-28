from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import base64
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def image_to_base64(path: str):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as img:
        return "data:image/png;base64," + base64.b64encode(img.read()).decode()


@app.post("/generate")
async def generate(
    plot_size: str = Form(default="30x40"),
    style: str = Form(default="Modern"),
    facing: str = Form(default="East")
):
    try:
        floor_plan = image_to_base64("floor_plan.png")
        interior = image_to_base64("interior.png")
        exterior = image_to_base64("exterior.png")

        vastu_map = {
            "East": 90,
            "North": 85,
            "West": 75,
            "South": 70
        }

        return {
            "floor_plan": floor_plan,
            "interior": interior,
            "exterior": exterior,
            "vastu_score": vastu_map.get(facing, 80)
        }

    except Exception as e:
        return {
            "error": str(e)
        }
