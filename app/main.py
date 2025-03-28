from fastapi import FastAPI

app = FastAPI(title="Web Crawler API")

@app.get("/")
def read_root():
    return {"message": "Creepy crawler app"}