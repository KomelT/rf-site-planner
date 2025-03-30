<template>
	<div>
		<div v-if="showSelector">
			<p class="text-lg font-bold py-2">Select mode:</p>
			<div class="grid grid-cols-2 gap-2">
				<Mode v-for="(mode, index) in modes" :key="index" :title="mode.title" :description="mode.description"
					:image="mode.image" @click="mode.onClick" />
			</div>
		</div>
		<ModeWrapper v-else :title="selectedModeText" @backButtonClick="showSelector = false">
			<CoverageSimulatorMode v-if="showCoverageSim" />
		</ModeWrapper>
	</div>
</template>
<script setup lang="ts">
import { computed, ref } from "vue";
import CoverageSimulatorMode from "../Modes/CoverageSimulatorMode.vue";
import ModeWrapper from "../Modes/ModeWrapper.vue";
import Mode from "./Mode.vue";

const showCoverageSim = ref(false);

const selectedModeText = ref("");
const showSelector = computed({
	get: () => {
		return !showCoverageSim.value;
	},
	set: (value: boolean) => {
		showCoverageSim.value = value;
	},
});

const modes = [
	{
		title: "Coverage simulator:",
		description: "Simulate coverage of a mesh network",
		image: import("../../assets/coverage-simulator.jpg"),
		onClick: () => {
			showCoverageSim.value = true;
			selectedModeText.value = "Coverage simulator";
		},
	},
];
</script>