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
	room: str
	building: Literal["house","garage"]
	description: Optional[str] = None
	city: Literal["Potsdam","Riverside"]
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

@app.get("/get-item/{name}")
async def get_item(name: str):
	new_list = []
	for book in ITEM_DATABASE:
		if book["name"] == name:
			new_list.append(book)
			#return book
	return new_list
	#do some things
	#return the rest of the data, loop for second entry
	#especially location
	#do as local file then upload to db 

@app.post("/add-item")
async def add_item(book: ITEM):
	book.item_id = uuid4().hex
	json_book = jsonable_encoder(book)
	ITEM_DATABASE.append(json_book)
	with open(ITEMS_FILE,"w") as f:
		json.dump(ITEM_DATABASE, f)
	return {"message": f"Item {book} added"}

#this index is it's location in the array
@app.get("/item-by-index/{index}")
async def item_by_index(index: int):
	if index < 0 or index >= len(ITEM_DATABASE):
		raise HTTPException(404, f"Index {index} not working")
	else:
		return {"book": ITEM_DATABASE[index]}

#look up products by item[name] to find an item in the house
#list what's in the house or the location
#list what's needed based on the other location
#for Ikea check delivery location - overlap of dates?

#ikea products
#bed in Riverside
#dresser in Potsdam
#mattress in Haarlem

#this would be inventory of item or location
#location would have shelf, room, house, city
#house would have a model 
#goal - is to find the item to complete project
#for example - missing screwdriver or power tool
