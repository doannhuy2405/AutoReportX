<!-- <script setup>
import { ref, onMounted } from "vue";
import api from "../api";

const items = ref([]);

const fetchItems = async () => {
  try {
    const response = await api.get("/items/");
    items.value = response.data;
  } catch (error) {
    console.error("Lỗi:", error);
  }
};

onMounted(fetchItems);
</script>

<template>
  <div>
    <h2>Danh sách Item</h2>
    <ul>
      <li v-for="item in items" :key="item._id">
        <strong>{{ item.name }}</strong>: {{ item.description }}
      </li>
    </ul>
  </div>
</template> -->
