import axios from "axios";

const API_BASE_URL = "http://0.0.0.0:5000"; // URL của backend

export const getItems = async (itemId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/items/${itemId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching item:", error);
    return null;
  }
};

console.log("All env variables:", import.meta.env);
console.log("OpenAI API Key:", import.meta.env.VITE_OPENAI_API_KEY);

