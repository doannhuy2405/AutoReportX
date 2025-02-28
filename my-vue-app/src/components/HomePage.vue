<template>
    <div class="body">
      <div class="content">
        <div class="container">
          <div class="header-container">
            <div style="flex: 1; text-align: center;">
              <h1 style="padding-left: 150px; font-size: 3em;">AutoReportX</h1>
            </div>
  
            <div class="auth-options" style="display: flex; align-items: center; gap: 15px;">
              <select id="language-select" @change="toggleLanguage" v-model="language">
                <option value="vi">Tiếng Việt VN</option>
                <option value="en">English US</option>
              </select>

              <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle avatar-btn" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <div class="avatar-container">
                    <img :src="user.avatar || defaultAvatar" class="rounded-circle avatar-img" alt="User Avatar">
                  </div>
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li class="dropdown-header text-center">
                    <div class="avatar-container" style="width: 155px; height: 155px;">
                      <img :src="user.avatar || defaultAvatar" class="rounded-circle avatar-img-lg" alt="User Avatar">
                    </div>
                    <p class="fw-bold">{{ user.name }}</p>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" href="./AccountInfo.vue">{{ translations[language].accountInfo }}</a></li>
                  <li><a class="dropdown-item" href="#">{{ translations[language].upgradePlan }}</a></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item text-danger" href="#" @click="logout">{{ translations[language].logout }}</a></li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="auth-form-p">
          <h4 style="font-size: 1.2em; text-align: center;">AutoReportX History</h4>
        </div>

       <div class="auth-form">
         <!-- Lưu trữ lịch sử tào báo cáo và nội dung báo cáo -->
         <div class="accordion" id="accordionPanelsStayOpenExample">
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseOne" aria-expanded="true" aria-controls="panelsStayOpen-collapseOne">
                Accordion Item #1
              </button>
            </h2>
            <div id="panelsStayOpen-collapseOne" class="accordion-collapse collapse show">
              <div class="accordion-body">
                <strong>This is the first item's accordion body.</strong> It is shown by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseTwo" aria-expanded="false" aria-controls="panelsStayOpen-collapseTwo">
                Accordion Item #2
              </button>
            </h2>
            <div id="panelsStayOpen-collapseTwo" class="accordion-collapse collapse">
              <div class="accordion-body">
                <strong>This is the second item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
              </div>
            </div>
          </div>
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapseThree" aria-expanded="false" aria-controls="panelsStayOpen-collapseThree">
                Accordion Item #3
              </button>
            </h2>
            <div id="panelsStayOpen-collapseThree" class="accordion-collapse collapse">
              <div class="accordion-body">
                <strong>This is the third item's accordion body.</strong> It is hidden by default, until the collapse plugin adds the appropriate classes that we use to style each element. These classes control the overall appearance, as well as the showing and hiding via CSS transitions. You can modify any of this with custom CSS or overriding our default variables. It's also worth noting that just about any HTML can go within the <code>.accordion-body</code>, though the transition does limit overflow.
              </div>
            </div>
          </div>
        </div>
       </div>
          
        <div class="contact-info">
          <p>{{ currentTranslations.contactTitle }}</p><br>
          <p>{{ currentTranslations.contactEmail }}</p>
          <p>{{ currentTranslations.contactPhone }}</p>
          <p>{{ currentTranslations.contactAddress }}</p>
        </div>  
  
        <footer class="footer">
          <div class="footer-left">
            <i class='bx bxs-lemon'></i>
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
  import { ref, computed, onMounted } from 'vue';
  import { inject } from "vue";
  import { useRouter } from 'vue-router';

  const router = useRouter() ;
  const user = ref({});

  onMounted(() => {
  // const userData = localStorage.getItem("user");
  // if (userData) {
  //   user.value = JSON.parse(userData);
  // } else {
  //   router.push("/login"); // Nếu chưa đăng nhập thì chuyển về trang login
  // }
});

const logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  router.push("/");
};



  const language = ref(inject("language"));
  const toggleLanguage = inject("toggleLanguage");
  
  const currentTranslations = computed(() => translations[language.value]);
  
  const translations = {
    vi: {
      contactTitle: "Mọi chi tiết xin vui lòng liên hệ:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 Hoặc 0559-285-596",
      contactAddress: "📍 Địa chỉ: Trường Công nghệ Thông tin & Truyền thông, Đại học Cần Thơ",
      accountInfo: "Thông tin tài khoản",
      upgradePlan: "Nâng cấp gói",
      logout: "Đăng xuất"
    },
    en: {
      contactTitle: "For further details, please contact:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 or 0559-285-596",
      contactAddress: "📍 Address: College of Information and Communication Technology, Can Tho University",
      accountInfo: "Account Information",
      upgradePlan: "Upgrade Plan",
      logout: "Logout"
    }
  };
  </script>
  
  <style scoped>

.auth-form {
      background-color: rgba(255, 255, 255, 0.8); /* Nền trắng trong suốt */
      border-radius: 5px;
      padding: 2ch;
      margin: 20px;
      width: 300px; /* Chiều rộng khung đăng nhập */
      height: 700px; /*Chiều dài cố định */
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
      
      margin-top: 0%;
      left: 10px;
      top: 0%;
  }

  .auth-form-input {
    background: rgba(255, 255, 255, 0.8);
    border-radius: 5px;
    padding: 2ch;
    margin: 20px;
    width: 1000px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    margin-top: 0%;
    right: 10px;
    top: 0%;
  }

  .auth-form-p {
    background-color: rgba(92, 90, 90, 0.8);
    border-radius: 5px;
    padding: 2ch;
    margin-left: 20px;
    width: 300px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
    
    left: 10px;
    top: 0%;
  }

  .accordion {
    width: 100%;
  }

  .accordion-item {
    width: 100%; /* Đảm bảo item không bị co lại */
}

.accordion-body {
    max-height: 200px; /* Giới hạn chiều cao nội dung bên trong */
    overflow-y: auto; /* Thanh cuộn nếu nội dung quá dài */
}

.history-container {
  position: fixed;
  left: 0;
  top: 50px; /* Cách đỉnh một chút */
  bottom: 0;
  width: 250px;
  overflow-y: auto; /* Nếu nội dung dài, có thể cuộn */
  z-index: 1000;
}

.history-panel {
  height: 100%;
  width: 100%;
  border-radius: 0; /* Bo góc hoặc bỏ nếu cần */
}


.avatar-container {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 60px; /* Điều chỉnh kích thước avatar */
  height: 60px;
  border-radius: 50%; /* Bo tròn khung */
  overflow: hidden; /* Cắt phần thừa nếu có */
  border: 2px solid #fff; /* Viền bo nhẹ */
  background-color: #f8f9fa; /* Màu nền nếu avatar bị lỗi */
}

.avatar-img {
  width: 100%; /* Đảm bảo ảnh vừa khung */
  height: 100%;
  object-fit: cover; /* Giữ tỉ lệ ảnh, cắt nếu cần */
  border-radius: 50%; /* Ảnh tròn */
}


.form-control {
  width: 70%;
  text-align: right;
}

.auth-options {
  display: flex;
  align-items: center;
  gap: 10px; /* Khoảng cách giữa các phần tử */
}


  /* Các phong cách hiện có */
  * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: Arial, sans-serif;
  }

  .avatar-img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border: 2px solid #ddd;
  padding: 3px;
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
            padding-top: 10px;
            width: 100%;
            max-width: 100%;
            display: flex;
        }
  
  .header-container {
    display: flex;
    justify-content: space-between;
    padding: 10px 20px;
    align-items: center;
    width: 100%;
    height: 0%;
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
  </style>