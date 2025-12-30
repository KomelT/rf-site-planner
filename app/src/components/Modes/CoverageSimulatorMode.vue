<template>
	<div>
		<div class="grid grid-cols-7 gap-2 mt-3 items-end">
			<div class="col-span-5">
				<DropDown title="Simulations" :options="simulationsOptions" :selected="simulationOption"
					@update:selected="changeCurrentSimulation" :deleteBtn="true" @delete:option="removeSimulation" />
			</div>
			<div class="col-span-2">
				<Button text="Add new" @click="addSimulation()" class="w-full" />
			</div>
		</div>
		<form>
			<div class="mt-3 flex flex-row gap-2">
				<InputText title="Simulation title" v-model:value="simulation.title" placeholder="Simulation name" />
				<InputNumber title="Opacity" v-model:value="simulation.opacity" @change="updateOpacity" :min="0" :max="1"
					:step="0.1" placeholder="Opacity" />
			</div>
			<ModeDataAccordian title="Transmitter options" :markerColor="simulation.id"
				v-model:showSection="showSections.transmitter">
				<div class="flex flex-row gap-2">
					<InputNumber title="Latitude" :min="-90" :max="90" v-model:value="simulation.lat" />
					<InputNumber title="Longtitude" :min="-180" :max="180" v-model:value="simulation.lon" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<Button :text="pickingLocation ? 'Cancel picking' : 'Pick location on map'" @click="addLocationListener"
						:class="pickingLocation ? 'bg-red-600' : ''" />
					<Button text="Fly to coordinates" @click="flyToCurrentMarker" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Power (dBm)" :min="1" v-model:value="simulation.tx_power" />
					<InputNumber title="Frequency (MHz)" :min="20" :max="30000" v-model:value="simulation.frequency_mhz" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" :min="1" v-model:value="simulation.tx_height" />
					<InputNumber title="Gain (dBi)" :min="0" v-model:value="simulation.tx_gain" />
					<InputNumber title="Loss (dB)" :min="0" v-model:value="simulation.tx_loss" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Receiver options" v-model:showSection="showSections.receiver">
				<div class="flex flex-row gap-2">
					<InputNumber title="Max Sensitivity (dBm)" :max="0" v-model:value="simulation.max_dbm" />
					<InputNumber title="Min Sensitivity (dBm)" :max="0" v-model:value="simulation.min_dbm" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" :min="1" v-model:value="simulation.rx_height" />
					<InputNumber title="Loss (dB)" :min="0" v-model:value="simulation.rx_loss" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Enviroment" v-model:showSection="showSections.enviroment">
				<div class="flex flex-row gap-2">
					<DropDown title="Radio climate" :options="climateOptions" v-model:value="simulation.radio_climate" />
					<DropDown title="Polarization" :options="polarizationOptions" v-model:value="simulation.polarization" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Clutter height (m)" :min="0" v-model:value="simulation.clutter_height" />
					<InputNumber title="Ground dielectric (V/m)" :min="1" v-model:value="simulation.ground_dielectric" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Ground conductivity (S/m)" :min="0" v-model:value="simulation.ground_conductivity" />
					<InputNumber title="Atmospheric bending (N)" :min="0" v-model:value="simulation.atmosphere_bending" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Simulation options" v-model:showSection="showSections.simulationsOptions">
				<div class="flex flex-row gap-2">
					<InputNumber title="Situation fraction (%)" :min="1" :max="100"
						v-model:value="simulation.situation_fraction" />
					<InputNumber title="Time fraction (%)" :min="1" :max="100" v-model:value="simulation.time_fraction" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Max range (km)" :min="1" :max="300" v-model:value="simulation.radius" />
					<Toggle title="High resolution" v-model:value="simulation.high_resolution" />
					<Toggle title="ITM mode" v-model:value="simulation.itm_mode" />
				</div>
			</ModeDataAccordian>
			<div class="flex flex-row justify-end mt-3">
				<Button text="Run simulation" @click="runSimulation" :loading="isSimulationRunning"
					:disabled="isSimulationRunning" />
			</div>
		</form>
	</div>
