<template>
    <div class="body">
        <div class="container">
            <h1 class="title">Nâng cấp gói của bạn</h1>

            <div class="auth-options">
                <select id="language-select" v-model="language"  @change="toggleLanguage">
                <option value="vi">Tiếng Việt VN</option>
                <option value="en">English US</option>
              </select>
            </div>


            <div class="card-wrapper">
                <div class="card" v-for="plan in plans" :key="plan.title" :class="{ active: plan.active }">
                <h2>{{ plan.title }}</h2>
                <p class="price">{{ plan.price }}</p>
                <p>{{ plan.description }}</p>
                <button class="button" @click="switchPlan(plan)">Chuyển sang {{ plan.buttonText }}</button>
                <ul>
                    <li v-for="feature in plan.features" :key="feature">{{ feature }}</li>
                </ul>
                </div>
            </div>
        </div>
    </div>
  </template>
  
  <script setup>
  import { ref, inject } from 'vue';
  import { useRouter } from 'vue-router';

  const router = useRouter() ;
  const language = ref(inject("language"));
  const toggleLanguage = inject("toggleLanguage");

  const translations = {

  }
  
  const plans = ref([
    {
      title: 'Miễn phí',
      price: '$0 USD/tháng',
      description: 'Cùng khám phá sự hỗ trợ của AI trong các công việc hàng ngày của bạn',
      buttonText: 'Kế hoạch hiện tại của bạn',
      features: [
        
      ],
      active: false
    },
    {
      title: 'Plus',
      price: '$20 USD/tháng',
      description: 'Nâng cao năng suất và tính sáng tạo với quyền truy cập mở rộng',
      buttonText: 'Chuyển sang Plus',
      features: [
       
      ],
      active: true
    },
    {
      title: 'Pro',
      price: '$200 USD/tháng',
      description: 'Khai thác tối đa OpenAI với cấp độ truy cập cao nhất',
      buttonText: 'Chuyển sang Pro',
      features: [
        
      ],
      active: false
    }
  ]);
  
  const switchPlan = (plan) => {
    plans.value.forEach(p => p.active = false);
    plan.active = true;
  };
  </script>
  
  <style scoped>

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

  .container {
    color: white;
    padding: 20px;
    border-radius: 8px;
  }
  
  .title {
    text-align: center;
    margin-bottom: 20px;
  }
  
  .card-wrapper {
    display: flex;
    justify-content: space-around;
  }
  
  .card {
    background-color: #2b2b2b;
    border: 1px solid #444;
    border-radius: 8px;
    padding: 20px;
    width: 30%;
    text-align: center;
    transition: transform 0.3s;
  }
  
  .card.active {
    border: 2px solid #1da1f2;
  }
  
  .price {
    font-size: 24px;
    font-weight: bold;
  }
  
  .button {
    background-color: #1da1f2;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    cursor: pointer;
    transition: opacity 0.2s;
  }
  
  .button:hover {
    opacity: 0.8;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
    text-align: left;
  }
  </style>