from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="REST API Starter")
DB: Dict[int, dict] = {}
_id = 0

class Item(BaseModel):
    name: str
    price: float

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/items")
def create_item(item: Item):
    global _id
    _id += 1
    DB[_id] = item.dict()
    return {"id": _id, **DB[_id]}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": item_id, **DB[item_id]}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    DB[item_id] = item.dict()
    return {"id": item_id, **DB[item_id]}

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    del DB[item_id]
    return {"deleted": item_id}

@app.post("/predict")
def predict(features: dict):
    # Dummy "model": sum numeric values
    score = sum(v for v in features.values() if isinstance(v, (int, float)))
    return {"score": score}