</template>
<script setup lang="ts">
import { useMap } from "@indoorequal/vue-maplibre-gl";
import { Marker, Popup, type Subscription } from "maplibre-gl";
import {
	type ComputedRef,
	type Ref,
	computed,
	onMounted,
	onBeforeUnmount,
	ref,
	watch,
} from "vue";
import { useNotificationStore } from "../../stores/notification";
import { useStore } from "../../stores/store";
import {
	type CoverageSimulatorSite,
	climateOptions,
	polarizationOptions,
} from "../../stores/types";
import Button from "../Inputs/Button.vue";
import DropDown from "../Inputs/DropDown.vue";
import InputNumber from "../Inputs/InputNumber.vue";
import InputText from "../Inputs/InputText.vue";
import ModeDataAccordian from "./ModeDataAccordian.vue";
import { isMobileDevice, randomHexColor } from "../../utils";
import { onBeforeMount } from "vue";
import Toggle from "../Inputs/Toggle.vue";

const map = useMap();
const store = useStore();
const notificationStore = useNotificationStore();

const markers = ref<Marker[]>([]);
const pickingLocation = ref(false);
const isSimulationRunning = ref(false);
const locationPickerSubscription = ref<Subscription | null>(null);

const showSections = ref({
	transmitter: true,
	receiver: false,
	enviroment: false,
	simulationsOptions: false,
});

const defaultSimulationValues: ComputedRef<CoverageSimulatorSite> = computed(
	() => {
		return {
			id: randomHexColor(),
			title: `Simulation ${store.coverSimModeData.simulations.length + 1}`,
			opacity: 0.7,
			lat: 45.85473269336,
			lon: 13.72616645611,
			tx_power: 27,
			frequency_mhz: 868.5,
			tx_height: 2,
			tx_gain: 5,
			tx_loss: 2,
			rx_gain: 5,
			rx_height: 2,
			rx_loss: 2,
			radio_climate: "continental_temperate",
			polarization: "vertical",
			clutter_height: 0.9,
			ground_dielectric: 15,
			ground_conductivity: 0.005,
			atmosphere_bending: 301,
			situation_fraction: 95,
			time_fraction: 95,
			radius: 30,
			high_resolution: false,
			colormap: "plasma",
			min_dbm: -153,
			max_dbm: -80,
			itm_mode: true,
		};
	},
);

if (store.coverSimModeData.simulations.length === 0) {
	store.coverSimModeData.simulations.push(defaultSimulationValues.value);
}

const simulationOption = computed(() => {
	return {
		id: simulation.value.id,
		title: simulation.value.title,
	};
});

const simulationsOptions = computed(() => {
	return store.coverSimModeData.simulations.map((simulation) => ({
		id: simulation.id,
		title: simulation.title,
	}));
});

const simulation: Ref<CoverageSimulatorSite> = ref(store.coverSimModeData.simulations[0]);

// watch for current simulation changes
watch(
	store.coverSimModeData.simulations,
	(_sim) => {
		if (!map.isLoaded || !map.map) return;

		markers.value.forEach((marker) => marker.remove());
		markers.value = [];

		for (const sim of store.coverSimModeData.simulations.values()) {
			markers.value.push(new Marker({
				color: sim.id,
			})
				.setLngLat([sim.lon, sim.lat])
				.setPopup(
					new Popup({ offset: 25 }).setHTML(
						`<h3><b>${sim.title}</b></h3><p>Power: ${sim.tx_power} W</p><p>Frequency: ${sim.frequency_mhz} MHz</p>`,
					),
				)
				.addTo(map.map));
		}
	},
	{ immediate: true, deep: true },
);

