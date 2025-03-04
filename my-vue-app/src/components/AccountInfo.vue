<template>
    <div class="body"> 
      <div class="content">
        <div class="container-fluid">
          <div class="header-container" style="text-align: center;">
            <h1 style="font-size: 7em; text-align: center;">AutoReportX</h1> 
          </div>   
  
          <br><br>

          <div class="auth-options">
              <select id="language-select" v-model="language" @change="toggleLanguage">
                <option value="vi">Tiếng Việt VN</option>
                <option value="en">English US</option>
              </select>
            </div>

          <div class="auth-form">
            <h2>{{ translations[language].profileTitle }}</h2>
            <form @submit.prevent="updateProfile">

              <!-- Avatar và upload -->
              <div class="avatar-upload">
                <input type="file" @change="handleAvatarUpload" accept="image/*" />
                <img :src="avatarPreview || require('@/assets/default_avatar.png')" alt="Avatar" />
              </div>

              <!-- Thông tin người dùng -->
              <div class="form-group">
                <label for="fullname">{{ translations[language].fullnameLabel }}</label>
                <input v-model="user.fullname" type="text" required />
              </div>

              <div class="form-group">
                <label for="email">{{ translations[language].emailLabel }}</label>
                <input v-model="user.email" type="email" required />
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

  import {ref, computed, reactive, onMounted } from 'vue';
  import { inject } from "vue";
  import axios from "axios";
  
  // Lấy ngôn ngữ từ inject
  const language = ref(inject("language"));
  const toggleLanguage = inject("toggleLanguage");

  // Dịch ngôn ngữ động
  const currentTranslations = computed(() => translations[language.value]);

  const user = reactive({
    fullname: "",
    email: "",
    username: "",
    password: "",
    avatar: "@/assets/default_avatar.png", // Avatar mặc định
  });

const avatarPreview = ref(null); // Hiển thị preview avatar
const avatarFile = ref(null); // File avatar được chọn


// API để lấy thông tin người dùng
const fetchUserProfile = async () => {
  try {
    const token = localStorage.getItem("token");
    if (!token) {
      alert("⚠️ Bạn chưa đăng nhập!");
      return;
    }

    const response = await axios.get("/api/user/profile", {
      headers: { Authorization: `Bearer ${token}` },
    });

    Object.assign(user, response.data);
    avatarPreview.value = user.avatar || require("@/assets/default_avatar.png"); // Sử dụng avatar mặc định nếu không có
    console.log("✅ Lấy thông tin user thành công:", response.data);
  } catch (error) {
    console.error("❌ Lỗi khi lấy thông tin user:", error);
    alert("⚠️ Không thể lấy thông tin tài khoản!");
  }
};


// Xử lý upload avatar
const handleAvatarUpload = (event) => {
  const file = event.target.files[0];
  if (!file) return;

  // Kiểm tra định dạng file (chỉ nhận ảnh)
  const allowedTypes = ["image/jpeg", "image/png", "image/webp"];
  if (!allowedTypes.includes(file.type)) {
    alert("⚠️ Chỉ chấp nhận file JPG, PNG, WEBP!");
    return;
  }

  // Kiểm tra kích thước file (giới hạn 2MB)
  if (file.size > 2 * 1024 * 1024) {
    alert("⚠️ Kích thước ảnh quá lớn! (Tối đa 2MB)");
    return;
  }

  avatarPreview.value = URL.createObjectURL(file);
  avatarFile.value = file;
};

// Xử lý cập nhật thông tin tài khoản
const updateProfile = async () => {
  try {
    const formData = new FormData();
    formData.append("fullname", user.fullname);
    formData.append("email", user.email);
    if (user.password) formData.append("password", user.password); // Chỉ gửi nếu có nhập
    if (avatarFile.value) formData.append("avatar", avatarFile.value);

    const token = localStorage.getItem("token");

    await axios.put("/api/user/profile", formData, {
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "multipart/form-data" },
    });

    alert("🎉 Cập nhật thành công!");
    fetchUserProfile(); // Cập nhật lại giao diện
  } catch (error) {
    console.error("❌ Lỗi cập nhật:", error);
    alert("⚠️ Cập nhật thất bại!");
  }
};


onMounted(fetchUserProfile);

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
      contactAddress: "📍 Địa chỉ: Trường Công nghệ Thông tin & Truyền thông"
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
      contactAddress: "📍 Address: College of Information and Communication Technology, Can Tho University"
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

  h2 {
      text-indent: 2em;
      font-size: 1.2em;
      max-width: 80%;
      word-wrap: break-word;
      text-align: justify;
  }

  p {
      font-size: 1em;
      max-width: 75%;
      word-wrap: break-word;
      text-align: justify;
      margin-left: 20px;
  }

  h4 {
      font-size: 1em;
      max-width: 80%;
      text-align: justify;
      word-wrap: break-word;
      font-weight: normal;
      text-indent: 2em;
  }

  h3 {
    font-size: 1.5em;
    max-width: 100%;
    word-wrap: break-word;
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
  
  .logo {
      width: 50px; /* Kích thước logo */
      height: 50px;
      position: absolute;
      top: 10px;
      left: 0;
      animation: moveLogo 3s linear infinite alternate;
  }
  @keyframes moveLogo {
      0% { left: 0; }
      100% { left: calc(100% - 10px); } /* Icon di chuyển qua lại */
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

  .header-logo {
      position: relative;

      animation: wave 2s ease-in-out infinite;
  }

  @keyframes wave {
      0% { transform: translateY(0px); }
      50% { transform: translateY(10px); }
      100% { transform: translateY(0px); }
  }

  .header-logo img {
      width: 400px; /* Điều chỉnh kích thước logo */
      height: auto;
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
      width: 700px; /* Chiều rộng khung đăng nhập */
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

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
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
}

.btn-update:hover {
  background-color: #0056b3;
}

</style>
  