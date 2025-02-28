const { MongoClient } = require('mongodb');

const uri = "mongodb://localhost:27017"; // Kết nối đến MongoDB trên localhost
const client = new MongoClient(uri);

async function connectDB() {
    try {
        await client.connect();
        console.log("✅ Kết nối MongoDB thành công!");
        return client.db("myDatabase"); // Thay "myDatabase" bằng tên database của bạn
    } catch (error) {
        console.error("❌ Kết nối MongoDB thất bại:", error);
    }
}

module.exports = connectDB;
