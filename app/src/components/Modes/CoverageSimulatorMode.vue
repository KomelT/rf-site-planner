<template>
	<div>
		<div class="grid grid-cols-7 gap-2 mt-3 items-end">
			<div class="col-span-5">
				<DropDown title="Simulations" :options="simulationsOptions" @update:selected="changeCurrentSimulation"
					:deleteBtn="true" @delete:option="removeSimulation" />
			</div>
			<div class="col-span-2">
				<Button text="Add new" @click="addSimulation()" class="w-full" />
			</div>
		</div>
		<form>
			<div class="mt-3">
				<InputText title="Simulation title" v-model:value="simulation.title" placeholder="Simulation name" />
			</div>
			<ModeDataAccordian title="Transmitter options" :markerColor="simulation.id"
				v-model:showSection="showSections.transmitter">
				<div class="flex flex-row gap-2">
					<InputNumber title="Latitude" v-model:value="simulation.lat" />
					<InputNumber title="Longtitude" v-model:value="simulation.lon" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<Button :text="pickingLocation ? 'Cancel picking' : 'Pick location on map'" @click="addLocationListener"
						:class="pickingLocation ? 'bg-red-600' : ''" />
					<Button text="Fly to coordinates" @click="flyToCurrentMarker" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Power (W)" v-model:value="simulation.tx_power" />
					<InputNumber title="Frequency (mHz)" v-model:value="simulation.frequency_mhz" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" v-model:value="simulation.tx_height" />
					<InputNumber title="Gain (dB)" v-model:value="simulation.tx_gain" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Receiver options" v-model:showSection="showSections.receiver">
				<div class="flex flex-row gap-2">
					<InputNumber title="Sensitivity (dBm)" v-model:value="simulation.signal_threshold" />
					<InputNumber title="Gain (dB)" v-model:value="simulation.rx_gain" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" v-model:value="simulation.rx_height" />
					<InputNumber title="Cable loss (dB)" v-model:value="simulation.system_loss" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Enviroment" v-model:showSection="showSections.enviroment">
				<div class="flex flex-row gap-2">
					<DropDown title="Radio climate" :options="climateOptions" v-model:value="simulation.radio_climate" />
					<DropDown title="Polarization" :options="polarizationOptions" v-model:value="simulation.polarization" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Clutter height (m)" v-model:value="simulation.clutter_height" />
					<InputNumber title="Ground dielectric (V/m)" v-model:value="simulation.ground_dielectric" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Ground conductivity (S/m)" v-model:value="simulation.ground_conductivity" />
					<InputNumber title="Atmospheric bending (N)" v-model:value="simulation.atmosphere_bending" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Simulation options" v-model:showSection="showSections.simulationsOptions">
				<div class="flex flex-row gap-2">
					<InputNumber title="Situation fraction (%)" v-model:value="simulation.situation_fraction" />
					<InputNumber title="Time fraction (%)" v-model:value="simulation.time_fraction" />
				</div>
				<div class="mt-3">
					<InputNumber title="Max range (km)" v-model:value="simulation.radius" />
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
import { randomHexColor } from "../../utils";

const map = useMap();
const store = useStore();
const notificationStore = useNotificationStore();

const currentMarker = ref<Marker | null>(null);
const pickingLocation = ref(false);
const isSimulationRunning = ref(false);
const locationPickerSubscription = ref<Subscription | null>(null);

const showSections = ref({
	transmitter: true,
	receiver: false,
	enviroment: false,
	simulationsOptions: false,
});

const simulations: Ref<CoverageSimulatorSite[]> = ref([]);

const defautltSimulationValues: ComputedRef<CoverageSimulatorSite> = computed(
	() => {
		return {
			id: randomHexColor(),
			title: `Simulation ${simulations.value.length}`,
			lat: 45.85473269336,
			lon: 13.72616645611,
			tx_power: 0.1,
			frequency_mhz: 868.5,
			tx_height: 2,
			tx_gain: 5,
			rx_gain: 5,
			rx_height: 2,
			system_loss: 1,
			signal_threshold: -153,
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
		};
	},
);

if (simulations.value.length === 0) {
	simulations.value.push(defautltSimulationValues.value);
}

const simulationsOptions = computed(() => {
	return simulations.value.map((simulation) => ({
		id: simulation.id,
		title: simulation.title,
	}));
});

const simulation: Ref<CoverageSimulatorSite> = ref(simulations.value[0]);

