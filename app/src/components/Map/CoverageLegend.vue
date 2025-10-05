<template>
	<MglCustomControl v-if="store.coverSimModeData.legend.show" :position="props.position"
		class="maplibregl-ctrl maplibregl-ctrl-group ml-2! sm:ml-0! w-auto">
		<div :class="['bg-white border rounded shadow-lg sm:max-w-96', hide ? 'border-gray-100' : 'border-gray-300']">
			<Button v-if="hide" text="Show" @click="hide = false" class="py-1! w-auto! px-2! m-2 bg-orange-400!" />
			<div v-if="!hide" class="">
				<img :src="`data:image/png;base64,${store.coverSimModeData.legend.data}`" alt="Legend"
					class="rounded-md border border-gray-300 shadow-md h-[calc(80vh)]" />
			</div>
		</div>
	</MglCustomControl>
</template>
<script setup lang="ts">
import { MglCustomControl } from "@indoorequal/vue-maplibre-gl";
import type { ControlPosition } from "maplibre-gl";
import { ref } from "vue";
import { useStore } from "../../stores/store";
import Button from "../Inputs/Button.vue";

export type CoverageLegendProps = {
	position: ControlPosition | undefined;
};

const hide = ref(false);

const props = defineProps<CoverageLegendProps>();

const store = useStore();
</script>