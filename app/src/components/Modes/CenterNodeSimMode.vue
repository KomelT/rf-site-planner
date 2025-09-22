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
			<ModeDataAccordian title="Transmitter options" :markerColor="currentTransmitter.id"
				v-model:showSection="showSections.transmitter">
				<div class="grid grid-cols-7 gap-2 items-end">
					<div class="col-span-5">
						<DropDown title="Simulations" :options="simulationTransmitter" @update:selected="changeCurrentTransmitter"
							:deleteBtn="true" @delete:option="removeTransmitter" />
					</div>
					<div class="col-span-2">
						<Button text="Add new" @click="addTransmitter()" class="w-full" />
					</div>
				</div>
				<div class="flex flex-row gap-2">
					<InputNumber title="Latitude" v-model:value="currentTransmitter.lat" :disabled="true" />
					<InputNumber title="Longtitude" v-model:value="currentTransmitter.lon" :disabled="true" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<Button :text="pickingTransmitterLocation ? 'Cancel picking' : 'Pick location on map'"
						@click="addTransmitterLocationListener()" :class="pickingTransmitterLocation ? 'bg-red-600' : ''" />
					<Button text="Fly to coordinates" @click="flyToNode(currentTransmitter.lat, currentTransmitter.lon)" />
				</div>
				<div class="flex flex-row gap-2 mt-3">
					<InputNumber title="Power (dBm)" v-model:value="currentTransmitter.power" />
					<InputNumber title="Frequency (mHz)" v-model:value="simulation.frequency_mhz" />
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
	type CenterNodeSimulatorSite,
	type LosSimulatorResponse,
	climateOptions,
	polarizationOptions,
} from "../../stores/types";
import { isMobileDevice, randomHexColor } from "../../utils";
import Button from "../Inputs/Button.vue";
import DropDown from "../Inputs/DropDown.vue";
import InputNumber from "../Inputs/InputNumber.vue";
import InputText from "../Inputs/InputText.vue";
import ModeDataAccordian from "./ModeDataAccordian.vue";

const map = useMap();
const store = useStore();
const notificationStore = useNotificationStore();

const pickingTransmitterLocation = ref(false);
const pickingReceiverLocation = ref(false);
const isSimulationRunning = ref(false);
const locationPickerSubscription = ref<Subscription | null>(null);

const showSections = ref({
	transmitter: true,
	receivers: true,
	enviroment: false,
	simulationsOptions: false,
});

const markers: Ref<Marker[]> = ref([]);

const simulations: Ref<CenterNodeSimulatorSite[]> = ref([]);

