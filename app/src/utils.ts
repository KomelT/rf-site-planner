// biome-ignore lint/suspicious/noExplicitAny: <explanation>
export function cloneObject(item: any) {
	return JSON.parse(JSON.stringify(item));
}
