import sys

import mariadb
from fastapi import FastAPI
from pydantic import BaseModel
from cryptography.fernet import Fernet
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz



# function to generate a key and save it into a file
def write_key():
    key = Fernet.generate_key()
    with open('key.key', 'wb') as key_file:
        key_file.write(key)

# function to load the key from the current directory named 'key.key'
def load_key():
    return open('key.key', 'rb').read()

write_key()
key = load_key()

# initialization of the Fernet class
fernet = Fernet(key)

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="admin",
        host="159.89.17.59",
        port=3306,
        database="party-event"

    )
    print("Connected to MariaDB Platform")
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

origins = [
    "http://0.0.0.0:3000",  # Change this according to your needs, or simply use "*" but consider the security implications
]


print(cur.execute("SELECT * FROM admin"))


class UserPost(BaseModel):
    name: str
    email: str
    group: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.post("/users/adduser", response_model=UserPost)
async def create_post(post: UserPost):
    posts.append(post)
    text = post.name
    qr_code = fernet.encrypt(text.encode())
    print(f'Encrypted: {qr_code}')
    time = datetime.now(pytz.timezone('Europe/Riga'))
    print(time)

    cur.execute("INSERT INTO users (name, email, `group`, qr, registered) VALUES (?, ?, ?, ?, ?)", (post.name, post.email, post.group, qr_code, time))
    conn.commit()
    return post

# # decrypting the string
# dec_message = fernet.decrypt(enc_message).decode()
# print(f'Decrypted: {dec_message}')

@app.get("/users/get/allusers")
async def get_all_posts():
    #Get all the users from the database
    cur.execute("SELECT name, email, registered, scanned FROM users")
    users = cur.fetchall()
    users_list = []
    for user in users:
        users_list.append({
            "name": user[0],
            "email": user[1],
            "date": user[2],
            "scanned": user[3]
        })
    return users_list
class Item(BaseModel):
    qrData: str
@app.post("/user/isvalid")
async def read_items(item: Item):
    print(item.qrData)
    #search qr in database
    cur.execute("SELECT * FROM users WHERE qr=?", (item.qrData,))
    qr = cur.fetchone()
    #return name, email, group, registered, scaned
    print(qr)
    if qr is None:
        print("Is Not Valid")
        return {"message": "QR code not found"}
    else:
        print(qr[7])
        return {"name": qr[1], "email": qr[2], "group": qr[3], "registered": qr[5], "scanned": qr[6], "qr": qr[4], "hasguest": qr[7], "isguest": qr[8]}


@app.post("/user/confirm")
async def confirm_user(item: Item):
    #search qr in database
    cur.execute("SELECT * FROM users WHERE qr=?", (item.qrData,))
    qr = cur.fetchone()
    print(qr)
    if qr is None:
        return {"message": "QR code not found"}
    else:
        cur.execute("UPDATE users SET scaned=? WHERE qr=?", (1, item.qrData))
        conn.commit()
        return {"status": "success"}

class Login(BaseModel):
    email: str
    password: str
@app.post("/admin/login")
async def admin_login(login: Login):
    print(login)
    cur.execute("SELECT * FROM admin WHERE username=?", (login.email,))
    auth = cur.fetchone()
    print(auth)
    if auth is None:
        print("error")
        return {"status": "error"}
    else:
        if login.password == auth[3]:
            return {"status": "success"}
        else:
            print("error")
            return {"status": "error"}
