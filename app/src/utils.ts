import type { LosSimulatorResponse } from "./stores/types";

// biome-ignore lint/suspicious/noExplicitAny: <explanation>
export function cloneObject(item: any) {
	return JSON.parse(JSON.stringify(item));
}

export function getUniqueId(): string {
	return Math.random().toString(16).slice(2);
}

export function processLosData(data: LosSimulatorResponse): {
	distance: number[];
	profile: number[];
	curvature: number[];
	fresnel: number[];
	reference: number[];
} {
	if (data.distance.length <= 100) return data;

	// reduce data resolution to 100 points
	const distance = data.distance as number[];
	const profile = data.profile as number[];
	const curvature = data.curvature as number[];
	const fresnel = data.fresnel as number[];
	const reference = data.reference as number[];

	const reducedDistance: number[] = [];
	const reducedProfile: number[] = [];
	const reducedCurvature: number[] = [];
	const reducedFresnel: number[] = [];
	const reducedReference: number[] = [];

	const step = Math.floor(distance.length / 100);
	for (let i = 0; i < distance.length; i += step) {
		reducedDistance.push(distance[i]);
		reducedProfile.push(profile[i]);
		reducedCurvature.push(curvature[i]);
		reducedFresnel.push(fresnel[i]);
		reducedReference.push(reference[i]);
	}

	// if the last point is not included, add it
	if (
		reducedDistance[reducedDistance.length - 1] !==
		distance[distance.length - 1]
	) {
		reducedDistance.push(distance[distance.length - 1]);
		reducedProfile.push(profile[profile.length - 1]);
		reducedCurvature.push(curvature[curvature.length - 1]);
		reducedFresnel.push(fresnel[fresnel.length - 1]);
		reducedReference.push(reference[reference.length - 1]);
	}

	// if the first point is not included, add it
	if (reducedDistance[0] !== distance[0]) {
		reducedDistance.unshift(distance[0]);
		reducedProfile.unshift(profile[0]);
		reducedCurvature.unshift(curvature[0]);
		reducedFresnel.unshift(fresnel[0]);
		reducedReference.unshift(reference[0]);
	}

	// if the first point is not 0, add it
	if (reducedDistance[0] !== 0) {
		reducedDistance.unshift(0);
		reducedProfile.unshift(profile[0]);
		reducedCurvature.unshift(curvature[0]);
		reducedFresnel.unshift(fresnel[0]);
		reducedReference.unshift(reference[0]);
	}

	return {
		distance: reducedDistance,
		profile: reducedProfile,
		curvature: reducedCurvature,
		fresnel: reducedFresnel,
		reference: reducedReference,
	};
}

export function randomHexColor(): string {
	return `#${Math.floor(Math.random() * 0xffffff)
		.toString(16)
		.padStart(6, "0")}`;
}
