import json
import os
import pickle
from typing import List
import time

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

PATH = "/home/xatier/.cache/chromium-tabs"


class Payload(BaseModel):
    data: str


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
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
    with open(PATH, "wb") as f:
        pickle.dump(j, f)


def load_payload() -> List:
    with open(PATH, "rb") as f:
        j = pickle.load(f)
    return j


@app.get("/load")
def load() -> List:
    print(f'/load {time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())}')
    j = load_payload()
    print_payload(j)
    return j


@app.post("/save", status_code=status.HTTP_201_CREATED)
def save(payload: Payload) -> None:
    print(f'/save {time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())}')
    j = json.loads(payload.data)
    print_payload(j)
    move_saved()
    save_payload(j)
    print(f'/save {time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime())}')
