<template>
    <div class="body"> 
      <div class="content">
        <div class="container-fluid">
          <div class="header-container" style="text-align: center;">
            <h1 style="font-size: 7em; text-align: center;">AutoReportX</h1> 

            <div class="auth-options">
              <select id="language-select" v-model="language" @change="toggleLanguage">
                <option value="vi">Tiếng Việt VN</option>
                <option value="en">English US</option>
              </select>
            </div>
          </div>
  
          <br><br>

          <div v-if="user" style="font-size: 2em;">
            <p>{{ translations[language].sayHiWithUser }}, {{ user.fullname }}!</p>
          </div>

          <div class="auth-form">
            <h2>{{ translations[language].profileTitle }}</h2>
            <form @submit.prevent="updateProfile">

              <!-- Thông tin người dùng -->
              <div class="form-group">
                <label for="fullname">{{ translations[language].fullnameLabel }}</label>
                <input id="fullname" v-model="user.fullname" type="text" disabled readonly />
              </div>

              <div class="form-group">
                <label for="email">{{ translations[language].emailLabel }}</label>
                <input id="email" v-model="user.email" type="email" disabled readonly />
              </div>

              <div class="form-group">
                <label for="username">{{ translations[language].usernameLabel }}</label>
                <input type="text" v-model="user.username" id="username" disabled readonly />
              </div>

              <div class="form-group">
                <label for="password">{{ translations[language].passwordLabel }}</label>
                <input
                  type="password"
                  v-model="user.password"
                  id="password"
                  :placeholder="translations[language].passwordPlaceholder"
                  autocomplete="off"
                />
              </div>

              <!-- Nút cập nhật -->
              <button type="submit" class="btn-update">
                {{ translations[language].updateButton }}
              </button>
            </form>
          </div>
  
      <div class="contact-info">
        <p>{{ currentTranslations.contactTitle }}</p><br>
        <p>{{ currentTranslations.contactEmail }}</p>
        <p>{{ currentTranslations.contactPhone }}</p>
        <p>{{ currentTranslations.contactAddress }}</p>
      </div>    
  
      <footer class="footer">
        <div class="footer-left">
          <i class='bx bxl-facebook' ></i>
          <i class='bx bxl-gmail' ></i>
          <i class='bx bxl-youtube' ></i>
          <i class='bx bxl-linkedin' ></i>
          <i class='bx bxl-github' ></i>
          <i class='bx bxl-instagram' ></i>
          <i class='bx bxl-tiktok' ></i>
          <i class='bx bxl-discord-alt' ></i>
        </div>
        <div class="footer-right">
          AutoReportX © 2025
        </div>
      </footer>
    </div>
  </div>
  </div>
</template>


<script setup>

  import {ref, computed, onMounted } from 'vue';
  import { inject } from "vue";
  import axios from "axios";
  import { useRouter } from "vue-router"; 

  const router = useRouter(); // Khởi tạo router
  
// Lấy ngôn ngữ từ inject
  const language = ref(inject("language"));
  const toggleLanguage = inject("toggleLanguage");

 // Dịch ngôn ngữ động
  const currentTranslations = computed(() => translations[language.value]);

  const user = ref({
    fullname: "",
    email: "",
    username: "",
    password: "",
  });

  const token = localStorage.getItem("token");

// API lấy thông tin user từ backend
const getUserInfo = async () => {
  try {
    const response = await axios.get("/api/user/profile", {
      headers: { Authorization: `Bearer ${token}` },
    });

    user.value = response.data;
  } catch (error) {
    console.error("❌ Lỗi lấy thông tin user:", error);
  }
};

// API cập nhật email & password
const updateProfile = async () => {
  try {
    await axios.put(
      "/api/user/profile",
      {
        email: user.value.email,
        password: user.value.password,
      },
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );

    alert("✅ Cập nhật thành công!");
    user.value.password = ""; // Reset password sau khi cập nhật

    // Chuyển hướng sang trang Home sau khi cập nhật
    router.push("/home");
  } catch (error) {
    console.error("❌ Lỗi cập nhật:", error);
    alert("⚠ Lỗi khi cập nhật!");
  }
};

