<template>
    <div class="body">
      <div class="content">
        <div class="container">
          <div class="header-container">
            <div style="display: flex;">
              <div class="header-logo">
                <img src="../assets/logo.png" alt="AutoReportX Logo" />
              </div>
              <h1 class="header-text">AutoReportX</h1>
            </div>
  
            <div class="auth-options">
              <select id="language-select" v-model="language" @change="toggleLanguage">
                <option value="vi">Tiếng Việt VN</option>
                <option value="en">English US</option>
              </select>
            </div>
          </div>
        </div>
        
        <!-- Khung đăng nhập -->
        <div class="auth-form">
          <h2 id="loginTitle">{{translations[language].loginTitle}}</h2>
          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="username" id="usernameLabel">{{translations[language].usernameLabel}}</label>
              <input type="text" v-model="username" id="usernamePlaceholder" :placeholder="translations[language].usernamePlaceholder" />
            </div>
            <div class="form-group">
              <label for="password" id="passwordLabel">{{translations[language].passwordLabel}}</label>
              <input type="password" v-model="password" id="passwordPlaceholder" :placeholder= "translations[language].passwordPlaceholder" />
              <a href="#" id="forgotPassword">{{translations[language].forgotPassword}}</a>
            </div>
            <button class="btn-login" id="loginButton"> {{translations[language].loginButton}}</button> 

            <p>{{ translations[language].orLoginWith }}</p>
            
            <div class="social-login">
              <button type="button" class="social-btn google " ><i class='bx bxl-google'></i>&nbsp;&nbsp;{{ translations[language].loginWithGoogle }}</button>
              <button type="button" class="social-btn facebook" ><i class='bx bxl-facebook-circle'></i>&nbsp;&nbsp;{{ translations[language].loginWithFacebook }}</button>
            </div>

          </form>
    
          <p class="signup-link">
            {{ translations[language].noAccount }}
            <button class="btn-signup" @click="goToSignUp">
              {{ translations[language].signupStatus }}
            </button>
          </p>

        </div>
        <!-- Kết thúc khung đăng nhập -->
  
        <div class="contact-info">
          <p>{{ currentTranslations.contactTitle }}</p><br>
          <p>{{ currentTranslations.contactEmail }}</p>
          <p>{{ currentTranslations.contactPhone }}</p>
          <p>{{ currentTranslations.contactAddress }}</p>
        </div>  
  
        <footer class="footer">
          <div class="footer-left">
            <i class='bx bxl-facebook'></i>
            <i class='bx bxl-gmail'></i>
            <i class='bx bxl-youtube'></i>
            <i class='bx bxl-linkedin'></i>
            <i class='bx bxl-github'></i>
            <i class='bx bxl-instagram'></i>
            <i class='bx bxl-tiktok'></i>
            <i class='bx bxl-discord-alt'></i>
          </div>
          <div class="footer-right">
            AutoReportX © 2025
          </div>
        </footer>
      </div>
    </div>
  </template>
  
  <script setup>
  import { useRouter } from 'vue-router';
  import {ref, computed } from 'vue';
  import { inject } from "vue";
  import axios from "axios";

  // Biến lưu tên đăng nhập và mật khẩu
  const username = ref("");
  const password = ref("");

  // Sử dụng Vue Router để điều hướng
  const router = useRouter();
  
  // Lấy ngôn ngữ từ inject
  const language = ref(inject("language"));
  const toggleLanguage = inject("toggleLanguage");

  // Dịch ngôn ngữ động
  const currentTranslations = computed(() => translations[language.value]);
  
  // Danh sách ngôn ngữ
  const translations = {
    vi: {
      contactTitle: "Mọi chi tiết xin vui lòng liên hệ:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 Hoặc 0559-285-596",
      contactAddress: "📍 Địa chỉ: Trường Công nghệ Thông tin & Truyền thông, Đại học Cần Thơ",
      loginTitle: "Đăng Nhập",
      usernameLabel: "Tên đăng nhập:",
      usernamePlaceholder: "Nhập tên đăng nhập",
      passwordLabel: "Mật khẩu:",
      passwordPlaceholder: "Nhập mật khẩu",
      forgotPassword: "Quên mật khẩu?",
      loginButton: "Đăng Nhập",
      orLoginWith: "Hoặc đăng nhập bằng:",
      noAccount: "Bạn chưa có tài khoản?",
      signupStatus: "Đăng ký",
      loginStatus: "Đăng nhập thành công!",
      loginError: "Sai tên đăng nhập hoặc mật khẩu!",
      loginWithFacebook: "Đăng nhập với Facebook",
      loginWithGoogle: "Đăng nhập với Google",

    },
    en: {
      contactTitle: "For further details, please contact:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 or 0559-285-596",
      contactAddress: "📍 Address: College of Information and Communication Technology, Can Tho University",
      loginTitle: "Login",
      usernameLabel: "Username:",
      usernamePlaceholder: "Enter your username",
      passwordLabel: "Password:",
      passwordPlaceholder: "Enter your password",
      forgotPassword: "Forgot password?",
      loginButton: "Login",
      orLoginWith: "Or log in with:",
      noAccount: "Don't have an account?",
      signupStatus: "Sign Up",
      loginStatus: "Log in successfully!",
      loginError: "Incorrect username or password!",
      loginWithFacebook: "Log in with Facebook",
      loginWithGoogle: "Log in with Google"
    }
  };

  const goToSignUp = () => {
    router.push("/signup");
  }

  // Xử lý đăng nhập
  const handleLogin = async () => {
  try {
    console.log("🔹 Bắt đầu gửi request đăng nhập...");

    console.log(username.value, password.value)
    
    const response = await axios.post("/api/auth/login", {
      username: username.value,
      password: password.value
    });

    console.log("✅ Đăng nhập thành công!", response.data);

    const { token, user } = response.data;

    // 🔹 Lưu token và user vào localStorage
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));

    alert("🎉 Đăng nhập thành công!");
    
    // 🔹 Chuyển hướng vào trang chủ
    router.push("/home");
  } catch (error) {
    console.error("❌ Lỗi đăng nhập:", error);
    
    if (error.response) {
      alert("⚠️ " + error.response.data.detail);
    } else {
      alert("❌ Không thể kết nối đến server!");
    }
  }
};
    
  </script>
  
  <style scoped>

