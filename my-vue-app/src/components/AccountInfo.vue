<template>
    <div class="body"> 
      <div class="content">
        <div class="container-fluid">
          <div class="header-container" style="text-align: center;">
            <h1 style="font-size: 2em;">AutoReportX</h1> 
          </div>   
  
          <br><br>
  
          <!-- Nội dung sẽ được thay đổi theo ngôn ngữ -->
          <div id="content">
            <div>
              <h2>{{ currentTranslations.title }}</h2><br><br>
              <p>{{ currentTranslations.search }}</p><br>
              <p>{{ currentTranslations.extraction }}</p><br>
              <p>{{ currentTranslations.assessment }}</p><br>
              <p>{{ currentTranslations.reporting }}</p><br>
              <h4>{{ currentTranslations.conclusion }}</h4><br><br>
              
            </div>  
            <div class="header-logo">
                    <img src="../assets/logo.png" alt="AutoReportX Logo">
                </div>
          </div>
        </div>

        <div class="tagline-box text-center">
          {{ currentTranslations.tagline }}
        </div>
      </div>
      <br><br>
  
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
  </template>
  
  <script setup>
//   import { RouterLink } from 'vue-router';
  import {ref, computed } from 'vue';
  import { inject } from "vue";
  
    // Declare reactive variables

  const language = ref(inject("language"));
//   const toggleLanguage = inject("toggleLanguage");
  // Declare the translations object
  const translations = {
    vi: {
      login: "Đăng Nhập",
      register: "Đăng Ký",
      title: "Trong thời đại bùng nổ thông tin, việc tìm kiếm, trích xuất và đánh giá nội dung một cách chính xác là yếu tố then chốt giúp doanh nghiệp và cá nhân đưa ra quyết định đúng đắn. AutoReportX ra đời như một giải pháp tiên phong, ứng dụng công nghệ hiện đại để xử lý dữ liệu một cách thông minh, nhanh chóng và hiệu quả.",
      search: "🔎 Tìm kiếm tối ưu: Hệ thống tích hợp thuật toán tiên tiến, giúp truy xuất thông tin với tốc độ vượt trội và độ chính xác cao.",
      extraction: "📑 Trích xuất thông minh: Xác định và tổng hợp nội dung quan trọng từ nhiều nguồn, hỗ trợ phân tích chuyên sâu.",
      assessment: "📊 Đánh giá thông tin: Ứng dụng AI để phân tích tính xác thực, mức độ tin cậy của dữ liệu.",
      reporting: "📝 Tạo báo cáo tự động: Biến dữ liệu thô thành báo cáo trực quan, hỗ trợ ra quyết định một cách nhanh chóng.",
      conclusion: "Với giao diện thân thiện, hiệu năng mạnh mẽ và khả năng xử lý dữ liệu vượt trội, AutoReportX không chỉ giúp tối ưu hóa quy trình làm việc mà còn nâng tầm khả năng khai thác tri thức, tạo ra giá trị thực tiễn cho người dùng.",
      tagline: "Hãy để công nghệ dẫn lối tri thức – Trải nghiệm sự khác biệt cùng AutoReportX!",
      contactTitle: "Mọi chi tiết xin vui lòng liên hệ:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 Hoặc 0559-285-596",
      contactAddress: "📍 Địa chỉ: Trường Công nghệ Thông tin & Truyền thông"
    },
    en: {
      login: "Login",
      register: "Sign Up",
      title: "In the era of information explosion, accurate search, extraction, and evaluation of content are key factors that enable businesses and individuals to make well-informed decisions. AutoReportX emerges as a pioneering solution, leveraging cutting-edge technology to process data intelligently, efficiently, and rapidly.",
      search: "🔎 Optimized Search: The system integrates advanced algorithms to retrieve information with exceptional speed and accuracy.",
      extraction: "📑 Smart Extraction: Identifies and synthesizes key content from multiple sources, supporting in-depth analysis.",
      assessment: "📊 Information Assessment: Utilizes AI to analyze authenticity and assess the reliability of data.",
      reporting: "📝 Automated Reporting: Transforms raw data into intuitive reports, facilitating quick and informed decision-making.",
      conclusion: "With a user-friendly interface, powerful performance, and superior data processing capabilities, AutoReportX not only optimizes workflows but also enhances knowledge extraction, creating real-world value for users.",
      tagline: "Let technology pave the way to knowledge – Experience the difference with AutoReportX!",
      contactTitle: "For further details, please contact:",
      contactEmail: "📧 Email: yb2207580@student.ctu.edu.vn",
      contactPhone: "📞 Hotline: 0848-077-996 or 0559-285-596",
      contactAddress: "📍 Address: College of Information and Communication Technology, Can Tho University"
    }
  };
  

  
  // Computed property to get the current translations based on the selected language
  const currentTranslations = computed(() => translations[language.value]);
  
  // Methods for handling language change

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


</style>
  