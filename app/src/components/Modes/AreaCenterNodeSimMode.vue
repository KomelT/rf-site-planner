<template>
	<div>
		<form>
			<ModeDataAccordian title="Polygon area" v-model:showSection="showSections.polygonArea">
				<div class="flex flex-row gap-2 mt-3">
					<Button :text="pickingPolygonArea ? 'Cancel picking' : 'Pick polygon on map'" @click="drawPolygonArea()"
						:class="pickingPolygonArea ? 'bg-red-600' : ''" />
					<Button v-if="pickingPolygonArea" :text="pickingPolygonArea ? 'Finish polygon' : ''"
						@click="finishPolygonArea()"
						:class="areaPolygon.length > 2 ? '!bg-green-600' : '!bg-green-800 cursor-not-allowed'" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Transmitter options" v-model:showSection="showSections.transmitter">
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Power (dBm)" v-model:value="currentTransmitter.power" />
					<InputNumber title="Frequency (MHz)" v-model:value="simulation.frequency_mhz" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" v-model:value="currentTransmitter.height" />
					<InputNumber title="Gain (dBi)" v-model:value="currentTransmitter.gain" />
				</div>
			</ModeDataAccordian>
			<ModeDataAccordian title="Recivers options" :markerColor="currentReceiver.id"
				v-model:showSection="showSections.receivers">
				<div class="grid grid-cols-7 gap-2 items-end">
					<div class="col-span-5">
						<DropDown title="Simulations" :options="simulationReceivers" @update:selected="changeCurrentReceiver"
							:deleteBtn="true" @delete:option="removeReceiver" />
					</div>
					<div class="col-span-2">
						<Button text="Add new" @click="addReceiver()" class="w-full" />
					</div>
				</div>
				<div class="flex flex-row gap-2">
					<InputNumber title="Latitude" v-model:value="currentReceiver.lat" :disabled="true" />
					<InputNumber title="Longtitude" v-model:value="currentReceiver.lon" :disabled="true" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<Button :text="pickingReceiverLocation ? 'Cancel picking' : 'Pick location on map'"
						@click="addReceiverLocationListener()" :class="pickingReceiverLocation ? 'bg-red-600' : ''" />
					<Button text="Fly to coordinates" @click="flyToNode(currentReceiver.lat, currentReceiver.lon)" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Height (m)" v-model:value="currentReceiver.height" />
					<InputNumber title="Gain (dBi)" v-model:value="currentReceiver.gain" />
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
	type AreaCenterNodeSimulatorSite,
	type LosSimulatorResponse,
	OverpassResponse,
	climateOptions,
	polarizationOptions,
} from "../../stores/types";
import { isMobileDevice, randomHexColor } from "../../utils";
import Button from "../Inputs/Button.vue";
import DropDown from "../Inputs/DropDown.vue";
import InputNumber from "../Inputs/InputNumber.vue";
import ModeDataAccordian from "./ModeDataAccordian.vue";

const map = useMap();
const store = useStore();
const notificationStore = useNotificationStore();

const pickingPolygonArea = ref(false);
const pickingReceiverLocation = ref(false);
const isSimulationRunning = ref(false);
const locationPickerSubscription = ref<Subscription | null>(null);
const areaPolygonSubscription = ref<Subscription | null>(null);

const showSections = ref({
	polygonArea: true,
	transmitter: true,
	receivers: true,
	enviroment: false,
	simulationsOptions: false,
});

const markers: Ref<Marker[]> = ref([]);

const areaPolygon: Ref<[number, number][]> = ref([]);
const polygonMarkers: Ref<Marker[]> = ref([]);

const simulations: Ref<AreaCenterNodeSimulatorSite[]> = ref([]);

const defaultSimulationValues: ComputedRef<AreaCenterNodeSimulatorSite> =
	computed(() => {
		return {
			id: simulations.value.length.toString(),
			title: `Simulation ${simulations.value.length}`,
			frequency_mhz: 868.5,
			transmitter: {
				height: 2,
				gain: 2,
				power: 27,
			},
			recivers: [
				{
					id: randomHexColor(),
					name: "Receiver 1",
					lat: 45.8481696198,
					lon: 13.7311562054,
					height: 2,
					gain: 2,
				},
				{
					id: randomHexColor(),
					name: "Receiver 2",
					lat: 45.8467440547,
					lon: 13.72315913,
					height: 2,
					gain: 2,
				},
			],
			tx_loss: 2,
			radio_climate: "continental_temperate",
			polarization: "vertical",
			clutter_height: 0.9,
			ground_dielectric: 15,
			ground_conductivity: 0.005,
			atmosphere_bending: 301,
			situation_fraction: 95,
			time_fraction: 95,
			high_resolution: false,
		};
	});

if (simulations.value.length === 0) {
	simulations.value.push(defaultSimulationValues.value);
}

const currentTransmitter = ref(simulations.value[0].transmitter);

