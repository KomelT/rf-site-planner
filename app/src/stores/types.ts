import { ref } from "vue";

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
