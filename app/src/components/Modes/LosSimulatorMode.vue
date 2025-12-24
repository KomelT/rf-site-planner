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
			<ModeDataAccordian title="Transmitter options" markerColor="red" v-model:showSection="showSections.transmitter">
				<div class="flex flex-row gap-2">
					<InputNumber title="Latitude" v-model:value="simulation.tx_lat" />
					<InputNumber title="Longtitude" v-model:value="simulation.tx_lon" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<Button :text="txPickingLocation ? 'Cancel picking' : 'Pick location on map'"
						@click="addLocationListener('tx')" :class="txPickingLocation ? 'bg-red-600' : ''" />
					<Button text="Fly to coordinates" @click="flyToMarker(simulation.tx_lon, simulation.tx_lat)" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Power (dBm)" v-model:value="simulation.tx_power" />
					<InputNumber title="Frequency (MHz)" v-model:value="simulation.frequency_mhz" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" v-model:value="simulation.tx_height" />
					<InputNumber title="Gain (dBi)" v-model:value="simulation.tx_gain" />
					<InputNumber title="Loss (dB)" v-model:value="simulation.tx_loss" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Reciver options" markerColor="#3FB1CE" v-model:showSection="showSections.receiver">
				<div class="flex flex-row gap-2">
					<InputNumber title="Latitude" v-model:value="simulation.rx_lat" />
					<InputNumber title="Longtitude" v-model:value="simulation.rx_lon" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<Button :text="rxPickingLocation ? 'Cancel picking' : 'Pick location on map'"
						@click="addLocationListener('rx')" :class="rxPickingLocation ? 'bg-red-600' : ''" />
					<Button text="Fly to coordinates" @click="flyToMarker(simulation.rx_lon, simulation.rx_lat)" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" v-model:value="simulation.rx_height" />
					<InputNumber title="Gain (dBi)" v-model:value="simulation.rx_gain" />
					<InputNumber title="Loss (dB)" v-model:value="simulation.rx_loss" />
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
				<div class="flex flex-row gap-2 mt-2">
					<Toggle title="High resolution" v-model:value="simulation.high_resolution" />
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
	type LosSimulatorResponse,
	type LosSimulatorSite,
	climateOptions,
	polarizationOptions,
} from "../../stores/types";
import { isMobileDevice, processLosData } from "../../utils";
import Button from "../Inputs/Button.vue";
import DropDown from "../Inputs/DropDown.vue";
import InputNumber from "../Inputs/InputNumber.vue";
import InputText from "../Inputs/InputText.vue";
import Toggle from "../Inputs/Toggle.vue";
import ModeDataAccordian from "./ModeDataAccordian.vue";

const map = useMap();
const store = useStore();
const notificationStore = useNotificationStore();

const txMarker = ref<Marker | null>(null);
const rxMarker = ref<Marker | null>(null);
const betwMarker = ref<Marker | null>(null);
const txPickingLocation = ref(false);
const rxPickingLocation = ref(false);
const isSimulationRunning = ref(false);
const locationPickerSubscription = ref<Subscription | null>(null);

const showSections = ref({
	transmitter: true,
	receiver: true,
	enviroment: false,
	simulationsOptions: false,
});

const defaultSimulationValues: ComputedRef<LosSimulatorSite> = computed(() => {
	return {
		id: store.losSimModeData.simulations.length.toString(),
		title: `Simulation ${store.losSimModeData.simulations.length}`,
		tx_lat: 45.85473269336,
		tx_lon: 13.72616645611,
		tx_height: 4,
		tx_power: 27,
		tx_gain: 5,
		tx_loss: 2,
		frequency_mhz: 868.5,
		rx_lat: 45.843544567,
		rx_lon: 13.7343341751,
		rx_height: 15,
		rx_gain: 6.5,
		rx_loss: 2,
		radio_climate: "continental_temperate",
		polarization: "vertical",
		clutter_height: 0.9,
		ground_dielectric: 15,
		ground_conductivity: 0.005,
		atmosphere_bending: 301,
		situation_fraction: 90,
		time_fraction: 95,
		high_resolution: false,
	};
});

if (store.losSimModeData.simulations.length === 0) {
	store.losSimModeData.simulations.push(defaultSimulationValues.value);
}

