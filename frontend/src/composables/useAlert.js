import { reactive } from "vue";

export function useAlert() {
	const alert = reactive({ message: "", type: "success" });

	function showAlert(message, type = "success") {
		alert.message = message;
		alert.type = type;
	}

	return { alert, showAlert };
}
