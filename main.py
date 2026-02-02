from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend is running correctly"}

@app.post("/generate")
def generate():
    return {
        "image_url": "https://images.unsplash.com/photo-1505691938895-1758d7feb511"
    }