.social-login {
    margin-top: 15px;
}

.social-btn {
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    width: 48%;
}

.facebook {
    background-color: #3b5998;
    color: white;
}

.google {
    background-color: #c77177;
    color: white;
}
  /* Các phong cách hiện có */
  * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: Arial, sans-serif;
  }
  
  .body {
      /* Các phong cách khác tại đây */
      flex-direction: column;color: white;
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
  
  .auth-options {
            display: flex;
            align-items: center;
            gap: 10px;
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
  
  h2 {
    text-align: center;
  }
  
  label {
      display: block;
      margin-bottom: 5px;
      font-weight: bold;
  }
  
  input {
      width: 100%;
      padding: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
  }
  
  .btn-login {
      width: 100%;
      padding: 10px;
      background-color: #f50057; /* Màu nút đăng nhập */
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
  }
  
  .btn-login:hover {
      background-color: #c51162; /* Màu nền khi hover */
  }
  
  .social-login {
      display: flex;
      justify-content: space-between;
  }
  
  .btn-social {
      width: 48%;
      padding: 10px;
      background-color: #00aced; /* Màu nút mạng xã hội */
      color: white;
      border: none;
      border-radius: 5px;
      cursor: pointer;
  }
  
  .btn-social:hover {
      background-color: #0099cc; /* Màu nền khi hover */
  }
  
  .container {
            padding: 40px;
        }
  
  .header-container {
    display: flex;
    justify-content: space-between;
    padding: 10px 20px;
    gap: 1px;
    align-items: center;
  }        
  
        .header-logo {
            position: relative;
            height: auto;
            display: flex;
            align-items: center;
            gap: 15px;
            margin-right: 20px ;
            position: relative;
            animation: wave 2s ease-in-out infinite;
        }
  
        @keyframes wave {
            0% { transform: translateY(0); }
            50% { transform: translateY(10px); }
            100% { transform: translateY(0); }
        }
  
        .header-text {
            text-align: left;
            font-size: 5em;
            margin-left: 20px; /* Tạo khoảng cách với logo */
        }
        
        .header-logo img {
            width: 100px; /* Điều chỉnh kích thước logo */
            height: auto;
        }
  
        .contact-info {
            text-align: left;
            color: white;
            font-size: 16px;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px; /* Tạo khoảng cách với footer */
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
            width: 24px; /* Điều chỉnh kích thước icon */
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

        .btn-signup {
          background: none;
          color: #007bff;
          text-decoration: underline;
          cursor: pointer;
        }

        .signup-link {
          margin-top: 10px;
        }
  </style>