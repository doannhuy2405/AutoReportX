<template>
  <router-view>
  </router-view>
</template>
  
  <script setup>
  import { RouterView, useRouter } from 'vue-router';
  import { provide, ref } from "vue";


  const isLoggedIn = ref(false);
  const router = useRouter();

  const login = () => {
    isLoggedIn.value=true;
    router.push("/home"); //Chuyển hướng sau khi đăng nhập thành công
  }

  //Cung cấp cho component con
  provide("isLoggedIn", isLoggedIn);
  provide("login", login);


  const language = ref("vi"); // Ngôn ngữ mặc định là tiếng Anh

  const currentPage = ref ('interface');
  provide('currentPage', currentPage); //cung cấp currentPage để các component có thể thay đổi

  const toggleLanguage = () => {
    language.value = language.value === "en" ? "en" : "vi";
    console.log(language.value)
  };

  provide("language", language);
  provide("toggleLanguage", toggleLanguage);

  </script>
  
  <style>
  
  </style>