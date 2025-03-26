import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig({
	plugins: [vue()],
	server: {
		port: 8080,
		host: "0.0.0.0",
	},
});
