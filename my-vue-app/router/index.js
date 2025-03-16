// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';

// Import các component bạn muốn chuyển hướng tới
import UserInterface from '@/components/UserInterface.vue';
import UserLogin from '@/components/UserLogin.vue';
import UserSignUp from '@/components/UserSignUp.vue';
import HomePage from '@/components/HomePage.vue';
import AccountInfo from '@/components/AccountInfo.vue';

// Tạo danh sách các routes
const routes = [
  {
    path: '/',
    name: 'interface',
    component: UserInterface
  },
  {
    path: '/login',
    name:'login',
    component: UserLogin
  },
  {
    path: '/signup',
    name: 'signup',
    component: UserSignUp
  },
  {
    path: '/home',
    name: 'homepage',
    component: HomePage
  },
  {
    path: '/accountinfo',
    name: 'accountinfo',
    component: AccountInfo
  }
];

// Tạo một instance của Vue Router
const router = createRouter({
  history: createWebHistory(), // sử dụng history mode (không có dấu # trong URL)
  routes // định nghĩa các routes
});

export default router;
