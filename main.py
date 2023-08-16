from uuid import uuid4
from fastapi import FastAPI, HTTPException 
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class ITEM(BaseModel):
	name: str
	price: float
	genre: Literal["house","garage"]
	item_id: Optional[str] = uuid4().hex

ITEMS_FILE = "items.json"
ROOMS_FILE = "rooms.json"
ITEM_DATABASE = []

#if doesn't exist then create it
if os.path.exists(ITEMS_FILE):
	with open(ITEMS_FILE,"r") as f:
		ITEM_DATABASE = json.load(f)

@app.get("/")
def root():
    return {"Message": "Ikea Inventory World"}

@app.get("/list-items")
async def list_items():
	return {"books": ITEM_DATABASE}

@app.get("/book-by-index/{index}")
async def book_by_index(index: int):
	if index < 0 or index >= len(ITEM_DATABASE):
		raise HTTPException(404, f"Index {index} not working")
	else:
		return {"book": ITEM_DATABASE[index]}

@app.post("/add-item")
async def add_item(book: ITEM):
	book.item_id = uuid4().hex
	json_book = jsonable_encoder(book)
	ITEM_DATABASE.append(json_book)
	with open(ITEMS_FILE,"w") as f:
		json.dump(ITEM_DATABASE, f)
	return {"message": f"Item {book} added"}

@app.post("/new-name")
async def new_name():
	return "new name"

@app.get("/item-by-index/{index}")
async def item_by_index(index: int):
	if index < 0 or index >= len(ITEM_DATABASE):
		raise HTTPException(404, f"Index {index} not working")
	else:
		return {"book": ITEM_DATABASE[index]}

#ikea products
#bed in Riverside
#dresser in Potsdam
#mattress in Haarlem

#this would be inventory of item or location
#location would have shelf, room, house, city
#house would have a model 
#goal - is to find the item to complete project
#for example - missing screwdriver or power tool

