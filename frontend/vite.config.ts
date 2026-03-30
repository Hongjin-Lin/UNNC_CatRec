import { defineConfig } from "vite";
import uni from "@dcloudio/vite-plugin-uni";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [uni()],
  server: {
    port: 5174,
    host: "0.0.0.0"
  },
  base: './',
  define: {
    __API_BASE__: JSON.stringify(process.env.VITE_API_URL || 'http://localhost:8000')
  }
});
