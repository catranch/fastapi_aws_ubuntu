from uuid import uuid4
from fastapi import FastAPI, HTTPException 
import os
import json
from pydantic import BaseModel
from typing import Optional, Literal
from fastapi.encoders import jsonable_encoder

app = FastAPI()

class Book(BaseModel):
	name: str
	price: float
	genre: Literal["fiction","non-fiction"]
	book_id: Optional[str] = uuid4().hex

BOOKS_FILE = "books.json"
BOOK_DATABASE = []

if os.path.exists(BOOKS_FILE):
	with open(BOOKS_FILE,"r") as f:
		BOOK_DATABASE = json.load(f)

@app.get("/")
def root():
    return {"Message": "Ikea World"}

@app.get("/list-books")
async def list_books():
	return {"books": BOOK_DATABASE}

@app.get("/book-by-index/{index}")
async def book_by_index(index: int):
	if index < 0 or index >= len(BOOK_DATABASE):
		raise HTTPException(404, f"Index {index} not working")
	else:
		return {"book": BOOK_DATABASE[index]}

@app.post("/add-book")
async def add_book(book: Book):
	book.book_id = uuid4().hex
	json_book = jsonable_encoder(book)
	BOOK_DATABASE.append(json_book)
	with open(BOOKS_FILE,"w") as f:
		json.dump(BOOK_DATABASE, f)
	return {"message": f"Book {book} added"}

@app.post("/new-name")
async def new_name():
	return "new name"


#this would be inventory of item or location
#location would have shelf, room, house, city
#house would have a model 
#verbs to move things around
#goal - is to find the tool or the memory to move forward

