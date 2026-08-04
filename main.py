from fastapi import FastAPI

app = FastAPI(
    title="ClinicCore"
)

@app.get("/")
def home():
    return {"status": "ClinicCore running"}
