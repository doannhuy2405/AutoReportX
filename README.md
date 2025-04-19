# Hệ thống AutoReportX: Tìm kiếm, trích xuất nội dung, đánh giá thông tin và tạo báo cáo tự động
AutoReportX được thiết kế nhằm tối ưu hóa việc thu thập, tìm kiếm tin thông và tạo báo cáo.

AutoReportX được phát triển bằng Visual Studio Code, sử dụng Vue.js làm framework và tận dụng Bootstrap để thiết kế giao diện kết hợp với HTML, CSS và JavaScript. Backend sử dụng Python kết hợp với FastAPI để xây dụng, trong khi MongoDB đóng vai trò là cơ sở dữ liệu chính. Cùng với đó là sự kết hợp các external APIs như OpenAI API, Tavily API, TogetherAI API và Firebase được tích hợp xử lý xác thực quản lý đăng nhập từ tài khoản Google.

HƯỚNG DẪN CÀI ĐẶT HỆ THỐNG AUTOREPORTX:

1. Yêu cầu hệ thống
   - Node.js >= 16.x
   - Python >= 3.9
   - MongoDB
   - Visual Studio Code
   - Git
   - Trình duyệt hiện đại
  
2. Clone source code từ Github
   
   git clone https://github.com/doannhuy2405/AutoReportX.git
   
   cd AutoReportX

3. Cài đặt frontend (Vue.js)

   cd my-vue-app
   
   npm install
   
   Chạy thử frontend:
   
   npm run serve (Tùy vào từng phiên bản sẽ là npm run dev)

4. Cài đặt backend (FastAPI)

   cd backend
   
   python -m venv venv (Cài đặt môi trường ảo)

   venv\Scripts\activate # Đối với window
   
   hoặc source venv/bin/activate  # Đối với macOS/Linux
   
   pip install -r requirements.txt
   
   Chạy FastAPI server:
   
   uvicorn main:app --reload

5. Cài đặt và khởi động MongoDB
   
   Tải MongoDB tại: https://www.mongodb.com/try/download/community
   
   Sau khi cài xong, bật dịch vụ MongoDB bằng MongoDB Compass hoặc dòng lệnh:
   mongod

   Sau đó, lưu đường dẫn kết nối MongoDB localhost (ví dụ mongodb://localhost:27017) vào biến MONGO_URI

7. Cấu hình Firebase (Google Auth)
    
   Truy cập Firebase Console: https://console.firebase.google.com/
   
   Tạo project mới hoặc dùng project hiện tại
   
   Bật Authentication -> Sign-in method -> Google
   
   Tạo Web App -> lấy apiKey, authDomain, projectId, storageBucket, messagingSenderId, appId
   
   Thêm thông tin vào file main.js và firebase.js trong my-vue-app

   Sau đó cấu hình Firebase Admin với file JSON (Service Account):

   Vào Firebase Console

   Chọn project

   Vào mục Project Settings (biểu tượng bánh răng)

   Chuyển sang tab Service account

   Nhấn nút Generate new private key

   Tại file JSON về -> đổi tên lại (ví dụ firebase_credentials.json)

   Đặt vào thư mục backend (Lưu ý: Đặt ngang bậc với main.py)

   Tiếp theo là cài đặt Firebase Admin SDK trong FastAPI:

   pip install firebase-admin

   Sau đó trở về mục .env trong backend:

   GOOGLE_APPLICATION_CREDENTIALS="đường dẫn file JSON vừa tải về" 

8. Tích hợp API

   Đảm bảo đã có API key cho:

   OpenAI API: https://platform.openai.com

   TogetherAI API: https://platform.together.xyz/

   Tavily API: https://www.tavily.com/

   Gán các API Key vào biến môi trường TOGETHER_API_KEY, TAVILY_API_KEY, MY_OPENAI_API_KEY trong .env trong backend

   Trong .env của backend vẫn còn thiếu 1 biến là SECRET_KEY (Là một chuỗi ký tự bí mật dùng để ký và xác minh JWT Token và bảo mật các thông tin nhạy cảm như session, xác thực người dùng)

   Tự tạo một chuỗi random mạnh bằng lệnh Python:

   python -c "import secrets; print(secrets.token_urlsafe(64))"

   Sau đó, kết quả sẽ trả ra một chuỗi ngẫu nhiên dài 64 ký tự -> Lưu chuỗi này vào biến SECRET_KEY trong .env

9. Khởi chạy toàn bộ hệ thống

    Mở 2 terminal:
   
   Terminal 1: khởi chạy backend
   - cd backend
   - venv\Scripts\activate
   - python main.py

   Terminal 2: khởi chạy my-vue-app
   - cd my-vue-app
   - npm run serve (Hoặc npm run dev tùy phiên bản)

   
           
