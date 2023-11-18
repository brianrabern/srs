from fastapi import FastAPI
from database import get_all, get_one, post_one, update_one, delete_one


app = FastAPI()


@app.get("/users")
def get_all_users():
    return get_all()


@app.get("/users/{uuid}")
def get_one_thing(uuid: str):
    return get_one(uuid)


@app.post("/users")
def post_one_thing(contact: str):
    return post_one(contact)


@app.put("/users/{uuid}")
def update_one_thing(uuid: str, update_data: dict):
    return update_one(uuid, update_data)


@app.delete("/users/{uuid}")
def delete_one_thing(uuid: str):
    return delete_one(uuid)