const simulationsOptions = computed(() => {
	return store.losSimModeData.simulations.map((simulation) => ({
		id: simulation.id,
		title: simulation.title,
	}));
});

const simulation: Ref<LosSimulatorSite> = ref(store.losSimModeData.simulations[0]);

// watch for current simulation changes
watch(
	simulation,
	(sim) => {
		if (!map.isLoaded || !map.map) return;

		if (!txMarker.value) {
			txMarker.value = new Marker({ color: "red" })
				.setLngLat([sim.tx_lon, sim.tx_lat])
				.setPopup(
					new Popup({ offset: 25 }).setHTML(
						`<h3>Tx site for ${sim.title}</h3>`,
					),
				)
				.addTo(map.map);
		}

		if (!rxMarker.value) {
			rxMarker.value = new Marker()
				.setLngLat([sim.rx_lon, sim.rx_lat])
				.setPopup(
					new Popup({ offset: 25 }).setHTML(
						`<h3>Rx site for ${sim.title}</h3>`,
					),
				)
				.addTo(map.map);
		}

		// @ts-ignore
		txMarker.value.setLngLat([sim.tx_lon, sim.tx_lat]);
		// @ts-ignore
		rxMarker.value.setLngLat([sim.rx_lon, sim.rx_lat]);

		store.geoJsonLine.type = "LineString";
		store.geoJsonLine.coordinates.splice(0, store.geoJsonLine.coordinates.length);
		store.geoJsonLine.coordinates.push([sim.tx_lon, sim.tx_lat]);
		store.geoJsonLine.coordinates.push([sim.rx_lon, sim.rx_lat]);
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
		title: "LOS Simulation",
		hideAfter: 2000,
	});

	try {
		const predictRes = await store.fetchLosSimulation({
			...simulation.value,
			tx_power: simulation.value.tx_power,
		});

		if (!predictRes.ok)
			throw new Error(`Failed to start prediction: ${await predictRes.text()}`);

		const predictData = await predictRes.json();
		const taskId = predictData.task_id;

		const data = await store.fetchSimulationStatus(taskId, 500);
		const lossData = JSON.parse(data.data) as unknown as LosSimulatorResponse;

		store.losSimModeData.chart.rx_signal_power = lossData.rx_signal_power;
		store.losSimModeData.chart.path_loss = lossData.path_loss;
		store.losSimModeData.chart.longley_rice_loss = lossData.longley_rice_loss;
		store.losSimModeData.chart.path.obstructed = lossData.path.obstructed;
		store.losSimModeData.chart.path.message = lossData.path.message;
		store.losSimModeData.chart.path.obstructions = lossData.path.obstructions;

		const lossProcessedData = processLosData(lossData);

		store.losSimModeData.chart.data = [
			{
				name: "Elevation (m)",
				data: lossProcessedData.profile,
			},
			{
				name: "Earth curvature (m)",
				data: lossProcessedData.curvature,
			},
			{
				name: "Fresnel zone (m)",
				data: lossProcessedData.fresnel,
			},
			{
				name: "Fresnel zone 60% (m)",
				data: lossProcessedData.fresnel_pt_6,
			},
			{
				name: "Point to point (m)",
				data: lossProcessedData.reference,
			},
		];

		store.losSimModeData.chart.options = {
			chart: {
				type: "line",
			},
			stroke: {
				curve: "smooth",
				width: 1.2,
			},
			yaxis: {
				decimalsInFloat: 0,
			},
			xaxis: {
				type: "numeric",
				categories: lossProcessedData.distance,
				tickAmount: 10,
				labels: {
					formatter: (value: string): string | string[] => {
						if (!value) return "";

						if (
							lossProcessedData.distance[
							lossProcessedData.distance.length - 1
							] > 10
						)
							return parseFloat(value).toFixed(0);

						return parseFloat(value).toFixed(1);
					},
				},
			},
			tooltip: {
				x: {
					formatter: (val: number): string => {
						const lenBetw = val
						const pathLen = lossProcessedData.distance[lossProcessedData.distance.length - 1];

						const coordBetw = [
							simulation.value.rx_lon + (simulation.value.tx_lon - simulation.value.rx_lon) * (lenBetw / pathLen),
							simulation.value.rx_lat + (simulation.value.tx_lat - simulation.value.rx_lat) * (lenBetw / pathLen)
						] as [number, number];

						if (!betwMarker.value && map.map) {
							betwMarker.value = new Marker({ color: "blue" })
								.setLngLat(coordBetw)
								.addTo(map.map);
						} else if (betwMarker.value) {
							betwMarker.value.setLngLat(coordBetw);
						}

						return val.toFixed(2) + " km";
					},
				}
			}
		};

		store.losSimModeData.chart.show = true;

		notificationStore.addNotification({
			type: "success",
			message: "Simulation finished",
			title: "LOS Simulation",
			hideAfter: 2000,
		});
	} catch (e) {
		console.error(e);
		notificationStore.addNotification({
			type: "error",
			message: "Simulation failed",
			title: "LOS Simulation",
			hideAfter: 2000,
		});
	} finally {
		isSimulationRunning.value = false;
	}
}

