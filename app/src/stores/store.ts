//import parseGeoraster from "georaster";
//import GeoRasterLayer from "georaster-layer-for-leaflet";
//import L from "leaflet";
import { defineStore } from "pinia";
// import { useLocalStorage } from '@vueuse/core';
import { randanimalSync } from "randanimal";
import { ref } from "vue";
//import "leaflet-easyprint";
import redPinMarker from "../assets/redPinMarker.ts";
import type { Site, SplatParams } from "../types.ts";
import { cloneObject } from "../utils.ts";

const useStore = defineStore("store", {
	state() {
		return {
			//map: undefined as undefined | L.Map,
			//currentMarker: undefined as undefined | L.Marker,
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
	actions: {
		/*setTxCoords(lat: number, lon: number) {
			this.splatParams.transmitter.tx_lat = lat;
			this.splatParams.transmitter.tx_lon = lon;
		},
		removeSite(index: number) {
			if (!this.map) {
				return;
			}
			this.localSites.splice(index, 1);
			this.map.eachLayer((layer: L.Layer) => {
				if (layer instanceof GeoRasterLayer) {
					this.map?.removeLayer(layer);
				}
			});
			this.redrawSites();
		},
		redrawSites() {
			if (!this.map) {
				return;
			}

			// Remove existing GeoRasterLayers
			this.map.eachLayer((layer: L.Layer) => {
				if (layer instanceof GeoRasterLayer) {
					this.map?.removeLayer(layer);
				}
			});

			// Add GeoRasterLayers back to the map
			for (const site of this.localSites) {
				const rasterLayer = new GeoRasterLayer({
					georaster: { ...site }.raster,
					opacity: 0.7,
					noDataValue: 255,
					resolution: 256,
				});
				rasterLayer.addTo(this.map as L.Map);
				rasterLayer.bringToFront();
			}
		},
		initMap() {
			this.map = L.map("map", {
				// center: [51.102167, -114.098667],
				zoom: 10,
				zoomControl: false,
			});
			const position: [number, number] = [
				this.splatParams.transmitter.tx_lat,
				this.splatParams.transmitter.tx_lon,
			];
			this.map.setView(position, 10);

			L.control.zoom({ position: "bottomleft" }).addTo(this.map as L.Map);

			const cartoLight = L.tileLayer(
				"https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
				{
					attribution: "© OpenStreetMap contributors © CARTO",
				},
			);

			const streetLayer = L.tileLayer(
				"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
				{
					attribution: "© OpenStreetMap contributors",
				},
			);

			const satelliteLayer = L.tileLayer(
				"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
				{
					attribution: "Tiles © Esri — Source: Esri, USGS, NOAA",
				},
			);

			const topoLayer = L.tileLayer(
				"https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
				{
					attribution:
						"Map data: © OpenStreetMap contributors, SRTM | OpenTopoMap",
				},
			);

			streetLayer.addTo(this.map as L.Map);

			// Base Layers
			const baseLayers = {
				OSM: streetLayer,
				"Carto Light": cartoLight,
				Satellite: satelliteLayer,
				"Topo Map": topoLayer,
			};

			// EasyPrint control
			// biome-ignore lint/suspicious/noExplicitAny: <explanation>
			(L as any)
				.easyPrint({
					title: "Save",
					position: "bottomleft",
					sizeModes: ["A4Portrait", "A4Landscape"],
					filename: "sites",
					exportOnly: true,
				})
				.addTo(this.map as L.Map);

			L.control
				.layers(
					baseLayers,
					{},
					{
						position: "bottomleft",
					},
				)
				.addTo(this.map as L.Map);

			this.map.on("baselayerchange", () => {
				this.redrawSites(); // Re-apply the GeoRasterLayer on top
			});
			this.currentMarker = L.marker(position, { icon: redPinMarker })
				.addTo(this.map as L.Map)
				.bindPopup("Transmitter site"); // Variable to hold the current marker
			this.redrawSites();
		},*/
		async runSimulation() {
			console.log("Simulation running...");
			try {
				this.simulationState = "running";

				// Send the request to the backend's /predict endpoint
				const predictResponse = await fetch(
					`${import.meta.env.VITE_API_URL}/predict`,
					{
						method: "POST",
						headers: {
							"Content-Type": "application/json",
						},
						body: JSON.stringify(payload),
					},
				);

				if (!predictResponse.ok) {
					this.simulationState = "failed";
					const errorDetails = await predictResponse.text();
					throw new Error(`Failed to start prediction: ${errorDetails}`);
				}

				const predictData = await predictResponse.json();
				const taskId = predictData.task_id;

				console.log(`Prediction started with task ID: ${taskId}`);

				// Poll for task status and result
				const pollInterval = 1000; // 1 seconds
				const pollStatus = async () => {
					const statusResponse = await fetch(
						`${import.meta.env.VITE_API_URL}/status/${taskId}`,
					);
					if (!statusResponse.ok) {
						throw new Error("Failed to fetch task status.");
					}

					const statusData = await statusResponse.json();
					console.log("Task status:", statusData);

					if (statusData.status === "completed") {
						this.simulationState = "completed";
						console.log("Simulation completed! Adding result to the map...");

						// Fetch the GeoTIFF data
						const resultResponse = await fetch(
							`${import.meta.env.VITE_API_URL}/result/${taskId}`,
						);
						if (!resultResponse.ok) {
							throw new Error("Failed to fetch simulation result.");
						}
						const arrayBuffer = await resultResponse.arrayBuffer();
						/* const geoRaster = await parseGeoraster(arrayBuffer);
						this.localSites.push({
							params: cloneObject(this.splatParams),
							taskId,
							raster: geoRaster,
						});
						this.currentMarker?.removeFrom(this.map as L.Map);
						this.splatParams.transmitter.name = await randanimalSync();
						this.redrawSites(); */
					} else if (statusData.status === "failed") {
						this.simulationState = "failed";
					} else {
						setTimeout(pollStatus, pollInterval); // Retry after interval
					}
				};

				pollStatus(); // Start polling
			} catch (error) {
				console.error("Error:", error);
			}
		},
	},
});

export { useStore };
