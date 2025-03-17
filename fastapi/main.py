from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello World"}

@app.post("/items/")
def create_item(name: str, price: float):
    return {"name": name, "price": price}

@app.put("/items/{item_id}")
def update_item(item_id: int, name: str, price: float):
    return {"item_id": item_id, "name": name, "price": price}

@app.patch("/items/{item_id}")
def patch_item(item_id: int, name: str = None, price: float = None):
    updated_data = {"item_id": item_id}
    if name is not None:
        updated_data["name"] = name
    if price is not None:
        updated_data["price"] = price
    return updated_data

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted successfully"}