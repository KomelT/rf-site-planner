import { defineStore } from "pinia";
import { randanimalSync } from "randanimal";
import { ref } from "vue";
import type { Site, SplatParams } from "../types.ts";

const useStore = defineStore("store", {
	state() {
		return {
			mobileMenuOpen: ref(true),
			localSites: [] as Site[], //useLocalStorage('localSites', ),
			simulationState: "idle",
			splatParams: <SplatParams>{
				transmitter: {
					name: randanimalSync(),
					tx_lat: 45.854746,
					tx_lon: 13.726172,
					tx_power: 0.1,
					tx_freq: 868.5,
					tx_height: 2.0,
					tx_gain: 2.0,
				},
				receiver: {
					rx_sensitivity: -130.0,
					rx_height: 1.0,
					rx_gain: 2.0,
					rx_loss: 2.0,
				},
				environment: {
					radio_climate: "continental_temperate",
					polarization: "vertical",
					clutter_height: 1.0,
					ground_dielectric: 15.0,
					ground_conductivity: 0.005,
					atmosphere_bending: 301.0,
				},
				simulation: {
					situation_fraction: 95.0,
					time_fraction: 95.0,
					simulation_extent: 30.0,
					high_resolution: false,
				},
				display: {
					color_scale: "plasma",
					min_dbm: -130.0,
					max_dbm: -80.0,
					overlay_transparency: 50,
				},
			},
		};
	},
});

export { useStore };
