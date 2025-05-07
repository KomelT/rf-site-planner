<template>
	<div>
		<div v-if="!anySimTrue">
			<div class="flex items-center justify-between">
				<p class="text-lg font-bold py-2">Select mode:</p>
				<button type="button" class="cursor-pointer -m-2.5 rounded-md p-2.5 text-gray-700"
					@click="store.mobileMenuOpen = false">
					<span class="sr-only">Close menu</span>
					<XMarkIcon class="size-6 text-gray-200" aria-hidden="true" />
				</button>
			</div>
			<div class="grid grid-cols-2 gap-2">
				<Mode v-for="(mode, index) in modes" :key="index" :title="mode.title" :description="mode.description"
					:image="mode.image" @click="mode.onClick" />
			</div>
		</div>
		<ModeWrapper v-else :title="selectedModeText" @backButtonClick="toggleSim()">
			<CoverageSimulatorMode v-if="showSim.showCoverageSim" />
			<LosSimulatorMode v-else-if="showSim.showLosSim" />
		</ModeWrapper>
	</div>
</template>
<script setup lang="ts">
import { XMarkIcon } from "@heroicons/vue/24/outline";
import { computed, ref } from "vue";
import { useStore } from "../../stores/store";
import CoverageSimulatorMode from "../Modes/CoverageSimulatorMode.vue";
import LosSimulatorMode from "../Modes/LosSimulatorMode.vue";
import ModeWrapper from "../Modes/ModeWrapper.vue";
import Mode from "./Mode.vue";

const store = useStore();

const showSim = ref({
	showCoverageSim: false,
	showLosSim: false,
});

type ShowSimKeys = keyof typeof showSim.value;

const anySimTrue = computed(() => {
	return Object.values(showSim.value).some((value) => value === true);
});

const selectedModeText = ref("");
function toggleSim(sim?: ShowSimKeys) {
	for (const key in showSim.value) {
		showSim.value[key] = false;
	}

	if (sim) showSim.value[sim] = true;
}

const modes = [
	{
		title: "Coverage simulator",
		description: "Simulate coverage of a mesh network",
		image: import("../../assets/coverage-simulator.jpg"),
		onClick: () => {
			toggleSim("showCoverageSim");
			selectedModeText.value = "Coverage simulator";
		},
	},
	{
		title: "Line Of Sight sim.",
		description: "Simulate line of sight between two points",
		image: import("../../assets/los-simulator.jpg"),
		onClick: () => {
			toggleSim("showLosSim");
			selectedModeText.value = "Line Of Sight simulator";
		},
	},
];
</script>