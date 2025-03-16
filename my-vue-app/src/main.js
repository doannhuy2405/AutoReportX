import { createApp } from 'vue'
import App from './App.vue'

import router from '../router'; // Nhập router vào

const vueApp = createApp(App);

vueApp.use(router); // Sử dụng Vue Router
vueApp.mount('#app');

// Firebase
import { initializeApp } from "firebase/app";
import { getAuth, signInWithPopup, GoogleAuthProvider } from "firebase/auth";

// Cấu hình Firebase
const firebaseConfig = {
  apiKey: "",
  authDomain: "",
  projectId: "autoreportx-3357d",
  storageBucket: "",
  messagingSenderId: "",
  appId: "",
};


// Khởi tạo Firebase
const firebaseApp = initializeApp(firebaseConfig);
const auth = getAuth(firebaseApp);

// Khởi tạo provider cho Google & Facebook
const googleProvider = new GoogleAuthProvider();

// Xuất các hàm cần dùng
export { auth, googleProvider, signInWithPopup };
