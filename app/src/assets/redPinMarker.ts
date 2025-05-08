import { getUniqueId } from "../utils";

function getMarker(): HTMLDivElement {
	const el = document.createElement("div");
	el.id = getUniqueId();
	el.innerHTML = `
    <ul style="list-style-type: none; padding: 0; margin: 0;">
        <li style="color: red; font-size: 30px;">📍</li>
    </ul>`;
	return el;
}
export default getMarker;
