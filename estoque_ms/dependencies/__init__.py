from fastapi import FastAPI

from . import db


def init_app(app: FastAPI) -> None:
    db.init_app()
