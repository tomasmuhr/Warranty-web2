<template>
	<BaseModal
		:id="modalId"
		size="sm"
	>
		<template #title>
			{{ title }}
		</template>

		<template #body>
			<slot>{{ message }}</slot>
		</template>

		<template #footer>
			<button
				type="button"
				class="btn btn-sm btn-secondary"
				data-bs-dismiss="modal"
			>
				Close
			</button>
			<button
				type="button"
				:class="['btn', 'btn-sm', confirmClass]"
				data-bs-dismiss="modal"
				@click="$emit('confirm')"
			>
				{{ confirmLabel }}
			</button>
		</template>
	</BaseModal>

	<!-- Trigger Button -->
	<button
		type="button"
		class="btn btn-danger btn-sm"
		data-bs-toggle="modal"
		:data-bs-target="`#${modalId}`"
	>
		Delete
	</button>
</template>

<script setup>
	import BaseModal from "../base/BaseModal.vue";

	defineProps({
		title: { type: String, default: "Confirm" },
		message: { type: String, default: "" },
		confirmLabel: { type: String, default: "Confirm" },
		confirmClass: { type: String, default: "btn-primary" },
	});

	defineEmits(["confirm", "close"]);

	const modalId = `confirm-${Math.random().toString(36).slice(2)}`;
</script>
