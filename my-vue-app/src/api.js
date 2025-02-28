import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000"; // URL của backend

export const getItems = async (itemId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/items/${itemId}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching item:", error);
    return null;
  }
};