const currentReceiver = ref(simulations.value[0].recivers[0]);

const simulationReceivers = computed(() => {
	return simulations.value[0].recivers.map((reciver) => ({
		id: reciver.id,
		title: reciver.name,
	}));
});

const simulation: Ref<AreaCenterNodeSimulatorSite> = ref(simulations.value[0]);

// watch for current simulation changes
watch(
	simulation,
	() => {
		if (!map.isLoaded || !map.map) return;

		// remove all markers
		for (const marker of markers.value) {
			marker.remove();
		}

		markers.value = [];

		// add receivers markers
		for (const reciver of simulation.value.recivers) {
			if (!map.map) continue;

			const marker = new Marker({
				color: reciver.id,
			})
				.setLngLat([reciver.lon, reciver.lat])
				.addTo(map.map);

			markers.value.push(marker);

			const popup = new Popup({ offset: 25 }).setHTML(
				`<div class="text-sm text-center">
            <p>Receiver</p>
            <p>Gain: ${reciver.gain} dB</p>
            <p>Height: ${reciver.height} m</p>
          </div>`,
			);
			marker.setPopup(popup);
			popup.addTo(map.map);
		}
	},
	{ immediate: true, deep: true },
);

watch(
	() => areaPolygon.value,
	(newPolygon) => {
		if (!map.isLoaded || !map.map) return;

		// remove all markers
		for (const marker of polygonMarkers.value) {
			marker.remove();
		}

		store.geoJsonLine.type = "LineString";
		store.geoJsonLine.coordinates.splice(0, store.geoJsonLine.coordinates.length);
		for (const point of newPolygon) {
			store.geoJsonLine.coordinates.push([point[0], point[1]]);

			const marker = new Marker({
				color: "#FF0000",
			})
				.setLngLat(point)
				.addTo(map.map);

			polygonMarkers.value.push(marker);

			const popup = new Popup({ offset: 25 }).setHTML(
				`<div class="text-sm text-center">
						<p>Polygon point</p>
					</div>`,
			);
			marker.setPopup(popup);
			popup.addTo(map.map);
		}
	},
	{
		deep: true,
		immediate: true,
	},
);

function drawPolygonArea() {
	if (!map.isLoaded || !map.map) return;

	if (isMobileDevice()) store.toggleMobileMenu();

	if (pickingPolygonArea.value) {
		pickingPolygonArea.value = false;
		if (areaPolygonSubscription.value) {
			areaPolygonSubscription.value.unsubscribe();
			areaPolygonSubscription.value = null;
		}
		areaPolygon.value = [];
		return;
	}

	pickingPolygonArea.value = true;
	areaPolygon.value = [];
	areaPolygonSubscription.value = map.map.on("click", (e) => {
		const { lng, lat } = e.lngLat;

		// add point to polygon
		areaPolygon.value.push([lng, lat]);
	});
}

function finishPolygonArea() {
	if (!map.isLoaded || !map.map) return;

	if (areaPolygon.value.length < 3) {
		notificationStore.addNotification({
			type: "error",
			message: "Polygon must have at least 3 points.",
			title: "Center Node Simulation",
			hideAfter: 3000,
		});
		return;
	}

	pickingPolygonArea.value = false;

	if (areaPolygonSubscription.value) {
		areaPolygonSubscription.value.unsubscribe();
		areaPolygonSubscription.value = null;
	}

	areaPolygon.value.push(areaPolygon.value[0]);
}

function addReceiverLocationListener() {
	if (!map.isLoaded || !map.map) return;

	if (isMobileDevice()) store.toggleMobileMenu();

	if (pickingReceiverLocation.value) {
		pickingReceiverLocation.value = false;
		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
		return;
	}

	pickingReceiverLocation.value = true;

	locationPickerSubscription.value = map.map.on("click", (e) => {
		const { lng, lat } = e.lngLat;
		pickingReceiverLocation.value = false;

		if (currentReceiver.value) {
			currentReceiver.value.lat = Number(lat.toFixed(10));
			currentReceiver.value.lon = Number(lng.toFixed(10));
		}

		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
	});
}

function flyToNode(lat: number, lon: number) {
	if (lat === 0 || lon === 0) return;

	if (isMobileDevice()) store.toggleMobileMenu();

	map.map?.flyTo({
		center: [lon, lat],
		zoom: 18,
	});
}

function changeCurrentReceiver(receiver: { id: string; title: string }) {
	const receiverIndex = simulation.value.recivers.findIndex(
		(sim) => sim.id === receiver.id,
	);

	if (receiverIndex === -1) return;
	currentReceiver.value = simulation.value.recivers[receiverIndex];
}

function removeReceiver(id: string) {
	const receiverIndex = simulation.value.recivers.findIndex(
		(sim) => sim.id === id,
	);
	if (receiverIndex === -1) return;
	simulation.value.recivers.splice(receiverIndex, 1);
}

