<template>
	<div>
		<DropDown title="Simulations" :options="simulationsOptions" />
		<form>
			<div class="mt-3">
				<InputText title="Simulation title" v-model:value="simulation.title"
					:placeholder="'Simulation ' + (simulations.length + 1)" />
			</div>
			<ModeDataAccordian title="Transmitter options" v-model:showSection="showSections.transmitter">
				<div class="flex flex-row gap-2">
					<InputNumber title="Latitude" v-model:value="simulation.latitude" />
					<InputNumber title="Longtitude" v-model:value="simulation.longitude" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<Button :text="'Add location ' + (pickingLocation ? '(ready)' : '')" @click="addLocationListener" />
					<Button text="Fly to coordinates" @click="flyToCurrentMarker" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Power (W)" v-model:value="simulation.power" />
					<InputNumber title="Frequency (mHz)" v-model:value="simulation.frequency" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" v-model:value="simulation.transmitterHeight" />
					<InputNumber title="Gain (dB)" v-model:value="simulation.transmitterGain" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Receiver options" v-model:showSection="showSections.receiver">
				<div class="flex flex-row gap-2">
					<InputNumber title="Sensitivity (dBm)" v-model:value="simulation.reciverSensitivity" />
					<InputNumber title="Gain (dB)" v-model:value="simulation.reciverGain" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" v-model:value="simulation.reciverHeight" />
					<InputNumber title="Cable loss (dB)" v-model:value="simulation.reciverCableLoss" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Enviroment" v-model:showSection="showSections.enviroment">
				<div class="flex flex-row gap-2">
					<DropDown title="Radio climate" :options="climateOptions" v-model:value="simulation.radioClimate" />
					<DropDown title="Polarization" :options="polarizationOptions" v-model:value="simulation.polarization" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Clutter height (m)" v-model:value="simulation.clutterHeight" />
					<InputNumber title="Ground dielectric (V/m)" v-model:value="simulation.groundDielectric" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Ground conductivity (S/m)" v-model:value="simulation.groundConductivity" />
					<InputNumber title="Atmospheric bending (N)" v-model:value="simulation.athmosphericBending" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Simulation options" v-model:showSection="showSections.simulationsOptions">
				<div class="flex flex-row gap-2">
					<InputNumber title="Situation fraction (%)" v-model:value="simulation.situationFraction" />
					<InputNumber title="Time fraction (%)" v-model:value="simulation.timeFraction" />
				</div>
				<div class="mt-3">
					<InputNumber title="Max range (km)" v-model:value="simulation.maxRange" />
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
import { Marker, Popup } from "maplibre-gl";
import { type Ref, computed, onBeforeUnmount, ref, watch } from "vue";
import redPinMarker from "../../assets/redPinMarker";
import { climateOptions, polarizationOptions } from "../../stores/types";
import Button from "../Inputs/Button.vue";
import DropDown from "../Inputs/DropDown.vue";
import InputNumber from "../Inputs/InputNumber.vue";
import InputText from "../Inputs/InputText.vue";
import ModeDataAccordian from "./ModeDataAccordian.vue";

const map = useMap();

const currentMarker = ref<Marker | null>(null);
const pickingLocation = ref(false);
const isSimulationRunning = ref(false);

type simulationType = {
	id: number | undefined;
	title: string;
	latitude: number;
	longitude: number;
	power: number;
	frequency: number;
	transmitterHeight: number;
	transmitterGain: number;
	reciverSensitivity: number;
	reciverGain: number;
	reciverHeight: number;
	reciverCableLoss: number;
	radioClimate:
	| "equatorial"
	| "continental_subtropical"
	| "maritime_subtropical"
	| "desert"
	| "continental_temperate"
	| "maritime_temperature_land"
	| "maritime_temperature_sea";
	polarization: "vertical" | "horizontal";
	clutterHeight: number;
	groundDielectric: number;
	groundConductivity: number;
	athmosphericBending: number;
	situationFraction: number;
	timeFraction: number;
	maxRange: number;
};

const simulations: Ref<simulationType[]> = ref([
	{
		id: undefined,
		title: "New simulation",
		latitude: 0,
		longitude: 0,
		power: 0,
		frequency: 0,
		transmitterHeight: 0,
		transmitterGain: 0,
		reciverSensitivity: 0,
		reciverGain: 0,
		reciverHeight: 0,
		reciverCableLoss: 0,
		radioClimate: "continental_temperate",
		polarization: "vertical",
		clutterHeight: 0,
		groundDielectric: 0,
		groundConductivity: 0,
		athmosphericBending: 0,
		situationFraction: 0,
		timeFraction: 0,
		maxRange: 0,
	},
]);

const defautltSimulation: simulationType = {
	id: undefined,
	title: `Simulation ${simulations.value.length}`,
	latitude: 45.85473269336,
	longitude: 13.72616645611,
	power: 0.1,
	frequency: 868.5,
	transmitterHeight: 2,
	transmitterGain: 2,
	reciverSensitivity: -130,
	reciverGain: 2,
	reciverHeight: 1,
	reciverCableLoss: 2,
	radioClimate: "continental_temperate",
	polarization: "vertical",
	clutterHeight: 0.9,
	groundDielectric: 15,
	groundConductivity: 0.005,
	athmosphericBending: 301,
	situationFraction: 95,
	timeFraction: 95,
	maxRange: 30,
};

const showSections = ref({
	transmitter: true,
	receiver: false,
	enviroment: false,
	simulationsOptions: false,
});

