<template>
	<MglCustomControl v-if="store.centerNodeSimModeData.table.show" :position="props.position" class="maplibregl-ctrl maplibregl-ctrl-group ml-2! sm:ml-0! w-auto">
		<div :class="['bg-white border rounded shadow-lg', hide ? 'border-gray-100' : 'border-gray-300']">
			<Button v-if="hide" text="Show" @click="hide = false" class="py-1! w-auto! px-2! m-2 bg-orange-400!" />
			<div v-if="!hide" class="">
				<div class="grid grid-cols-7 gap-2 m-3 items-end">
					<div class="col-span-4">
						<h2 class="text-lg font-medium text-gray-900">Central Node Table</h2>
						<p class="mt-1 text-sm text-gray-600">Signal power between central node and other nodes</p>
					</div>
					<div class="col-span-3">
						<div class="flex justify-end items-center">
							<Button text="Hide" @click="hide = true" class="py-1! w-auto! px-2! bg-orange-400!" />
							<button @click="store.centerNodeSimModeData.table.show = false"
								class="ml-2 inline-flex items-center border-none! rounded-md bg-white p-1 text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
								<span class="sr-only">Close panel</span>
								<svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
									stroke-width="1.5" stroke="currentColor" aria-hidden="true">
									<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
								</svg>
							</button>
						</div>
						<DropDown title="Sort methods" :options="sortMethods" v-model:selected="selectedSortMethod"
							:btnOptions="{ labelColor: 'text-gray-900' }" />
					</div>
				</div>
				<div class="mt-8 px-1 flow-root">
					<div class="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
						<div class="inline-block min-w-full py-2 align-middle sm:px-6">
							<table class="relative min-w-full divide-y divide-gray-300">
								<thead>
									<tr>
										<th scope="col" class="py-3.5 px-1 text-center text-sm font-semibold text-gray-800">
											<a href="#" class="group inline-flex" @click="sortByColumn(0)">
												TX / RX
												<span class="sm:ml-2 flex-none rounded text-gray-400">
													<ChevronUpIcon v-if="colsSortWays.get(0) === 'desc'" class="size-5" aria-hidden="true" />
													<ChevronDownIcon v-else class="size-5" aria-hidden="true" />
												</span>
											</a>
										</th>
										<th v-for="(col, index) in colsNames" :key="index" scope="col"
											class="py-3 sm:py-4 px-0 sm:px-1 text-center text-sm font-semibold text-gray-900">
											<a href="#" class="group inline-flex" @click="sortByColumn(index + 1)">
												{{ col }}
												<span class="sm:ml-2 flex-none rounded text-gray-400">
													<ChevronUpIcon v-if="colsSortWays.get(index + 1) === 'desc'" class="size-5"
														aria-hidden="true" />
													<ChevronDownIcon v-else class="size-5" aria-hidden="true" />
												</span>
											</a>
										</th>
									</tr>
								</thead>
								<tbody class="divide-y divide-gray-200">
									<tr v-for="(row, rowIndex) in rows" :key="rowIndex" class="">
										<td v-for="(cell, cellIndex) in row" :key="cellIndex"
											class="whitespace-nowrap text-center py-3 sm:py-4 px-0 sm:px-1 text-sm font-medium text-gray-900">
											{{ cell }}</td>
									</tr>
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
	</MglCustomControl>
</template>
<script setup lang="ts">
import { MglCustomControl } from "@indoorequal/vue-maplibre-gl";
import type { ControlPosition } from "maplibre-gl";
import { ref, watch } from "vue";
import { useStore } from "../../stores/store";
import DropDown from "../Inputs/DropDown.vue";
import Button from "../Inputs/Button.vue";
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/vue/20/solid'

export type CentralNodetableProps = {
	position: ControlPosition | undefined;
};

const hide = ref(false);

const sortMethods = [
	{ id: "custom", title: "Custom" },
	{ id: "max", title: "Max" },
	{ id: "min", title: "Min" },
	{ id: "average", title: "Average" }
]
const selectedSortMethod = ref(sortMethods[0]);
const selectedSortId = () => selectedSortMethod.value?.id ?? "custom";

const props = defineProps<CentralNodetableProps>();

const store = useStore();

