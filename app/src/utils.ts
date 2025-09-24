import type { LosSimulatorResponse } from "./stores/types";

// biome-ignore lint/suspicious/noExplicitAny: <explanation>
export function cloneObject(item: any) {
	return JSON.parse(JSON.stringify(item));
}

export function getUniqueId(): string {
	return Math.random().toString(16).slice(2);
}

function alignAndDownsample(
	distance: number[],
	series: number[][],
	maxPts = 500,
	maxSkew = 5
): { aligned: number[][], idx: number[] } {
	function bestShift(ref: number[], s: number[], maxShift: number): number {
		let best = 0;
		let bestScore = Number.POSITIVE_INFINITY;

		for (let sh = -maxShift; sh <= maxShift; sh++) {
			// Overlap indices after shifting s by sh relative to ref
			const startRef = Math.max(0, -sh);
			const startS = Math.max(0, sh);
			const endRef = Math.min(ref.length, s.length - sh);
			const endS = Math.min(s.length, ref.length + sh);

			const overlap = Math.min(endRef - startRef, endS - startS);
			if (overlap <= 1) continue; // need at least 2 points to compare ends

			const r0 = ref[startRef];
			const r1 = ref[endRef - 1];
			const s0 = s[startS];
			const s1 = s[endS - 1];

			// Score: boundary mismatch (use absolute difference)
			const score = Math.abs(s0 - r0) + Math.abs(s1 - r1);
			if (score < bestScore) {
				bestScore = score;
				best = sh;
			}
		}
		return best;
	}

	// Compute best shift for each non-reference series *against distance*
	const shifts = series.map(s => bestShift(distance, s, maxSkew));

	// Compute common overlap range after shifts
	// For the reference (distance), shift = 0
	const allShifts = [0, ...shifts];
	const lengths = [distance.length, ...series.map(s => s.length)];

	// For each array i, valid ref indices are:
	// [max(0, -shift_i) ... min(refLen, len_i - shift_i))
	let left = 0;
	let right = distance.length;
	for (let i = 0; i < allShifts.length; i++) {
		const sh = allShifts[i];
		const len = lengths[i];
		const li = Math.max(0, -sh);
		const ri = Math.min(distance.length, len - sh);
		left = Math.max(left, li);
		right = Math.min(right, ri);
	}
	if (right - left < 2) {
		throw new Error("Premalo skupnega prekrivanja po poravnavanju (right-left < 2).");
	}

	// Build aligned (cropped & shifted) arrays
	const alignedDistance = distance.slice(left, right);
	const alignedSeries = series.map((s, i) => {
		const sh = shifts[i];
		const start = left + sh;
		const end = right + sh;
		return s.slice(start, end);
	});

	// Downsample all aligned arrays together to ≤ maxPts (keep first & last)
	function downsampleAligned(seriesAll: number[][], maxPoints: number): { out: number[][], idx: number[] } {
		const n = seriesAll[0].length;
		if (seriesAll.some(s => s.length !== n)) throw new Error("Nizi niso poravnani po dolžini.");
		if (n <= maxPoints) return { out: seriesAll, idx: [...Array(n).keys()] };

		const idx: number[] = [];
		const step = (n - 1) / (maxPoints - 1);
		const used = new Set<number>();
		for (let i = 0; i < maxPoints; i++) {
			const j = Math.round(i * step);
			const k = Math.max(0, Math.min(n - 1, j));
			if (!used.has(k)) {
				idx.push(k);
				used.add(k);
			}
		}
		// ensure first/last
		if (idx[0] !== 0) idx.unshift(0);
		if (idx[idx.length - 1] !== n - 1) idx.push(n - 1);
		// trim if over
		if (idx.length > maxPoints) idx.length = maxPoints;

		const out = seriesAll.map(s => idx.map(i => s[i]));
		return { out, idx };
	}

	const { out, idx } = downsampleAligned([alignedDistance, ...alignedSeries], maxPts);
	// Return aligned & reduced (without reordering series)
	return { aligned: out, idx };
}

export function processLosData(data: LosSimulatorResponse): {
	distance: number[];
	profile: number[];
	curvature: number[];
	fresnel: number[];
	fresnel_pt_6: number[];
	reference: number[];
} {

	const maxPoints = 1000;

	if (data.distance.length <= maxPoints) return data;

	const distance = data.distance as number[];
	const profile = data.profile as number[];
	const curvature = data.curvature as number[];
	const fresnel = data.fresnel as number[];
	const fresnel_pt_6 = data.fresnel_pt_6 as number[];
	const reference = data.reference as number[];


	const [
		reducedDistance,
		reducedProfile,
		reducedCurvature,
		reducedFresnel,
		reducedFresnelPt6,
		reducedReference
	] = alignAndDownsample(distance, [
		profile, curvature, fresnel, fresnel_pt_6, reference
	], maxPoints, 5).aligned;

	return {
		distance: reducedDistance,
		profile: reducedProfile,
		curvature: reducedCurvature,
		fresnel: reducedFresnel,
		fresnel_pt_6: reducedFresnelPt6,
		reference: reducedReference,
	};
}

export function randomHexColor(): string {
	return `#${Math.floor(Math.random() * 0xffffff)
		.toString(16)
		.padStart(6, "0")}`;
}

export function isMobileDevice(): boolean {
	return /Mobi|Android/i.test(navigator.userAgent);
}