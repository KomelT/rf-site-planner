import { defineStore } from "pinia";
import { ref } from "vue";
import type { CoverageSimulatorPayload } from "./types.ts";

const useStore = defineStore("store", {
	state() {
		return {
			mobileMenuOpen: ref(true),
			mapStyle: ref("openstreetmap"),
		};
	},
	actions: {
		fetchCoverageSimulation(payload: CoverageSimulatorPayload) {
			return fetch(`${import.meta.env.VITE_API_URL}/predict`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
			});
		},
	},
});

export { useStore };
