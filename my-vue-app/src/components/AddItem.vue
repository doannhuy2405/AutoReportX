<!-- <script setup>
import { ref } from "vue";
import axios from "axios";  

const username = ref("")
const password = ref("")
const message = ref("")

const handleLogin = async () => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/api/login", {
      username: username.value,
      password: password.value
    })
    message.value = response.data.message
  } catch (error) {
    message.value = "Đăng nhập thất bại: " + error.response.data.detail
  }
}
</script>

<template>
  <div class="auth-form">
    <h2>Đăng nhập</h2>
    <form @submit.prevent="handleLogin">
      <div class="form-group">
        <label for="username">Tên đăng nhập</label>
        <input type="text" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="password">Mật khẩu</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Đăng nhập</button>
    </form>
    <p>{{ message }}</p>
  </div>
</template> -->
