from uuid import uuid4
from fastapi import FastAPI, HTTPException 
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from fastapi.encoders import jsonable_encoder

app = InventoryFastAPI()

class Book(BaseModel):
	name: str
	price: float
	genre: Literal["house","garage"]
	book_id: Optional[str] = uuid4().hex

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
async def list_books():
	return {"books": ITEM_DATABASE}

@app.get("/book-by-index/{index}")
async def book_by_index(index: int):
	if index < 0 or index >= len(ITEM_DATABASE):
		raise HTTPException(404, f"Index {index} not working")
	else:
		return {"book": ITEM_DATABASE[index]}

@app.post("/add-book")
async def add_book(book: Book):
	book.book_id = uuid4().hex
	json_book = jsonable_encoder(book)
	ITEM_DATABASE.append(json_book)
	with open(ITEMS_FILE,"w") as f:
		json.dump(ITEM_DATABASE, f)
	return {"message": f"Book {book} added"}

@app.post("/new-name")
async def new_name():
	return "new name"


#this would be inventory of item or location
#location would have shelf, room, house, city
#house would have a model 
#verbs to move things around
#goal - is to find the tool or the memory to move forward

