import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";

// https://vite.dev/config/
export default defineConfig({
	plugins: [vue(), tailwindcss()],
	server: {
		port: 8080,
		host: "0.0.0.0",
	},
});