async function runSimulation() {
	if (!map.isLoaded || !map.map) return;

	if (isMobileDevice()) store.toggleMobileMenu();

	isSimulationRunning.value = true;
	notificationStore.addNotification({
		type: "info",
		message: "Starting simulation...",
		title: "Coverage Simulation",
		hideAfter: 5000,
	});

	try {
		const predictRes = await store.fetchCoverageSimulation({
			...simulation.value,
		});

		if (!predictRes.ok)
			throw new Error(`Failed to start prediction: ${await predictRes.text()}`);

		const predictData = await predictRes.json();
		const taskId = predictData.task_id;

		const data = JSON.parse((await store.fetchSimulationStatus(taskId, 1000)).data);

		store.coverSimModeData.legend.data = data.legend;
		store.coverSimModeData.legend.show = true;

		notificationStore.addNotification({
			type: "success",
			message: "Simulation completed successfully.",
			title: "Coverage Simulation",
			hideAfter: 5000,
		});

		if (!map.isLoaded || !map.map) return;

		if (simulation.value.wmsUrl) {
			const url = new URL(simulation.value.wmsUrl);
			await store.deleteCoverageSimulation(url.searchParams.get("layers")?.split(":")[1] || "");
		}

		if (map.map.getSource(`coverage-${simulation.value.id}`)) {
			map.map.removeLayer(`coverage-${simulation.value.id}`);
			map.map.removeSource(`coverage-${simulation.value.id}`);
		}

		simulation.value.wmsUrl = store.getMapWmsUrl(taskId);

		map.map.addSource(`coverage-${simulation.value.id}`, {
			type: "raster",
			tiles: [simulation.value.wmsUrl],
			tileSize: 256,
		});
		map.map.addLayer({
			id: `coverage-${simulation.value.id}`,
			type: "raster",
			source: `coverage-${simulation.value.id}`,
			paint: {
				"raster-opacity": simulation.value.opacity,
			},
		});

	} catch (error) {
		notificationStore.addNotification({
			type: "error",
			message: "Simulation failed!",
			title: "Coverage Simulation",
			hideAfter: 5000,
		});
		console.error("Error during simulation:", error);
	} finally {
		isSimulationRunning.value = false;
	}
}

// add location listener for selecting location on map
function addLocationListener() {
	if (!map.isLoaded || !map.map) return;

	if (isMobileDevice()) store.toggleMobileMenu();

	if (pickingLocation.value) {
		pickingLocation.value = false;
		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
		return;
	}

	pickingLocation.value = true;

	locationPickerSubscription.value = map.map.on("click", (e) => {
		const { lng, lat } = e.lngLat;
		pickingLocation.value = false;
		simulation.value.lat = Number(lat.toFixed(10));
		simulation.value.lon = Number(lng.toFixed(10));

		markers.value.find((marker) => marker.getElement().style.color === simulation.value.id)?.setLngLat([
			Number(lng.toFixed(10)),
			Number(lat.toFixed(10)),
		]);

		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
	});
}

function flyToCurrentMarker() {
	if (!map.isLoaded || !map.map) return;

	if (isMobileDevice()) store.toggleMobileMenu();

	map.map.flyTo({
		center: [simulation.value.lon, simulation.value.lat],
		zoom: 15,
	});
}

function flyToSimulationsExtent() {
	if (!map.isLoaded || !map.map) return;

	const sims = store.coverSimModeData.simulations;
	if (!sims.length) return;

	let minLat = 90;
	let maxLat = -90;
	let minLon = 180;
	let maxLon = -180;

	for (const sim of sims) {
		const radiusKm = Math.max(0, sim.radius ?? 0);
		const lat = sim.lat;
		const lon = sim.lon;
		const latRad = (lat * Math.PI) / 180;
		const kmPerDegLat = 110.574;
		const kmPerDegLon = Math.max(0.0001, 111.320 * Math.cos(latRad));
		const deltaLat = radiusKm / kmPerDegLat;
		const deltaLon = radiusKm / kmPerDegLon;

		minLat = Math.min(minLat, lat - deltaLat);
		maxLat = Math.max(maxLat, lat + deltaLat);
		minLon = Math.min(minLon, lon - deltaLon);
		maxLon = Math.max(maxLon, lon + deltaLon);
	}

	minLat = Math.max(-90, minLat);
	maxLat = Math.min(90, maxLat);
	minLon = Math.max(-180, minLon);
	maxLon = Math.min(180, maxLon);

	if (minLat === maxLat && minLon === maxLon) {
		map.map.flyTo({
			center: [minLon, minLat],
			zoom: 15,
		});
		return;
	}

	map.map.fitBounds(
		[
			[minLon, minLat],
			[maxLon, maxLat],
		],
		{
			padding: 40,
			maxZoom: 15,
		},
	);
}

