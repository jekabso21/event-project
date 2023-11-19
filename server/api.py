import sys

import mariadb
from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="GKCi651wSa3LutHX",
        host="127.0.0.1",
        port=3306,
        database="party-event"

    )
    print("Connected to MariaDB Platform")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()


class UserData(BaseModel):
    name: str
    email: str
    group: str


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


posts = []

@app.post("/join/adduser")
async def add_user(data: UserData):
    qr_data = hashlib.md5(data.name.encode('UTF-8'))
    qr_data = qr_data.hexdigest()
    try:
        cur.execute("INSERT INTO users (name, email, `group`, qrcode) VALUES (%s, %s, %s, %s)", (data.name, data.email, data.group, 'lel'))
        conn.commit()
    except mariadb.Error as e:
        print(f"Error: {e}")

    return data


# @app.post("/post", response_model=UserPost)
# async def create_post(post: UserPost):
#     posts.append(post)
#     return post
#
#
# @app.get("/posts", response_model=list[UserPost])
# async def get_all_posts():
#     return posts

@app.delete("/posts/{post_id}")
async def delete_post(post_id: int):
    posts.pop(post_id - 1)
    return {}
