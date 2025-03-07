import { initializeApp } from "firebase/app";
import { getAuth, signInWithPopup, GoogleAuthProvider, FacebookAuthProvider } from "firebase/auth";

// Cấu hình Firebase
const firebaseConfig = {
  apiKey: "AIzaSyA65qkBiK7ZWUWMpLs_BTIv7lfjrGB1hd8",
  authDomain: "autoreportx-3357d.firebaseapp.com",
  projectId: "autoreportx-3357d",
  storageBucket: "autoreportx-3357d.firebasestorage.app",
  messagingSenderId: "995040790307",
  appId: "1:995040790307:web:93c25b6be5909f8dcc6e96",
};


// Khởi tạo Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Khởi tạo provider cho Google & Facebook
const googleProvider = new GoogleAuthProvider();
const facebookProvider = new FacebookAuthProvider();

// Xuất các hàm cần dùng
export { auth, googleProvider, facebookProvider, signInWithPopup };
