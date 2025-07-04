import { defineStore } from "pinia";
import { ref } from "vue";
import type {
	CoverageSimulatorPayload,
	LosSimulatorPayload,
	LosSimulatorResponse,
	LosSimulatorResponseUpdated,
	OverpassResponse,
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
		fetchOverpassArea(
			polygon: [number, number][],
		): Promise<OverpassResponse[] | null> {
			return new Promise((resolve) => {
				const overpassUrl = "https://overpass-api.de/api/interpreter";

				// Replace with your polygon: space-separated "lat lon" pairs (must form a closed loop)
				const poly = `${polygon.map((coord) => `${coord[1]} ${coord[0]}`).join(" ")} ${polygon[0].join(" ")}`;

				// Overpass QL with filters
				const query = `
				[out:json][timeout:60];
				(
					node["natural"="peak"](poly:"${poly}");
					node["man_made"="communications_tower"](poly:"${poly}");
					way["man_made"="communications_tower"](poly:"${poly}");
					relation["man_made"="communications_tower"](poly:"${poly}");
				);
				out body;
				>;
				out skel qt;
				`;

				fetch(overpassUrl, {
					method: "POST",
					headers: {
						"Content-Type": "application/x-www-form-urlencoded",
					},
					body: `data=${encodeURIComponent(query)}`,
				})
					.then((response) => response.json())
					.then((data) => {
						resolve(data.elements as OverpassResponse[]);
					})
					.catch((error) => {
						console.log("Error fetching Overpass data:", error);
						resolve(null);
					});
				return null;
			});
		},
	},
});

export { useStore };