const defautltSimulationValues: ComputedRef<CenterNodeSimulatorSite> = computed(
	() => {
		return {
			id: simulations.value.length.toString(),
			title: `Simulation ${simulations.value.length}`,
			frequency_mhz: 868.5,
			transmitter: [
				{
					id: randomHexColor(),
					name: "Transmitter 1",
					lat: 45.8547367972,
					lon: 13.7261620811,
					height: 2,
					gain: 2,
					power: 27,
				},
			],
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
			system_loss: 2,
			signal_threshold: -130,
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
	},
);

if (simulations.value.length === 0) {
	simulations.value.push(defautltSimulationValues.value);
}

const currentTransmitter = ref(simulations.value[0].transmitter[0]);

const currentReceiver = ref(simulations.value[0].recivers[0]);

const simulationsOptions = computed(() => {
	return simulations.value.map((simulation) => ({
		id: simulation.id,
		title: simulation.title,
	}));
});

const simulationTransmitter = computed(() => {
	return simulations.value[0].transmitter.map((reciver) => ({
		id: reciver.id,
		title: reciver.name,
	}));
});

const simulationReceivers = computed(() => {
	return simulations.value[0].recivers.map((reciver) => ({
		id: reciver.id,
		title: reciver.name,
	}));
});

const simulation: Ref<CenterNodeSimulatorSite> = ref(simulations.value[0]);

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

		// add transmitter marker
		for (const transmitter of simulation.value.transmitter) {
			if (!map.map) continue;

			const marker = new Marker({
				color: transmitter.id,
			})
				.setLngLat([transmitter.lon, transmitter.lat])
				.addTo(map.map);

			markers.value.push(marker);

			const popup = new Popup({ offset: 25 }).setHTML(
				`<div class="text-sm text-center">
						<p>Transmitter</p>
						<p>Gain: ${transmitter.gain} dB</p>
						<p>Height: ${transmitter.height} m</p>
					</div>`,
			);
			marker.setPopup(popup);
			popup.addTo(map.map);
		}

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

function changeCurrentSimulation() { }

function removeSimulation() { }

function addSimulation() { }

function addTransmitterLocationListener() {
	if (!map.isLoaded || !map.map) return;

	if (pickingTransmitterLocation.value) {
		pickingTransmitterLocation.value = false;
		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
		return;
	}

	pickingTransmitterLocation.value = true;

	locationPickerSubscription.value = map.map.on("click", (e) => {
		const { lng, lat } = e.lngLat;
		pickingTransmitterLocation.value = false;

		if (currentTransmitter.value) {
			currentTransmitter.value.lat = Number(lat.toFixed(10));
			currentTransmitter.value.lon = Number(lng.toFixed(10));
		}

		if (locationPickerSubscription.value) {
			locationPickerSubscription.value.unsubscribe();
			locationPickerSubscription.value = null;
		}
	});
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

function changeCurrentTransmitter(transmitter: { id: string; title: string }) {
	const transmitterIndex = simulation.value.transmitter.findIndex(
		(sim) => sim.id === transmitter.id,
	);

	if (transmitterIndex === -1) return;
	currentTransmitter.value = simulation.value.transmitter[transmitterIndex];
}

function changeCurrentReceiver(receiver: { id: string; title: string }) {
	const receiverIndex = simulation.value.recivers.findIndex(
		(sim) => sim.id === receiver.id,
	);

	if (receiverIndex === -1) return;
	currentReceiver.value = simulation.value.recivers[receiverIndex];
}

function removeTransmitter(id: string) {
	const transmitterIndex = simulation.value.transmitter.findIndex(
		(sim) => sim.id === id,
	);

	if (transmitterIndex === -1) return;
	simulation.value.transmitter.splice(transmitterIndex, 1);
}

function addTransmitter() {
	simulation.value.transmitter.push({
		id: randomHexColor(),
		name: `Transmitter ${simulation.value.transmitter.length + 1}`,
		lat: 45.8547367972,
		lon: 13.7261620811,
		gain: 2,
		height: 2,
		power: 27,
	});

	currentTransmitter.value =
		simulation.value.transmitter[simulation.value.transmitter.length - 1];
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
	try {
		if (isMobileDevice()) store.toggleMobileMenu();

		isSimulationRunning.value = true;

		notificationStore.addNotification({
			type: "info",
			message: "Starting simulation...",
			title: "Center Node Simulation",
			hideAfter: 2000,
		});

		const tasks = ref<{ id: string; tx: string; rx: string }[]>([]);

		store.centerNodeSimModeData.table.data = [];

		for (const transmitter of simulation.value.transmitter) {
			for (const receiver of simulation.value.recivers) {
				try {
					const predictRes = await store.fetchLosSimulation({
						tx_lat: transmitter.lat,
						tx_lon: transmitter.lon,
						tx_height: transmitter.height,
						tx_gain: transmitter.gain,
						tx_power: transmitter.power,
						rx_lat: receiver.lat,
						rx_lon: receiver.lon,
						rx_height: receiver.height,
						rx_gain: receiver.gain,
						frequency_mhz: simulation.value.frequency_mhz,
						atmosphere_bending: simulation.value.atmosphere_bending,
						ground_conductivity: simulation.value.ground_conductivity,
						ground_dielectric: simulation.value.ground_dielectric,
						clutter_height: simulation.value.clutter_height,
						radio_climate: simulation.value.radio_climate,
						polarization: simulation.value.polarization,
						situation_fraction: simulation.value.situation_fraction,
						time_fraction: simulation.value.time_fraction,
						signal_threshold: simulation.value.signal_threshold,
						system_loss: simulation.value.system_loss,
						high_resolution: simulation.value.high_resolution,
					});

					if (!predictRes.ok)
						throw new Error(
							`Failed to start prediction: ${await predictRes.text()}`,
						);

					const predictData = await predictRes.json();
					tasks.value.push({
						id: predictData.task_id,
						tx: transmitter.id,
						rx: receiver.id,
					});
				} catch (error) {
					notificationStore.addNotification({
						type: "error",
						message: `Error starting simulation, between ${transmitter.name} and ${receiver.name}: ${error}`,
						title: "Center Node Simulation",
						hideAfter: 5000,
					});
					isSimulationRunning.value = false;
					return;
				}
			}
		}

		for (const task of tasks.value) {
			try {
				const data = await store.fetchSimulationStatus(task.id, 500);

				notificationStore.addNotification({
					type: "success",
					message: `Simulation result, between ${simulation.value.transmitter.find((val) => val.id === task.tx)?.name ?? task.tx} and ${simulation.value.recivers.find((val) => val.id === task.rx)?.name ?? task.rx} fetched successfully.`,
					title: "Center Node Simulation",
					hideAfter: 2000,
				});

				const tx_id = tasks.value.find((val) => val.id === task.id)?.tx;
				const rx_id = tasks.value.find((val) => val.id === task.id)?.rx;

				store.centerNodeSimModeData.table.data.push({
					...(JSON.parse(data.data) as unknown as LosSimulatorResponse),
					tx_id: tx_id ?? "",
					tx_title:
						simulation.value.transmitter.find((val) => val.id === tx_id)
							?.name ?? "",
					rx_id: rx_id ?? "",
					rx_title:
						simulation.value.recivers.find((val) => val.id === rx_id)?.name ??
						"",
				});

				store.centerNodeSimModeData.table.show = false;
				store.centerNodeSimModeData.table.show = true;
			} catch (error) {
				notificationStore.addNotification({
					type: "error",
					message: `Error fetching simulation result for task ${task.id}: ${error}`,
					title: "Center Node Simulation",
					hideAfter: 5000,
				});
			}
		}
		isSimulationRunning.value = false;
	} catch (error) {
		notificationStore.addNotification({
			type: "error",
			message: `Error running simulation: ${error}`,
			title: "Center Node Simulation",
			hideAfter: 5000,
		});
		isSimulationRunning.value = false;
	}
}

onBeforeUnmount(() => {
	for (const marker of markers.value) {
		marker.remove();
	}

	locationPickerSubscription.value?.unsubscribe();

	store.centerNodeSimModeData.table.data.splice(0, store.centerNodeSimModeData.table.data.length);
	store.centerNodeSimModeData.table.show = false;
});
</script>