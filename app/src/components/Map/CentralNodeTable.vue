<template>
  <MglCustomControl v-if="store.centralNodeTable.show" :position="props.position">
    <table class="table table-striped table-bordered text-black m-1 bg-white">
      <thead>
        <tr>
          <th class="px-1">Transmitter</th>
          <th v-for="(col, index) in colsNames" class="px-1" :key="index">{{ col }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, rowIndex) in rows" :key="rowIndex">
          <td v-for="(cell, cellIndex) in row" class="px-1" :key="cellIndex">{{ cell }}</td>
        </tr>
      </tbody>
    </table>
		<DropDown title="Sort methods" :options="sortMethods" v-model="selectedSortMethod" />
  </MglCustomControl>
</template>
<script setup lang="ts">
import { MglCustomControl } from "@indoorequal/vue-maplibre-gl";
import type { ControlPosition } from "maplibre-gl";
import { ref, watch } from "vue";
import { useStore } from "../../stores/store";
import DropDown from "../Inputs/DropDown.vue";

export type CentralNodetableProps = {
	position: ControlPosition | undefined;
};

const sortMethods = [
	{ id: "average", title: "Average"}
]
const selectedSortMethod = ref(sortMethods[0].id);

const props = defineProps<CentralNodetableProps>();

const store = useStore();

const cols = ref<string[]>([]);
const colsNames = ref<string[]>([]);
const rows = ref<string[][]>([]);

watch(
	() => store.centralNodeTable.data,
	(newData) => {
		if (newData.length > 0) {
			// Extract unique rx_ids once
			cols.value = Array.from(new Set(newData.map((val) => val.rx_id)));

			// Map column IDs to titles
			colsNames.value = cols.value.map((colId) => {
				const node = newData.find((val) => val.rx_id === colId);
				return node ? node.rx_title : colId;
			});

			// create array of tx_ids
			const txIds = Array.from(new Set(newData.map((val) => val.tx_id)));

			// Create rows based on tx_ids
			rows.value = txIds.map((txId) => {
				const row = [
					`${newData.find((val) => val.tx_id === txId)?.tx_title || txId}`,
				];
				for (const colId of cols.value) {
					const value = newData.find(
						(val) => val.tx_id === txId && val.rx_id === colId,
					);
					row.push(value ? `${value.rx_signal_power} dBm` : "N/A");
				}
				return row;
			});
		} else {
			cols.value = [];
			colsNames.value = [];
			rows.value = [];
		}
	},
	{ immediate: true, deep: true },
);
</script>