onMounted(getUserInfo);

  const translations = {
    vi: {
      profileTitle: "Thông Tin Tài Khoản",
      fullnameLabel: "Họ và Tên",
      emailLabel: "Email",
      usernameLabel: "Tên Đăng Nhập",
      passwordLabel: "Mật Khẩu",
      updateButton: "Cập Nhật",
      contactTitle: "Mọi chi tiết xin vui lòng liên hệ:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 Hoặc 0559-285-596",
      contactAddress: "📍 Địa chỉ: Trường Công nghệ Thông tin & Truyền thông",
      sayHiWithUser: "Xin chào", 
      passwordPlaceholder: "Nhập vào mật khẩu mới..."
    },
    en: {
      profileTitle: "Account Information",
      fullnameLabel: "Full name",
      emailLabel: "Email",
      usernameLabel: "Username",
      passwordLabel: "Password",
      updateButton: "Update",
      contactTitle: "For further details, please contact:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 or 0559-285-596",
      contactAddress: "📍 Address: College of Information and Communication Technology, Can Tho University",
      sayHiWithUser: "Hi",
      passwordPlaceholder: "Enter new password..."
    }
  };
  </script>
  
  <style scoped >
  * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: Arial, sans-serif;
  }

  .body {
      color: white;
      margin: 0;
      padding: 0;
      font-family: 'Times New Roman', Times, serif;
      background-image: url('../assets/Background_web.png'); 
      background-size: cover;
      background-position: center;
      background-attachment: fixed; 
      height: 100%;
      display: flex;
      flex-direction: column;
  }
  
  .nav {
      margin-top: 10px;
  }
  .nav a {
      color: white;
      text-decoration: none;
      margin: 0 15px;
      font-size: 18px;
      padding: 8px 15px;
      background: rgba(255, 255, 255, 0.2);
      border-radius: 5px;
      transition: 0.3s;
  }

  .auth-links a {
      color: white !important; /* Chuyển chữ thành màu trắng */
      font-weight: bold; /* Làm đậm chữ */
      text-decoration: none; /* Loại bỏ gạch chân */
  }
  
  .auth-links a:hover {
      text-decoration: underline; /* Gạch chân khi di chuột */
  }        

  .nav a:hover {
      background: rgba(255, 255, 255, 0.5);
  }

  .container-fluid {
      padding: 40px;
  }

  .header-container {
      display: flex;
      justify-content: space-between; /* Căn hai bên */
      position: relative;
      align-items: center; /* Căn giữa theo chiều dọc */
  }        

  .footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      color: white;
      padding: 10px 20px;
      text-align: center;
      gap: 20px;
  }

  .content {
      flex: 1;
  }
  
  .footer-left i {
      color: white;
      font-size: 25px;
      margin-right: 15px;
      text-decoration: none;
  }

  .footer-left {
      display: flex;
      align-items: center;
      gap: 15px; /* Khoảng cách giữa các icon */
  }

  .footer-left img {
      width: 30px; /* Điều chỉnh kích thước icon */
      height: 24px;
  }

  .footer-right {
      font-size: 25px;
      display: flex;
      align-items: center;
  }
  
  .footer-right .language-btn {
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: white;
      padding: 5px 15px;
      border-radius: 20px;
      cursor: pointer;
      font-size: 14px;
  }
  
  .footer-right span {
      opacity: 0.7;
      font-size: 12px;
  }        

  .contact-info {
      text-align: center;
      color: white;
      font-size: 16px;
      padding: 20px;
      border-radius: 10px;
      margin-bottom: 20px; /* Tạo khoảng cách với footer */
  }

  .auth-options {
      display: flex;
      align-items: center;
      gap: 10px;
  }
  
  #language-select {
      background: black;
      color: white;
      border: 1px solid white;
      padding: 5px;
      border-radius: 5px;
      cursor: pointer;
  }

  .lang-content {
      display: none;
  }
  
  #content-vi {
      display: block; /* Mặc định hiển thị tiếng Việt */
  }        
  #content {
      display: flex;
  }

  p.double {border-style: double;}

  .tagline-box {
  background: linear-gradient(90deg, #1E3A8A, #6B21A8);
  color: white;
  padding: 20px;
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.3);
}

.auth-form {
      background-color: rgba(255, 255, 255, 0.8); /* Nền trắng trong suốt */
      border-radius: 10px;
      padding: 20px;
      margin: 20px auto;
      width: 750px; /* Chiều rộng khung */
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
  }
  
  .form-group {
      margin-bottom: 15px;
  }

  .form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 16px;
}

  .form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

  .avatar-upload {
  text-align: center;
  margin-bottom: 20px;
}

.avatar-upload img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
}

input[type="file"] {
  display: block;
  margin: 10px auto;
}

input {
      width: 100%;
      padding: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
}

.btn-update {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  width: 100%;
}

.btn-update:hover {
  background-color: #0056b3;
}

</style>
  