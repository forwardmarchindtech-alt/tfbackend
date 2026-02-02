from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class PlotRequest(BaseModel):
    plot_description: str

@app.get("/")
def home():
    return {"message": "Backend is running correctly"}

@app.post("/generate")
def generate_design(request: PlotRequest):
    return {
        "plot_received": request.plot_description,
        "image_url": "https://images.unsplash.com/photo-1505691938895-1758d7feb511"
    }
