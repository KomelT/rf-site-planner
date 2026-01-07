import { ref } from "vue";

export type RadioClimate =
	| "equatorial"
	| "continental_subtropical"
	| "maritime_subtropical"
	| "desert"
	| "continental_temperate"
	| "maritime_temperature_land"
	| "maritime_temperature_sea";

export type Polarization = "vertical" | "horizontal";

export type LosSimulatorPayload = {
	tx_lat: number;
	tx_lon: number;
	tx_height: number;
	tx_power: number;
	tx_gain: number;
	tx_loss: number;
	frequency_mhz: number;
	rx_lat: number;
	rx_lon: number;
	rx_height: number;
	rx_gain: number;
	rx_loss: number;
	clutter_height: number;
	ground_dielectric: number;
	ground_conductivity: number;
	atmosphere_bending: number;
	radio_climate: RadioClimate;
	polarization: Polarization;
	situation_fraction: number;
	time_fraction: number;
	high_resolution: boolean;
	itm_mode: boolean;
};

export type LosSimulatorSite = LosSimulatorPayload & {
	id: string;
	title: string;
};

export type LosSimulatorResponse = {
	distance: number[];
	profile: number[];
	curvature: number[];
	fresnel: number[];
	fresnel_pt_6: number[];
	reference: number[];
	path: {
		obstructed: boolean;
		message: string;
		obstructions: number[][];
	};
	first_fresnel: {
		obstructed: boolean;
		message: string;
	};
	rx_signal_power: number;
	path_loss_rssi: number;
	path_loss: number;
	lr_it_loss_line_type: string;
	lr_it_loss: number;
	lr_it_loss_rssi: number;
};

export type LosSimulatorResponseUpdated = LosSimulatorResponse & {
	tx_id: string;
	tx_title: string;
	rx_id: string;
	rx_title: string;
};

export type CoverageSimulatorPayload = {
	lat: number;
	lon: number;
	tx_height: number;
	tx_power: number;
	tx_gain: number;
	tx_loss: number;
	frequency_mhz: number;
	rx_height: number;
	rx_loss: number;
	clutter_height: number;
	ground_dielectric: number;
	ground_conductivity: number;
	atmosphere_bending: number;
	radio_climate: RadioClimate;
	polarization: Polarization;
	radius: number;
	situation_fraction: number;
	time_fraction: number;
	high_resolution: boolean;
	colormap: string;
	min_dbm: number;
	max_dbm: number;
	itm_mode: boolean;
};

export type CoverageSimulatorSite = CoverageSimulatorPayload & {
	id: string;
	title: string;
	opacity: number;
	wmsUrl?: string;
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

export type CenterNodeSimulatorPayload = {
	frequency_mhz: number;
	clutter_height: number;
	ground_dielectric: number;
	ground_conductivity: number;
	atmosphere_bending: number;
	tx_loss: number;
	radio_climate: RadioClimate;
	polarization: Polarization;
	situation_fraction: number;
	time_fraction: number;
	high_resolution: boolean;
	transmitter: {
		id: string;
		name: string;
		lat: number;
		lon: number;
		height: number;
		gain: number;
		power: number;
	}[];
	recivers: {
		id: string;
		name: string;
		lat: number;
		lon: number;
		height: number;
		gain: number;
	}[];
};

export type CenterNodeSimulatorSite = CenterNodeSimulatorPayload & {
	id: string;
	title: string;
};

export type AreaCenterNodeSimulatorPayload = {
	frequency_mhz: number;
	clutter_height: number;
	ground_dielectric: number;
	ground_conductivity: number;
	atmosphere_bending: number;
	tx_loss: number;
	radio_climate: RadioClimate;
	polarization: Polarization;
	situation_fraction: number;
	time_fraction: number;
	high_resolution: boolean;
	transmitter: {
		height: number;
		gain: number;
		power: number;
	};
	recivers: {
		id: string;
		name: string;
		lat: number;
		lon: number;
		height: number;
		gain: number;
	}[];
};

export type AreaCenterNodeSimulatorSite = AreaCenterNodeSimulatorPayload & {
	id: string;
	title: string;
};

export type OverpassResponse = {
	id: number;
	lat: number;
	lon: number;
	tags: {
		alt_name: string;
		ele: number;
		name: string;
		natural: string;
		source: string;
	};
};
