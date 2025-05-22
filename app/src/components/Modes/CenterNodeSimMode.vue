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
      <ModeDataAccordian title="Transmitter options" markerColor="#FF0000"
        v-model:showSection="showSections.transmitter">
        <div class="flex flex-row gap-2">
          <InputNumber title="Latitude" v-model:value="simulation.lat" :disabled="true" />
          <InputNumber title="Longtitude" v-model:value="simulation.lon" :disabled="true" />
        </div>
        <div class="flex flex-row gap-2 mt-3">
          <Button text="Fly to coordinates" @click="flyToNode(simulation.lat, simulation.lon)" />
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
import { type ComputedRef, type Ref, computed, ref, watch } from "vue";
import { useNotificationStore } from "../../stores/notification";
import { useStore } from "../../stores/store";
import type { CenterNodeSimulatorSite } from "../../stores/types";
import { randomHexColor } from "../../utils";
import Button from "../Inputs/Button.vue";
import DropDown from "../Inputs/DropDown.vue";
import InputNumber from "../Inputs/InputNumber.vue";
import InputText from "../Inputs/InputText.vue";
import ModeDataAccordian from "./ModeDataAccordian.vue";

const map = useMap();

const currentMarker = ref<Marker | null>(null);
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
			lat: 0,
			lon: 0,
			tx_power: 0.1,
			frequency_mhz: 868.5,
			tx_height: 2,
			tx_gain: 2,
			recivers: [
				{
					id: randomHexColor(),
					name: "Receiver 1",
					lat: 45.8481696198,
					lon: 13.7311562054,
					gain: 2,
					height: 2,
				},
				{
					id: randomHexColor(),
					name: "Receiver 2",
					lat: 45.8467440547,
					lon: 13.72315913,
					gain: 2,
					height: 2,
				},
			],
		};
	},
);

if (simulations.value.length === 0) {
	simulations.value.push(defautltSimulationValues.value);
}

const currentReceiver = ref(simulations.value[0].recivers[0]);

const simulationsOptions = computed(() => {
	return simulations.value.map((simulation) => ({
		id: simulation.id,
		title: simulation.title,
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
	(sim) => {
		if (!map.isLoaded || !map.map) return;

		// remove all markers
		for (const marker of markers.value) {
			marker.remove();
		}

		markers.value = [];

		// add new markers according to the simulation
		for (const reciver of simulation.value.recivers) {
			if (!map.map) continue;

			const marker = new Marker({
				color: reciver.id,
			})
				.setLngLat([reciver.lon, reciver.lat])
				.addTo(map.map);

			markers.value.push(marker);

			const popup = new Popup({ offset: 25 })
				.setHTML(
					`<div class="text-sm text-center">
            <p>Receiver</p>
            <p>Gain: ${reciver.gain} dB</p>
            <p>Height: ${reciver.height} m</p>
          </div>`,
				)
				.setMaxWidth("300px");

			marker.setPopup(popup);

			popup.addTo(map.map);
		}
	},
	{ immediate: true, deep: true },
);

function addReceiverLocationListener() {
	if (!map.isLoaded || !map.map) return;

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
		lat: simulation.value.lat,
		lon: simulation.value.lon,
		gain: 2,
		height: 2,
	});
}

function runSimulation() {
	console.log("Running simulation");
}
</script>