// watch for current simulation changes
watch(
	simulation,
	(sim) => {
		if (!map.isLoaded || !map.map) return;

		if (!currentMarker.value) {
			currentMarker.value = new Marker({
				color: simulation.value.id,
			})
				.setLngLat([sim.lon, sim.lat])
				.setPopup(
					new Popup({ offset: 25 }).setHTML(
						`<h3>${sim.title}</h3><p>Power: ${sim.tx_power} W</p><p>Frequency: ${sim.frequency_mhz} MHz</p>`,
					),
				)
				.addTo(map.map);
		}

		// @ts-ignore
		currentMarker.value.setLngLat([sim.lon, sim.lat]);
	},
	{ immediate: true, deep: true },
);

async function runSimulation() {
	if (!map.isLoaded || !map.map) return;

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
			tx_power: 10 * Math.log10(simulation.value.tx_power) + 30,
			radius: simulation.value.radius * 1000,
			colormap: "plasma",
			min_dbm: simulation.value.signal_threshold,
			max_dbm: -80,
		});

		if (!predictRes.ok)
			throw new Error(`Failed to start prediction: ${await predictRes.text()}`);

		const predictData = await predictRes.json();
		const taskId = predictData.task_id;

		await store.fetchSimulationStatus(taskId, 1000);

		notificationStore.addNotification({
			type: "success",
			message: "Simulation completed successfully.",
			title: "Coverage Simulation",
			hideAfter: 5000,
		});

		if (map.isLoaded && map.map) {

			if (map.map.getSource(`coverage-${simulation.value.id}`)) {
				map.map.removeLayer(`coverage-${simulation.value.id}`);
				map.map.removeSource(`coverage-${simulation.value.id}`);
			}

			map.map.addSource(`coverage-${simulation.value.id}`, {
				type: "raster",
				tiles: [store.getMapWmsUrl(taskId)],
				tileSize: 256,
			});
			map.map.addLayer({
				id: `coverage-${simulation.value.id}`,
				type: "raster",
				source: `coverage-${simulation.value.id}`,
				paint: {},
			});
		}
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

		if (currentMarker.value) {
			currentMarker.value.setLngLat([
				Number(lng.toFixed(10)),
				Number(lat.toFixed(10)),
			]);
		}

		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
	});
}

function flyToCurrentMarker() {
	if (!map.isLoaded || !map.map) return;

	map.map.flyTo({
		center: [simulation.value.lon, simulation.value.lat],
		zoom: 15,
	});
}

function addSimulation() {
	simulations.value.push(defautltSimulationValues.value);
	simulation.value = simulations.value[simulations.value.length - 1];
}

function changeCurrentSimulation(sim: { id: string; title: string }) {
	const index = simulations.value.findIndex(
		(simulation) => simulation.id === sim.id,
	);
	if (index !== -1) {
		simulation.value = simulations.value[index];
	}

	currentMarker.value?.setLngLat([simulation.value.lon, simulation.value.lat]);
}

function removeSimulation(id: string) {
	if (!map.isLoaded || !map.map) return;

	if (simulations.value.length === 1) {
		notificationStore.addNotification({
			type: "error",
			message: "You need at least one simulation.",
			title: "Coverage Simulation",
			hideAfter: 5000,
		});
		return;
	}

	const index = simulations.value.findIndex((sim) => sim.id === id);
	if (index !== -1) {
		simulations.value.splice(index, 1);
	}

	try {
		map.map?.removeLayer(`coverage-${id}`);
		map.map?.removeSource(`coverage-${id}`);
	} catch (e) {
		console.error(`Error removing layer: ${id}`);
	}
}

// remove all uneded stuff before umount
onBeforeUnmount(() => {
	currentMarker.value?.remove();

	locationPickerSubscription.value?.unsubscribe();
	locationPickerSubscription.value = null;

	try {
		map.map?.removeLayer(`coverage-${simulation.value.id}`);
		map.map?.removeSource(`coverage-${simulation.value.id}`);
	} catch (e) {
		console.error(`Error removing layer: ${simulation.value.id}`);
	}

	for (const simulation of simulations.value) {
		try {
			map.map?.removeLayer(`coverage-${simulation.id}`);
			map.map?.removeSource(`coverage-${simulation.id}`);
		} catch (e) {
			console.error(`Error removing layer: ${simulation.id}`);
		}
	}
});
</script>