function addReceiver() {
	simulation.value.recivers.push({
		id: randomHexColor(),
		name: `Receiver ${simulation.value.recivers.length + 1}`,
		lat: 45.8467440547,
		lon: 13.72315913,
		gain: 2,
		height: 2,
	});

	currentReceiver.value =
		simulation.value.recivers[simulation.value.recivers.length - 1];
}

async function runSimulation() {
	if (isMobileDevice()) store.toggleMobileMenu();

	notificationStore.addNotification({
		type: "info",
		message: "Starting simulation...",
		title: "Center Node Simulation",
		hideAfter: 2000,
	});

	isSimulationRunning.value = true;
	const res = await store.fetchOverpassArea(areaPolygon.value);

	if (!res || res.length === 0) {
		notificationStore.addNotification({
			type: "error",
			message: "Failed to fetch area data.",
			title: "Center Node Simulation",
			hideAfter: 3000,
		});
		return;
	}

	const trans: OverpassResponse[] = res?.map((el) => {
		if (!(!el.tags.name || el.tags.name.trim() === ""))
			return el;
		return undefined;
	}).filter((el): el is OverpassResponse => el !== undefined)

	const tasks = ref<{ id: string; tx: string; rx: string }[]>([]);
	store.centerNodeSimModeData.table.data = [];

	for (const transmitter of trans) {
		for (const receiver of simulation.value.recivers) {
			try {
				const predictRes = await store.fetchLosSimulation({
					tx_lat: transmitter.lat,
					tx_lon: transmitter.lon,
					tx_height: currentTransmitter.value.height,
					tx_gain: currentTransmitter.value.gain,
					tx_power: currentTransmitter.value.power,
					rx_lat: receiver.lat,
					rx_lon: receiver.lon,
					rx_height: receiver.height,
					rx_gain: receiver.gain,
					rx_loss: 0,
					frequency_mhz: simulation.value.frequency_mhz,
					atmosphere_bending: simulation.value.atmosphere_bending,
					ground_conductivity: simulation.value.ground_conductivity,
					ground_dielectric: simulation.value.ground_dielectric,
					clutter_height: simulation.value.clutter_height,
					radio_climate: simulation.value.radio_climate,
					polarization: simulation.value.polarization,
					situation_fraction: simulation.value.situation_fraction,
					time_fraction: simulation.value.time_fraction,
					tx_loss: simulation.value.tx_loss,
					high_resolution: simulation.value.high_resolution,
				});

				if (!predictRes.ok)
					throw new Error(
						`Failed to start prediction: ${await predictRes.text()}`,
					);

				const predictData = await predictRes.json();
				tasks.value.push({
					id: predictData.task_id,
					tx: transmitter.id.toString(),
					rx: receiver.id,
				});

			} catch (error) {
				console.error("Error starting simulation:", error);
				notificationStore.addNotification({
					type: "error",
					message: `Error starting simulation, between ${transmitter.tags.name} and ${receiver.name}: ${error}`,
					title: "Center Node Simulation",
					hideAfter: 5000,
				});
				isSimulationRunning.value = false;
				return;
			}
		}
	}

	// Move the promises creation and resolution outside the loops
	const taskPromises = tasks.value.map(async (task) => {
		return new Promise((resolve) => {
			store.fetchSimulationStatus(task.id, 100).then((data) => {
				const tx_id = task.tx;
				const rx_id = task.rx;

				resolve({
					...(JSON.parse(data.data) as unknown as LosSimulatorResponse),
					tx_id: tx_id ?? "",
					tx_title:
						res.find((val) => val.id.toString() === tx_id?.toString())?.tags
							.name ?? "",
					rx_id: rx_id ?? "",
					rx_title:
						simulation.value.recivers.find((val) => val.id === rx_id)?.name ??
						"",
				});
			});
		});
	});

	store.centerNodeSimModeData.table.show = true;

	Promise.all(taskPromises).then((results) => {
		isSimulationRunning.value = false;
		store.centerNodeSimModeData.table.data.push(
			...results.filter(
				(
					result,
				): result is LosSimulatorResponse & {
					tx_id: string;
					tx_title: string;
					rx_id: string;
					rx_title: string;
				} =>
					result !== null && result !== undefined && typeof result === "object",
			),
		);
	});
}

onBeforeUnmount(() => {
	for (const marker of markers.value) {
		marker.remove();
	}

	for (const marker of polygonMarkers.value) {
		marker.remove();
	}

	store.geoJsonLine.type = "LineString";
	store.geoJsonLine.coordinates.splice(0, store.geoJsonLine.coordinates.length);

	locationPickerSubscription.value?.unsubscribe();

	store.centerNodeSimModeData.table.data.splice(0, store.centerNodeSimModeData.table.data.length);
	store.centerNodeSimModeData.table.show = false;
});
</script>