const cols = ref<string[]>([]);
const colsNames = ref<string[]>([]);
const baseRows = ref<string[][]>([]);
const rows = ref<string[][]>([]);
const colsSortWays = ref<Map<number, 'asc' | 'desc'>>(new Map());
const skipCustomReset = ref(false);

const parseRSSI = (value: string) => {
	const parsed = Number.parseFloat(value.split(" ")[0]);
	return Number.isFinite(parsed) ? parsed : null;
};

const getRowStats = (row: string[]) => {
	const values = row
		.slice(1)
		.map(parseRSSI)
		.filter((val): val is number => val !== null);

	if (values.length === 0) {
		return { hasValues: false, min: Number.POSITIVE_INFINITY, max: Number.NEGATIVE_INFINITY, avg: Number.NEGATIVE_INFINITY };
	}

	const min = Math.min(...values);
	const max = Math.max(...values);
	const avg = values.reduce((sum, val) => sum + val, 0) / values.length;
	return { hasValues: true, min, max, avg };
};

const applySortMethod = (method: string) => {
	if (method === "custom") {
		rows.value = [...baseRows.value];
		return;
	}

	const sorted = [...baseRows.value].sort((a, b) => {
		const aStats = getRowStats(a);
		const bStats = getRowStats(b);

		if (!aStats.hasValues && !bStats.hasValues) {
			return a[0].localeCompare(b[0], undefined, { numeric: true, sensitivity: "base" });
		}
		if (!aStats.hasValues) return 1;
		if (!bStats.hasValues) return -1;

		if (method === "min") {
			if (aStats.min !== bStats.min) return aStats.min - bStats.min;
		} else if (method === "max") {
			if (aStats.max !== bStats.max) return bStats.max - aStats.max;
		} else if (method === "average") {
			if (aStats.avg !== bStats.avg) return bStats.avg - aStats.avg;
		}

		return a[0].localeCompare(b[0], undefined, { numeric: true, sensitivity: "base" });
	});

	rows.value = sorted;
};

watch(
	() => store.centerNodeSimModeData.table.data,
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
			baseRows.value = txIds.map((txId) => {
				const row = [
					`${newData.find((val) => val.tx_id === txId)?.tx_title || txId}`,
				];
				for (const colId of cols.value) {
					const value = newData.find(
						(val) => val.tx_id === txId && val.rx_id === colId,
					);
					row.push(value ? `${value.rx_signal_power.toFixed(2)} dBm` : "N/A");
				}
				return row;
			});
			rows.value = [...baseRows.value];
			applySortMethod(selectedSortId());
		} else {
			cols.value = [];
			colsNames.value = [];
			baseRows.value = [];
			rows.value = [];
		}
	},
	{ immediate: true, deep: true },
);

watch(selectedSortMethod, (method) => {
	const methodId = method?.id ?? "custom";
	if (methodId === "custom" && skipCustomReset.value) {
		skipCustomReset.value = false;
		return;
	}
	applySortMethod(methodId);
});

function sortByColumn(columnIndex: number) {
	skipCustomReset.value = true;
	selectedSortMethod.value = sortMethods[0];
	const isRSSI = columnIndex > 0;

	// 1) decide next direction first (outside comparator)
	const current = colsSortWays.value.get(columnIndex) ?? 'desc';
	const next = current === 'asc' ? 'desc' : 'asc';
	colsSortWays.value.set(columnIndex, next);
	const dir = next === 'asc' ? 1 : -1;

	const compare = (a: string, b: string): number => {
		let an = 0;
		let bn = 0;

		if (isRSSI) {
			an = parseFloat(a.split(" ")[0]);
			bn = parseFloat(b.split(" ")[0]);
		} else {
			an = parseFloat(a.split(" ")[1]);
			bn = parseFloat(b.split(" ")[1]);
		}

		if (!isNaN(an) && !isNaN(bn)) {
			return an - bn;
		}
		// fallback: natural string compare
		return a.localeCompare(b, undefined, { numeric: true, sensitivity: 'base' });
	};

	// 3) sort (clone to ensure Vue reactivity if needed)
	rows.value = [...rows.value].sort((r1, r2) => compare(r1[columnIndex], r2[columnIndex]) * dir);
}

</script>
