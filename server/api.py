import sys

import mariadb
from fastapi import FastAPI
from pydantic import BaseModel

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="GKCi651wSa3LutHX",
        host="15.204.213.220",
        port=3306,
        database="party-event"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

print(cur.execute("SELECT * FROM admin"))


class UserPost(BaseModel):
    name: str
    body: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/join/adduser")
async def add_user():
    return {"message": "User added"}


@app.post("/join/adduser")
async def add_user(req: dict):
    return {"message": "User added", "DATA": "data Hello World"}


posts = []


@app.post("/post", response_model=UserPost)
async def create_post(post: UserPost):
    posts.append(post)
    return post


@app.get("/posts", response_model=list[UserPost])
async def get_all_posts():
    return posts
