import { defineStore } from "pinia";
import { ref } from "vue";
import type {
	CoverageSimulatorPayload,
	LosSimulatorPayload,
	LosSimulatorResponse,
	LosSimulatorResponseUpdated,
} from "./types.ts";

const useStore = defineStore("store", {
	state() {
		return {
			mobileMenuOpen: ref(true),
			mapStyle: ref("openstreetmap"),
			chart: ref({
				// biome-ignore lint/suspicious/noExplicitAny: <explanation>
				data: [] as { name: string; data: any[] }[],
				options: {},
				show: false,
				rx_signal_power: ref<LosSimulatorResponse["rx_signal_power"]>(0),
				path: {
					obstructed: ref<LosSimulatorResponse["path"]["obstructed"]>(false),
					message: ref<LosSimulatorResponse["path"]["message"]>(""),
					obstructions: ref<LosSimulatorResponse["path"]["obstructions"]>([]),
				},
			}),
			centralNodeTable: ref({
				data: [] as LosSimulatorResponseUpdated[],
				options: {},
				show: false,
			}),
		};
	},
	actions: {
		fetchLosSimulation(payload: LosSimulatorPayload) {
			return fetch(`${import.meta.env.VITE_API_URL}/predict/los`, {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify(payload),
			});
		},
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
		): Promise<{ status: string; data: string }> {
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
								resolve(data);
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
