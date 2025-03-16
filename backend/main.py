import jwt
import os
import bcrypt
import uvicorn
import pypandoc
from fastapi.responses import StreamingResponse
from datetime import datetime, timedelta
from fastapi.middleware.cors import CORSMiddleware
from AutoReportX import run_gradio, create_word_file, create_pdf_file #Import hànm từ AutoReportX
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from pymongo import MongoClient
from pydantic import BaseModel
from dotenv import load_dotenv
from bson import ObjectId
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
from fastapi.staticfiles import StaticFiles
#--------------------------------------------------------------------------------

# Tải pandoc tích hợp sẵn
pypandoc.download_pandoc()

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

# ALGORITHM
ALGORITHM = "HS256"

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

    # Kiểm tra email và username đã tồn tại chưa
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email đã tồn tại!")
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="Username đã tồn tại!")

    # Băm mật khẩu
    hashed_password = hash_password(user.password)
    
    new_user = {
        "fullname": user.fullname,
        "email": user.email,
        "username": user.username,
        "password": hashed_password,
    }
    users_collection.insert_one(new_user)
    
    # Tạo Token ngay sau khi đăng ký
    token_data = {"username": user.username, "email": user.email}
    token = create_token(token_data)

    return {
        "message": "Đăng ký thành công!",
        "token": token,
        "username": user.username,
        "fullname": user.fullname,
    }


# API Đăng nhập người dùng
@app.post("/auth/login")
async def login(user: UserLogin):
    
    #In dữ liệu nhận từ frontend
    print("Dữ liệu từ frontend:", user.dict()) 
    
    #Tìm người dùng trong sơ sở dữ liệu
    db_user = users_collection.find_one({"username": user.username})
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Sai tài khoản hoặc mật khẩu!")

    # Tạo Token JWT
    token_data = {"username": db_user["username"], "email": db_user["email"]}
    token = create_token(token_data)

    # Trả về thông tin người dùng và token
    return {
        "token": token,
        "username": db_user["username"],
        "fullname": db_user["fullname"],
    }
    

# Cấu hình OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Hàm giải mã token
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except JWTError as e:
        print("❌ Lỗi giải mã token:", str(e))
        raise HTTPException(status_code=401, detail="Invalid token")
    

# API lấy thông tin người dùng
@app.get("/user/profile")
async def get_user_profile(token: str = Depends(oauth2_scheme)):
    # Giải mã token để lấy username
    username = decode_token(token)
    
    # Tìm thông tin trong MongoDB
    user = users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Trả về thông tin người dùng
    return {
        "fullname": user.get("fullname", ""),
        "email": user.get("email", ""),
        "username": user.get("username", "")
    }

# API cập nhật thông tin người dùng
from fastapi import Request

@app.put("/user/profile")
async def update_user_profile(request: Request, token: str = Depends(oauth2_scheme)):
    try:
        username = decode_token(token)
        user = users_collection.find_one({"username": username})
        if not user:
            raise HTTPException(status_code=404, detail="Người dùng không tồn tại")

        # Nhận dữ liệu từ request JSON
        data = await request.json()
        fullname = data.get("fullname")
        email = data.get("email")
        password = data.get("password")

        update_data = {}
        if fullname:
            update_data["fullname"] = fullname
        if email:
            update_data["email"] = email
        if password:
            hashed_password = hash_password(password)
            print(f"🔹 DEBUG: Mật khẩu mới (chưa hash): {password}")
            print(f"🔹 DEBUG: Mật khẩu mới (đã hash): {hashed_password}")
            update_data["password"] = hashed_password

        if update_data:
            print(f"🔹 DEBUG: Dữ liệu cập nhật: {update_data}")
            users_collection.update_one({"username": username}, {"$set": update_data})
            print(f"✅ DEBUG: Cập nhật MongoDB thành công cho user {username}")

        return {"message": "Cập nhật thông tin thành công"}
    except HTTPException as e:
        raise e
    except Exception as e:
        print("❌ Lỗi cập nhật:", e)
        raise HTTPException(status_code=500, detail="Lỗi server khi cập nhật thông tin người dùng")



# Gọi hàm từ AutoReportX.py 
class QueryRequest(BaseModel):
    user_query: str
    iteration_limit: int = 1

@app.post("/predict/")
async def predict(request: QueryRequest):
    try:
        # Gọi hàm từ AutoReportX.py
        result = run_gradio(request.user_query, request.iteration_limit)
        return {"data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Định nghĩa model cho request
class DownloadRequest(BaseModel):
    content: str
    file_type: str
    
@app.post("/download-report/")
async def download_report(request: DownloadRequest):
    try:
        print("Nhận yêu cầu tải file với loại:", request.file_type)
        
        if request.file_type == "doc":
            file_stream, filename = create_word_file(request.content)
            media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        
        elif request.file_type == "pdf":
            file_stream, filename = create_pdf_file(request.content, 'report.pdf')
            media_type = "application/pdf"
        
        else:
            return {"error": "Loại file không hợp lệ. Chọn 'doc' hoặc 'pdf'."}

        return StreamingResponse(
            file_stream,
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return {"error": f"Lỗi khi tạo file: {str(e)}"}
    
    
if __name__ == "__main__": 
    # Chạy Server
    uvicorn.run(app, host="0.0.0.0", port=5000)