# from fastapi import APIRouter, HTTPException
# from pymongo import MongoClient
# from pydantic import BaseModel




# router = APIRouter()

# client = MongoClient("mongodb://localhost:27017/")
# db = client["mydatabase"]
# collection = db["mycollection"]

# class Item(BaseModel):
#     name: str
#     value: str

# @router.post("/mongodb/items/")
# async def create_item(item: Item):
#     result = collection.insert_one(item.dict())
#     return {"inserted_id": str(result.inserted_id)}

# @router.get("/mongodb/items/{name}")
# async def read_item(name: str):
#     item = collection.find_one({"name": name})
#     if not item:
#         raise HTTPException(status_code=404, detail="Item not found")
#     item["_id"] = str(item["_id"])
#     return item

# @router.delete("/mongodb/items/{name}")
# async def delete_item(name: str):
#     result = collection.delete_one({"name": name})
#     if result.deleted_count == 0:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"deleted": True}