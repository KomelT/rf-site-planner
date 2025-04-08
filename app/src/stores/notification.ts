import { defineStore } from "pinia";
import { type Ref, ref } from "vue";

export type Notification = {
	id: string;
	type: "info" | "success" | "warning" | "error";
	title: string;
	message: string;
	hideAfter: number;
};

export const useNotificationStore = defineStore("notification", () => {
	const notifications: Ref<Notification[]> = ref([]);

	function addNotification(notification: Omit<Notification, "id">) {
		const id = Math.random().toString(36).substring(7);
		notifications.value.push({ ...notification, id });

		if (notification.hideAfter !== 0) {
			setTimeout(() => {
				const index = notifications.value.findIndex((n) => n.id === id);
				if (index !== -1) notifications.value.splice(index, 1);
			}, notification.hideAfter);
		}
	}

	function closeNotification(id: string) {
		const index = notifications.value.findIndex((n) => n.id === id);
		if (index !== -1) notifications.value.splice(index, 1);
	}

	return {
		notifications,
		addNotification,
		closeNotification,
	};
});
