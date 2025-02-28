from fastapi import FastAPI, HTTPException
import jwt
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import bcrypt
import uvicorn
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware

# Load biến môi trường
load_dotenv()

# Khởi tạo FastAPI
app = FastAPI()

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Kết nối MongoDB
MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI không được tìm thấy trong biến môi trường!")

try:
    client = MongoClient(MONGO_URI)
    db = client["mydatabase"]
    users_collection = db["users"]
except Exception as e:
    raise ValueError(f"Lỗi kết nối MongoDB: {e}")

# Load SECRET_KEY
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY không được tìm thấy trong biến môi trường!")

# Schema dữ liệu người dùng
class UserRegister(BaseModel):
    fullname: str
    email: str
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Hàm hash password
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

# Hàm kiểm tra password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        print("🔹 Kiểm tra mật khẩu:", plain_password)
        print("🔹 Mật khẩu hash:", hashed_password)

        # Kiểm tra xem hashed_password có bị mất ký tự không
        if not hashed_password.startswith("$2b$"):
            print("⚠️ Mật khẩu hash không hợp lệ!")
            return False

        result = bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        print("🔹 Kết quả kiểm tra:", result)
        return result
    except Exception as e:
        print("❌ Lỗi khi kiểm tra mật khẩu:", e)
        return False


# Hàm tạo JWT token
def create_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")

# API Đăng ký người dùng
@app.post("/auth/register")
async def register(user: UserRegister):
    print("Dữ liệu từ frontend:", user.dict())  # In dữ liệu nhận được từ frontend

    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email đã tồn tại!")
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username đã tồn tại!")

    hashed_password = hash_password(user.password)
    
    new_user = {
        "fullname": user.fullname,
        "email": user.email,
        "username": user.username,
        "password": hashed_password
    }
    users_collection.insert_one(new_user)
    
    return {"message": "Đăng ký thành công!"}


# API Đăng nhập người dùng
@app.post("/auth/login")
async def login(user: UserLogin):
    print("Dữ liệu từ frontend:", user.dict()) 
    db_user = users_collection.find_one({"username": user.username})
    print("db_userrrrrrrrrrrrrrrrrrr:", user.password, db_user["password"])
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Sai tài khoản hoặc mật khẩu!")

    token = create_token({"username": db_user["username"], "email": db_user["email"]})
    return {"token": token, "username": db_user["username"], "fullname": db_user["fullname"]}
# app.include_router(router, prefix="/api")

# @app.get("/")
# async def root():
#     return {"message": "Backend is running!"}

# # Cho phép frontend truy cập API từ bất kỳ nguồn nào (CORS)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Cần đổi thành URL frontend nếu deploy thực tế
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id, "name": f"Item {item_id}"}
# Chạy server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
    
import secrets
print(secrets.token_hex(32))

