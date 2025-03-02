import jwt
import os
import bcrypt
import uvicorn
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from flask import Flask, jsonify, request # type: ignore
from flask_cors import CORS # type: ignore
from pydantic import BaseModel
from AutoReportX import run_gradio #Import hànm từ AutoReportX
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv

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
    collection = db["reports"]
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
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Sai tài khoản hoặc mật khẩu!")

    token = create_token({"username": db_user["username"], "email": db_user["email"]})
    return {"token": token, "username": db_user["username"], "fullname": db_user["fullname"]}


# Lấy thông tin tài khoản
@app.route("/api/user/profile", methods=["GET"])
def get_profile():
    token = request.headers.get("Authorization")
    if not token or token != "Bearer your-token-here":
        return jsonify({"error": "Unauthorized"}), 401

    user_id = "mock_user_id"  # Xác định user từ token trong thực tế

    # Dữ liệu user mock (thay bằng truy vấn database)
    user = {
        "fullname": "Nguyễn Văn A",
        "email": "nguyenvana@example.com",
        "username": "nguyenvana",
        "avatar": "/uploads/avatar1.jpg"
    }

    return jsonify({"user": user})


# Cập nhật thông tin tài khoản

@app.route("/api/user/profile", methods=["PUT"])
def update_profile():
    token = request.headers.get("Authorization")
    if not token or token != "Bearer your-token-here":
        return jsonify({"error": "Unauthorized"}), 401

    user_id = "mock_user_id"

    fullname = request.form.get("fullname")
    email = request.form.get("email")
    password = request.form.get("password")
    avatar = request.files.get("avatar")

    user = {
        "fullname": fullname,
        "email": email,
        "username": "nguyenvana",
    }

    if avatar:
        filename = secure_filename(avatar.filename)
        avatar.save(os.path.join("uploads", filename))
        user["avatar"] = f"/uploads/{filename}"

    return jsonify({"user": user})


# Gọi hàn từ AutoReportX.py 

class QueryRequest(BaseModel):
    user_query: str
    iteration_limit: int = 5

@app.post("/predict/")
async def predict(request: QueryRequest):
    try:
        # Gọi hàm từ AutoReportX.py
        result = run_gradio(request.user_query, request.iteration_limit)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__": 
    # Chạy Server
    uvicorn.run(app, host="0.0.0.0", port=5000)