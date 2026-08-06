import json
import os
from typing import List
import time

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

PATH = "/home/xatier/.cache/chromium-tabs"


class Payload(BaseModel):
    data: str


API_TOKEN = os.environ.get("TAB_MANAGER_API_TOKEN", "")

if not API_TOKEN:
    raise RuntimeError("TAB_MANAGER_API_TOKEN environment variable must be set")


def verify_token(x_api_token: str = Header(...)):
    if x_api_token != API_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API token")


ALLOWED_ORIGINS = os.environ.get("TAB_MANAGER_ALLOWED_ORIGINS", "").split(",")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=['GET', 'POST'],
    allow_headers=['x-api-token', 'content-type'],
)

console = Console()


def print_payload(j: List) -> None:
    table = Table(
        "Window",
        "Title",
        "URL",
        show_header=True,
        header_style="bold magenta"
    )

    for window in j:
        for tab in window['tabs']:
            table.add_row(str(window["win"]), tab["title"], tab["url"])

    console.print(table)

def move_saved() -> None:
    os.rename(PATH, f'{PATH}.{int(time.time())}')

def save_payload(j: List) -> None:
    with open(PATH, "w") as f:
        json.dump(j, f)


def load_payload() -> List:
    with open(PATH, "r") as f:
        j = json.load(f)
    return j


@app.get("/load", dependencies=[Depends(verify_token)])
def load() -> List:
    print(f'/load {time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())}')
    j = load_payload()
    print_payload(j)
    return j


@app.post("/save", status_code=status.HTTP_201_CREATED, dependencies=[Depends(verify_token)])
def save(payload: Payload) -> None:
    print(f'/save {time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())}')
    j = json.loads(payload.data)
    print_payload(j)
    move_saved()
    save_payload(j)
    print(f'/save {time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())}')
