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
			return fetch(`${import.meta.env.VITE_API_URL}/predict/coverage`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
			});
		},
		fetchSimulationStatus(
			taskId: string,
			intervalTime = 2000,
		): Promise<Response> {
			return new Promise((resolve, reject) => {
				try {
					const interval = setInterval(async () => {
						const res = await fetch(
							`${import.meta.env.VITE_API_URL}/task/status/${taskId}`,
						);

						if (!res.ok) throw new Error("Error fetching task status");

						const data = await res.json();

						switch (data.status) {
							case "completed":
								clearInterval(interval);
								resolve(res);
								break;
							case "failed":
								clearInterval(interval);
								reject(new Error("Task failed"));
								break;
						}
					}, intervalTime);
				} catch (error) {
					reject(error);
				}
			});
		},
		getMapWmsUrl(taskId: string): string {
			return `${import.meta.env.VITE_GEOSERVER_URL}/RF-SITE-PLANNER/wms?service=WMS&version=1.1.0&transparent=true&request=GetMap&layers=RF-SITE-PLANNER:${taskId}&bbox={bbox-epsg-3857}&width=256&height=256&srs=EPSG:3857&format=image/png`;
		},
	},
});

export { useStore };
