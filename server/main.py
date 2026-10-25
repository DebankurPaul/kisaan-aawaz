from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Kisaan Awaaz is live"}

@app.get("/health")
def health():
    return {"status": "ok"}