const simulationsOptions = computed(() => {
	return simulations.value.map((simulation) => ({
		id: simulation.id,
		title: simulation.title,
	}));
});

const simulation: Ref<simulationType> = ref(defautltSimulation);

// watch for current simulation changes
watch(
	simulation,
	(sim) => {
		if (!map.isLoaded || !map.map) return;

		if (!currentMarker.value) {
			currentMarker.value = new Marker({
				element: redPinMarker,
			})
				.setLngLat([sim.longitude, sim.latitude])
				.setPopup(
					new Popup({ offset: 25 }).setHTML(
						`<h3>${sim.title}</h3><p>Power: ${sim.power} W</p><p>Frequency: ${sim.frequency} MHz</p>`,
					),
				)
				.addTo(map.map);
		}

		// @ts-ignore
		currentMarker.value.setLngLat([sim.longitude, sim.latitude]);
	},
	{ immediate: true, deep: true },
);

// watch for simulations changes
watch(
	simulations,
	(simulation) => {
		if (!map.isLoaded || !map.map) return;

		for (const sim of simulation) {
			if (sim.id === undefined) continue;

			new Marker()
				.setLngLat([sim.longitude, sim.latitude])
				.setPopup(
					new Popup({ offset: 25 }).setHTML(
						`<h3>${sim.title}</h3><p>Power: ${sim.power} W</p><p>Frequency: ${sim.frequency} MHz</p>`,
					),
				)
				.addTo(map.map);
		}
	},
	{ deep: true, immediate: true },
);

async function runSimulation() {
	if (!map.isLoaded || !map.map) return;

	isSimulationRunning.value = true;
	const payload = {
		// Transmitter parameters
		lat: simulation.value.latitude,
		lon: simulation.value.longitude,
		tx_height: simulation.value.transmitterHeight,
		tx_power: 10 * Math.log10(simulation.value.power) + 30,
		tx_gain: simulation.value.transmitterGain,
		frequency_mhz: simulation.value.frequency,

		// Receiver parameters
		rx_height: simulation.value.reciverHeight,
		rx_gain: simulation.value.reciverGain,
		signal_threshold: simulation.value.reciverSensitivity,
		system_loss: simulation.value.reciverCableLoss,

		// Environment parameters
		clutter_height: simulation.value.clutterHeight,
		ground_dielectric: simulation.value.groundDielectric,
		ground_conductivity: simulation.value.groundConductivity,
		atmosphere_bending: simulation.value.athmosphericBending,
		radio_climate: simulation.value.radioClimate,
		polarization: simulation.value.polarization,

		// Simulation parameters
		radius: simulation.value.maxRange * 1000,
		situation_fraction: simulation.value.situationFraction,
		time_fraction: simulation.value.timeFraction,
		high_resolution: false,

		// Display parameters
		colormap: "plasma",
		min_dbm: -130,
		max_dbm: -80,
	};

	const predictResponse = await fetch(
		`${import.meta.env.VITE_API_URL}/predict`,
		{
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(payload),
		},
	);

	if (!predictResponse.ok) {
		isSimulationRunning.value = false;
		const errorDetails = await predictResponse.text();
		throw new Error(`Failed to start prediction: ${errorDetails}`);
	}

	const predictData = await predictResponse.json();
	const taskId = predictData.task_id;

	console.log(`Prediction started with task ID: ${taskId}`);

	// Poll for task status and result
	const pollInterval = 1000; // 1 seconds
	const pollStatus = async () => {
		const statusResponse = await fetch(
			`${import.meta.env.VITE_API_URL}/status/${taskId}`,
		);

		if (!statusResponse.ok) {
			isSimulationRunning.value = false;
			throw new Error("Failed to fetch task status.");
		}

		const statusData = await statusResponse.json();
		console.log("Task status:", statusData);

		if (statusData.status === "completed") {
			if (map.isLoaded && map.map) {
				map.map.addSource(taskId, {
					type: "raster",
					tiles: [
						`${import.meta.env.VITE_GEOSERVER_URL}/RF-SITE-PLANNER/wms?service=WMS&version=1.1.0&transparent=true&request=GetMap&layers=RF-SITE-PLANNER:${taskId}&bbox={bbox-epsg-3857}&width=256&height=256&srs=EPSG:3857&format=image/png`,
					],
					tileSize: 256,
				});
				map.map.addLayer({
					id: taskId,
					type: "raster",
					source: taskId,
					paint: {},
				});
			}
		} else if (statusData.status === "failed") {
			console.error("Simulation failed.");
		} else {
			setTimeout(pollStatus, pollInterval); // Poll again after the interval
		}
	};

	pollStatus(); // Start polling
}

// add location listener for selecting location on map
function addLocationListener() {
	if (!map.isLoaded || !map.map) return;
	pickingLocation.value = true;

	const neki = map.map.on("click", (e) => {
		const { lng, lat } = e.lngLat;
		pickingLocation.value = false;
		simulation.value.latitude = Number(lat.toFixed(10));
		simulation.value.longitude = Number(lng.toFixed(10));

		if (currentMarker.value) {
			currentMarker.value.setLngLat([
				Number(lng.toFixed(10)),
				Number(lat.toFixed(10)),
			]);
		}

		neki.unsubscribe();
	});
}

// fly to current marker
function flyToCurrentMarker() {
	if (!map.isLoaded || !map.map) return;

	map.map.flyTo({
		center: [simulation.value.longitude, simulation.value.latitude],
		zoom: 15,
	});
}

// remove all markers on umount
onBeforeUnmount(() => {
	if (currentMarker.value) {
		currentMarker.value.remove();
	}
});
</script>