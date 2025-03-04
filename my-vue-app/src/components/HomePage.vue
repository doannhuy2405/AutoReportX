<template>
    <div class="body">
      <div class="content">
        <div class="container">
          <div class="header-container">
            <div style="flex: 1; text-align: center;">
              <h1 style="padding-left: 150px; font-size: 4em;">AutoReportX</h1>
            </div>
  
            <div class="auth-options" style="display: flex; align-items: center; gap: 15px;">
              <select id="language-select" @change="toggleLanguage" v-model="language">
                <option value="vi">Tiếng Việt VN</option>
                <option value="en">English US</option>
              </select>

              <div class="dropdown">
                <button class="btn btn-secondary dropdown-toggle avatar-btn" type="button" data-bs-toggle="dropdown" aria-expanded="false">
                  <div class="avatar-container">
                    <img :src="user?.avatar || defaultAvatar" class="rounded-circle avatar-img" alt="User Avatar">
                  </div>
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                  <li class="dropdown-header text-center">
                    <div class="avatar-container" style="width: 155px; height: 155px;">
                      <img :src="user?.avatar || defaultAvatar" class="rounded-circle avatar-img" alt="User Avatar">
                    </div>
                    <p class="fw-bold">{{ user.name }}</p>
                  </li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" href="#" @click="goToAccountInfo" >{{ translations[language].accountInfo }}</a></li>
                  <li><a class="dropdown-item" href="#">{{ translations[language].upgradePlan }}</a></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item text-danger" href="#" @click="logout">{{ translations[language].logout }}</a></li>
                </ul>
              </div>
            </div>
          </div>
        </div>

        <div class="home-page">
          <h1>Open Deep Researcher - AI Research Assistant</h1>
          <input v-model="userQuery" placeholder="Nhập câu hỏi của bạn..." />
          <button @click="runGradio" :disabled="loading">
            {{ loading ? 'Đang tải...' : 'Bắt đầu tìm kiếm' }}
          </button>
          <div v-if="result">
            <h2>Kết quả:</h2>
            <pre>{{ result }}</pre>
            <!-- Nút tải về file -->
            <button @click="downloadReport('doc')" :disabled="!result">Tải về Word</button>
            <button @click="downloadReport('pdf')" :disabled="!result">Tải về PDF</button>
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

// Hàm tạo báo cáo tự động
const userQuery = ref('');
const result = ref('');
const loading = ref(false);

  const runGradio = async () => {
  if (!userQuery.value.trim()) {
    alert('Vui lòng nhập câu hỏi!');
    return;
  }

  loading.value = true;
  result.value = '';

  try {
    const response = await fetch('/api/predict/', {  // Sử dụng proxy /api
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_query: userQuery.value, // user_query
        iteration_limit: 1,         // iteration_limit
      }),
    });

    if (!response.ok) {
      throw new Error(`Lỗi HTTP: ${response.status}`);
    }

    const data = await response.json();
    result.value = data.data;
  } catch (error) {
    console.error('Lỗi khi gọi API:', error);
    result.value = 'Đã xảy ra lỗi khi tải kết quả.';
  } finally {
    loading.value = false;
  }
};

// Hàm dowload file 

const downloadReport = async (fileType) => {
  if (!result.value) {
    alert('Không có kết quả để tải về!');
    return;
  }
  console.log(fileType, result.value)

  try {
    const response = await fetch('/api/download-report/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        content: result.value,
        file_type: fileType,
      }),
    });

    if (!response.ok) {
      throw new Error(`Lỗi HTTP: ${response.status}`);
    }

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileType === 'doc' ? 'report.docx' : 'report.pdf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  } catch (error) {
    console.error('Lỗi khi tải file:', error);
    alert('Đã xảy ra lỗi khi tải file.');
  }
};

// const downloadReport = async (fileType) => {
//   if (!result.value) {
//     alert('Không có kết quả để tải về!');
//     return;
//   }

//   try {
//     const response = await fetch('/api/download-report/', {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json',
//       },
//       body: JSON.stringify({
//         content: result.value, // Nội dung từ kết quả
//         file_type: fileType,   // Loại file: 'doc' hoặc 'pdf'
//       }),
//     });

//     if (!response.ok) {
//       throw new Error(`Lỗi HTTP: ${response.status}`);
//     }

//     // Xử lý tải file
//     const blob = await response.blob();
//     const url = window.URL.createObjectURL(blob);
//     const a = document.createElement('a');
//     a.href = url;
//     a.download = fileType === 'doc' ? 'report.docx' : 'report.pdf';
//     document.body.appendChild(a);
//     a.click();
//     document.body.removeChild(a);
//     window.URL.revokeObjectURL(url);
//   } catch (error) {
//     console.error('Lỗi khi tải file:', error);
//     alert('Đã xảy ra lỗi khi tải file.');
//   }
// };


  const user = ref({
    avatar: "",  // Ảnh mặc định (nếu chưa có dữ liệu)
    name: "Người dùng"
  });

  const defaultAvatar = "../assets/default_avatar.png";

  const router = useRouter() ;


  // Gọi API lấy thông tin user
  const fetchUser = async () => {
    try {
      const response = await fetch("http://localhost:5000/user");
      const data = await response.json();
      if (data) {
        user.value = data; // Gán dữ liệu từ API vào user
      }
    } catch (error) {
      console.error("Lỗi khi lấy dữ liệu người dùng:", error);
    }
  };

  // Gọi API khi component được mount
  onMounted(fetchUser);

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
      logout: "Đăng xuất",
      user: "Người dùng"
    },
    en: {
      contactTitle: "For further details, please contact:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 or 0559-285-596",
      contactAddress: "📍 Address: College of Information and Communication Technology, Can Tho University",
      accountInfo: "Account Information",
      upgradePlan: "Upgrade Plan",
      logout: "Logout",
      user: "User"
    }
  };

  const goToAccountInfo = () => {
    router.push("/accountinfo");
  };
  
  </script>
  
  <style scoped>

.home-page {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

input {
  background: rgba(255, 255, 255, 0.8);
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  font-size: 16px;
}

button {
  background: rgba(255, 255, 255, 0.8);
  padding: 10px 20px;
  font-size: 16px;
  margin: 5px;
  cursor: pointer;
}


pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  background: rgba(255, 255, 255, 0.8);
  padding: 10px;
  border-radius: 5px;
  text-align: left;
}

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