// add location listener for selecting location on map
function addLocationListener(type: "tx" | "rx") {
	if (!map.isLoaded || !map.map) return;

	if (isMobileDevice()) store.toggleMobileMenu();

	if (type === "tx" && txPickingLocation.value) {
		txPickingLocation.value = false;
		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
		return;
	}

	if (type === "rx" && rxPickingLocation.value) {
		rxPickingLocation.value = false;
		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
		return;
	}

	if (type === "tx") {
		txPickingLocation.value = true;
		rxPickingLocation.value = false;
	} else if (type === "rx") {
		rxPickingLocation.value = true;
		txPickingLocation.value = false;
	}

	locationPickerSubscription.value = map.map.on("click", (e) => {
		const { lng, lat } = e.lngLat;

		betwMarker.value?.remove();

		simulation.value[`${type}_lat`] = Number(lat.toFixed(10));
		simulation.value[`${type}_lon`] = Number(lng.toFixed(10));

		if (txPickingLocation && txMarker.value) {
			txMarker.value.setLngLat([
				Number(lng.toFixed(10)),
				Number(lat.toFixed(10)),
			]);
		} else if (rxPickingLocation && rxMarker.value) {
			rxMarker.value.setLngLat([
				Number(lng.toFixed(10)),
				Number(lat.toFixed(10)),
			]);
		}

		txPickingLocation.value = false;
		rxPickingLocation.value = false;

		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
	});
}

function flyToMarker(lon: number, lat: number) {
	if (!map.isLoaded || !map.map) return;

	if (isMobileDevice()) store.toggleMobileMenu();

	map.map.flyTo({
		center: [lon, lat],
		zoom: 15,
	});
}

function addSimulation() {
	store.losSimModeData.simulations.push(defaultSimulationValues.value);
	simulation.value = store.losSimModeData.simulations[store.losSimModeData.simulations.length - 1];
}

function changeCurrentSimulation(sim: { id: string; title: string }) {
	const index = store.losSimModeData.simulations.findIndex(
		(simulation) => simulation.id === sim.id,
	);
	if (index !== -1) {
		simulation.value = store.losSimModeData.simulations[index];
	}

	txMarker.value?.setLngLat([simulation.value.tx_lon, simulation.value.tx_lat]);
	rxMarker.value?.setLngLat([simulation.value.rx_lon, simulation.value.rx_lat]);
}

function removeSimulation(id: string) {
	if (!map.isLoaded || !map.map) return;

	if (store.losSimModeData.simulations.length === 1) {
		notificationStore.addNotification({
			type: "error",
			message: "You need at least one simulation.",
			title: "Coverage Simulation",
			hideAfter: 2000,
		});
		return;
	}

	const index = store.losSimModeData.simulations.findIndex((sim) => sim.id === id);
	if (index !== -1) {
		store.losSimModeData.simulations.splice(index, 1);
	}

	try {
		map.map?.removeLayer(`coverage-${id}`);
		map.map?.removeSource(`coverage-${id}`);
	} catch (e) {
		console.error(`Error removing layer: ${id}`);
	}
}

// remove all markers on umount
onBeforeUnmount(() => {
	store.losSimModeData.chart.show = false;

	if (txMarker.value) {
		txMarker.value.remove();
	}

	if (rxMarker.value) {
		rxMarker.value.remove();
	}

	if (betwMarker.value) {
		betwMarker.value.remove();
	}

	store.geoJsonLine.type = "LineString";
	store.geoJsonLine.coordinates.splice(0, store.geoJsonLine.coordinates.length);
});
</script>
