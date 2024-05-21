

from typing import Union
import logging
import json
import hashlib
import hmac

from fastapi import FastAPI
from fastapi import (FastAPI, Depends, Request, HTTPException, BackgroundTasks)


logging.basicConfig(encoding='utf-8',
                    level=logging.INFO,
                    format='%(levelname)s-%(message)s'
                    )

logger = logging.getLogger("test")

logger.setLevel(logging.INFO)

logger.debug("START")
logger.info("START")

app = FastAPI()


def check_jira_signature(
        secret: str="It's a Secret to Everybody",
        payload: str="Hello World!",
        given_signature: str="sha256=a4771c39fbe90f317c7824e83ddef3caae9cb3d976c214ace1f2937e133263c9"
        ):

    #secret = "It's a Secret to Everybody"
    #payload = "Hello World!"
    #given_signature = "sha256=a4771c39fbe90f317c7824e83ddef3caae9cb3d976c214ace1f2937e133263c9"

    hash_object = hmac.new(
        secret.encode("utf-8"),
        msg=payload.encode("utf-8"),
        digestmod=hashlib.sha256,
    )
    calculated_signature = "sha256=" + hash_object.hexdigest()

    if not hmac.compare_digest(calculated_signature, given_signature):
        print(
            "Signatures do not match\nExpected signature:"
            f" {calculated_signature}\nActual: signature: {given_signature}"
        )
    else:
        print("Signatures match")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/webhooks/new_ticket")
async def new_ticket_handler(req: Request):
    signature = req.headers.get("X-Hub-Signature")


    body = await req.body()
    print("$$$$$$ bode=", body)
    json_body = await req.json()
    print("============")
    print(json.dumps(json_body))
    #logger.info(b)
    print("============")

    print("signature:", signature, ":ebd signature")

    check_jira_signature(
        secret="IP5CblG2j0niQwvNSMvU",
        payload=json.dumps(json_body),
        given_signature=signature
        )


    check_jira_signature(
        secret="IP5CblG2j0niQwvNSMvU",
        payload=body,
        given_signature=signature
        )

    return "hello"


# 127.0.0.1:8000/webhooks/new_ticket
# https://environmental-ainsley-v3-engineering-655c7dc2.koyeb.app/webhooks/new_ticket

"""
curl -X POST \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  -d '{"param0":"pradeep"}' \
  "127.0.0.1:8000/webhooks/new_ticket"
  
curl -X POST \
  -H "Content-type: application/json" \
  -H "Accept: application/json" \
  -d '{"param0":"pradeep"}' \
  "https://environmental-ainsley-v3-engineering-655c7dc2.koyeb.app/webhooks/new_ticket"
"""