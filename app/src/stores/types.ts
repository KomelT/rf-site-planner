import { ref } from "vue";

export type CoverageSimulatorPayload = {
	lat: number;
	lon: number;
	tx_height: number;
	tx_power: number;
	tx_gain: number;
	frequency_mhz: number;
	rx_height: number;
	rx_gain: number;
	signal_threshold: number;
	system_loss: number;
	clutter_height: number;
	ground_dielectric: number;
	ground_conductivity: number;
	atmosphere_bending: number;
	radio_climate:
		| "equatorial"
		| "continental_subtropical"
		| "maritime_subtropical"
		| "desert"
		| "continental_temperate"
		| "maritime_temperature_land"
		| "maritime_temperature_sea";
	polarization: "vertical" | "horizontal";
	radius: number;
	situation_fraction: number;
	time_fraction: number;
	high_resolution: boolean;
	colormap: string;
	min_dbm: number;
	max_dbm: number;
};

export type CoverageSimulatorSite = CoverageSimulatorPayload & {
	id: string;
	title: string;
};

export const climateOptions = ref([
	{ id: "equatorial", title: "Equatorial" },
	{ id: "continental-subtropical", title: "Continental subtropical" },
	{ id: "maritime-subtropical", title: "Maritime subtropical" },
	{ id: "desert", title: "Desert" },
	{ id: "continental-temperature", title: "Continental temperature" },
	{ id: "maritime-temperature-land", title: "Maritime temperature (land)" },
	{ id: "maritime-temperature-sea", title: "Maritime temperature (sea)" },
]);

export const polarizationOptions = ref([
	{ id: "vertical", title: "Vertical" },
	{ id: "horizontal", title: "Horizontal" },
]);
