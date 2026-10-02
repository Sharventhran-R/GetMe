from fastapi import FastAPI

app = FastAPI(title="Community Missing Item & Asset Tracker")

@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok"}
