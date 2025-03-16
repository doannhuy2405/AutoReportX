const dotenv = require('dotenv');
dotenv.config();

const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:5000', // Backend mặc định
        changeOrigin: true,
        secure: false,
        pathRewrite: { '^/api': '' }, // Xóa nguyên tiền tố /api
      },
    },
  },
  transpileDependencies: true,
});