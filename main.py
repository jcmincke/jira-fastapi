from typing import Union

from fastapi import FastAPI
from fastapi import (FastAPI, Depends, Request, HTTPException, BackgroundTasks)

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.get("/webhooks/new_ticket")
async def new_ticket_handler(req: Request):

    b = await req.json()
    print("============")
    print(b)
    print("============")

    return "hello"


# 127.0.0.1:8000/webhooks/new_ticket
# https://environmental-ainsley-v3-engineering-655c7dc2.koyeb.app/webhooks/new_ticket

"""
curl -X GET \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  -d '{"param0":"pradeep"}' \
  "127.0.0.1:8000/webhooks/new_ticket"
  
"""