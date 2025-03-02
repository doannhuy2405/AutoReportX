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
        pathRewrite: { '^/api': '' }, // Giữ nguyên tiền tố /api
      },
      // '/gradio': {
      //   target: 'http://192.168.0.136:7860', // Gradio backend
      //   changeOrigin: true,
      //   secure: false,
      //   pathRewrite: { '^/gradio': '' }, // Giữ nguyên tiền tố /gradio
      // },
    },
  },
  transpileDependencies: true,
});