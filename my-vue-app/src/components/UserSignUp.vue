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
        
         <!-- Khung đăng ký -->
         <div class="auth-form">
          <h2 id="registerTitle">{{ translations[language].registerTitle }}</h2>
          <form @submit.prevent="handleSignUp">
            <div class="form-group">
              <label for="fullname">{{ translations[language].fullnameLabel }}</label>
              <input type="text" v-model="fullname" id="fullname" :placeholder="translations[language].fullnamePlaceholder" />
            </div>
            <div class="form-group">
              <label for="email">{{ translations[language].emailLabel }}</label>
              <input type="email" v-model="email" id="email" :placeholder="translations[language].emailPlaceholder" />
            </div>
            <div class="form-group">
              <label for="username">{{ translations[language].usernameLabel }}</label>
              <input type="text" v-model="username" id="username" :placeholder="translations[language].usernamePlaceholder" />
            </div>
            <div class="form-group">
              <label for="password">{{ translations[language].passwordLabel }}</label>
              <input type="password" v-model="password" id="password" :placeholder="translations[language].passwordPlaceholder" />
            </div>
            <div class="form-group">
              <label for="confirmPassword">{{ translations[language].confirmPasswordLabel }}</label>
              <input type="password" v-model="confirmPassword" id="confirmPassword" :placeholder="translations[language].confirmPasswordPlaceholder" />
            </div>
            <button class="btn-login" id="registerButton">{{ translations[language].registerButton }}</button>

            <p>{{ translations[language].orLoginWith }}</p>

            <div class="social-login">
              <button type="button" class="social-btn google " ><i class='bx bxl-google'></i>&nbsp;&nbsp;{{ translations[language].loginWithGoogle }}</button>
              <button type="button" class="social-btn facebook" ><i class='bx bxl-facebook-circle'></i>&nbsp;&nbsp;{{ translations[language].loginWithFacebook }}</button>
            </div>
            
          </form>
          <p class="signin-link">
              {{ translations[language].haveAccount }}
              <button class="btn-signin" @click="goToLogin">
                {{ translations[language].signinStatus }}
              </button>
            </p>
        </div>
        <!-- Kết thúc khung đăng ký -->
  
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
  import { inject } from 'vue';
  import {ref, computed } from 'vue';
  import axios from "axios";

  const router = useRouter();
  const language = ref(inject("language"));
  const toggleLanguage = inject("toggleLanguage");

  const currentTranslations = computed(() => translations[language.value]);
  
  const translations = {
    vi: {
      contactTitle: "Mọi chi tiết xin vui lòng liên hệ:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 Hoặc 0559-285-596",
      contactAddress: "📍 Địa chỉ: Trường Công nghệ Thông tin & Truyền thông, Đại học Cần Thơ",
      registerTitle: "Đăng Ký",
      fullnameLabel: "Họ và tên:",
      fullnamePlaceholder: "Nhập họ và tên",
      emailLabel: "Email:",
      emailPlaceholder: "Nhập email",
      usernameLabel: "Tên đăng nhập:",
      usernamePlaceholder: "Nhập tên đăng nhập",
      passwordLabel: "Mật khẩu:",
      passwordPlaceholder: "Nhập mật khẩu",
      confirmPasswordLabel: "Xác nhận mật khẩu:",
      confirmPasswordPlaceholder: "Nhập lại mật khẩu",
      registerButton: "Đăng Ký",
      haveAccount: "Bạn đã có tài khoản?",
      signinStatus: "Đăng nhập",
      signupSuccess: "Đăng ký thành công!",
      orLoginWith: "Hoặc đăng nhập với:",
      loginWithFacebook: "Đăng nhập với Facebook",
      loginWithGoogle: "Đăng nhập với Google"
    },
    en: {
      contactTitle: "For further details, please contact:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 or 0559-285-596",
      contactAddress: "📍 Address: College of Information and Communication Technology, Can Tho University",
      registerTitle: "Register",
      fullnameLabel: "Full Name:",
      fullnamePlaceholder: "Enter your full name",
      emailLabel: "Email:",
      emailPlaceholder: "Enter your email",
      usernameLabel: "Username:",
      usernamePlaceholder: "Enter your username",
      passwordLabel: "Password:",
      passwordPlaceholder: "Enter your password",
      confirmPasswordLabel: "Confirm Password:",
      confirmPasswordPlaceholder: "Re-enter your password",
      registerButton: "Register",
      haveAccount: "Already have an account?",
      signinStatus: "Log In",
      signupSuccess: "Sign up successful!",
      orLoginWith: "Or log in with:",
      loginWithGoogle: "Log in with Google",
      loginWithFacebook: "Log in with Facebook"
    }
  };

  const goToLogin = () => {
    router.push("/login");
  };

  const fullname = ref("");
  const email = ref("");
  const username = ref("");
  const password = ref("");
  const confirmPassword = ref("");

  const handleSignUp = async () => {
  if (password.value !== confirmPassword.value) {
    alert("❌ Mật khẩu xác nhận không khớp!");
    return;
  }

  try {
    const response = await axios.post("/api/auth/register", {
      fullname: fullname.value,
      email: email.value,
      username: username.value,
      password: password.value
    });
    console.log(response);

    const { token, user } = response.data;

    // Lưu token và thông tin user vào localStorage
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(user));

    alert("🎉 Đăng ký thành công!");

    // Chuyển đến trang chủ
    router.push("/home");
  } catch (error) {
    alert("❌ " + (error.response?.data?.detail || "Đăng ký thất bại!"));
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

.btn-home {
  margin-top: 15px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn-home:hover {
  background-color: #0056b3;
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

        .btn-signin {
  background: none;
  color: #007bff;
  text-decoration: underline;
  cursor: pointer;
}
.signin-link {
  margin-top: 10px;
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
  
  </style>