function addSimulation() {
	store.coverSimModeData.simulations.push(defaultSimulationValues.value);
	setTimeout(() => {
		simulation.value = store.coverSimModeData.simulations[store.coverSimModeData.simulations.length - 1];
	}, 1)
}

function changeCurrentSimulation(sim: { id: string; title: string }) {
	const index = store.coverSimModeData.simulations.findIndex(
		(simulation) => simulation.id === sim.id,
	);
	if (index !== -1) {
		simulation.value = store.coverSimModeData.simulations[index];
	}

	// @ts-ignore
	markers.value.find((marker) => marker.getElement().style.color === simulation.value.id)?.setLngLat([
		Number(simulation.value.lon.toFixed(10)),
		Number(simulation.value.lat.toFixed(10)),
	]);
}

function removeSimulation(id: string) {
	if (!map.isLoaded || !map.map) return;

	const index = store.coverSimModeData.simulations.findIndex((sim) => sim.id === id);
	if (index !== -1) {
		if (store.coverSimModeData.simulations[index].wmsUrl) {
			const url = new URL(store.coverSimModeData.simulations[index].wmsUrl)
			store.deleteCoverageSimulation(url.searchParams.get("layers")?.split(":")[1] || "");
		}
		store.coverSimModeData.simulations.splice(index, 1);
	}

	if (store.coverSimModeData.simulations.length === 0) {
		store.coverSimModeData.simulations.push(defaultSimulationValues.value);
		simulation.value = store.coverSimModeData.simulations[0];
	}

	try {
		map.map?.removeLayer(`coverage-${id}`);
		map.map?.removeSource(`coverage-${id}`);
	} catch (e) {
		console.error(`Error removing layer: ${id}`);
	}
}

function updateOpacity() {
	if (!map.map) return;

	map.map.setPaintProperty(`coverage-${simulation.value.id}`, "raster-opacity", simulation.value.opacity);
}

onBeforeMount(() => {
	store.coverSimModeData.simulations.forEach(async (sim) => {
		if (!sim.wmsUrl) return;

		const url = new URL(sim.wmsUrl);
		url.searchParams.set("bbox", "1531186.5506086498,5762740.436476007,1536078.520418901,5767632.406286258");

		const py = await (await fetch(url)).body?.getReader().read()

		if (!py?.value?.byteLength || py?.value?.byteLength < 600) return;

		map.map?.addSource(`coverage-${sim.id}`, {
			type: "raster",
			tiles: [sim.wmsUrl],
			tileSize: 256,
		});

		map.map?.addLayer({
			id: `coverage-${sim.id}`,
			type: "raster",
			source: `coverage-${sim.id}`,
			paint: {
				"raster-opacity": sim.opacity,
			},
		});

		store.coverSimModeData.legend.show = true;
	});
});

onMounted(() => {
	flyToSimulationsExtent();
});

// remove all uneded stuff before umount
onBeforeUnmount(() => {
	markers.value.forEach((marker) => marker.remove());

	locationPickerSubscription.value?.unsubscribe();
	locationPickerSubscription.value = null;

	store.coverSimModeData.legend.show = false;

	try {
		map.map?.removeLayer(`coverage-${simulation.value.id}`);
		map.map?.removeSource(`coverage-${simulation.value.id}`);
	} catch (e) {
		console.error(`Error removing layer: ${simulation.value.id}`);
	}

	for (const simulation of store.coverSimModeData.simulations) {
		try {
			map.map?.removeLayer(`coverage-${simulation.id}`);
			map.map?.removeSource(`coverage-${simulation.id}`);
		} catch (e) {
			console.error(`Error removing layer: ${simulation.id}`);
		}
	}
});
</script>
