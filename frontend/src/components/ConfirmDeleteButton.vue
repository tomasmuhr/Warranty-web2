<template>
	<div
		class="modal fade"
		:id="modalId"
		tabindex="-1"
		aria-hidden="true"
	>
		<div class="modal-dialog modal-sm">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">{{ title }}</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					<slot>{{ message }}</slot>
				</div>
				<div class="modal-footer">
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
				</div>
			</div>
		</div>
	</div>
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
	defineProps({
		title: { type: String, default: "Confirm" },
		message: { type: String, default: "" },
		confirmLabel: { type: String, default: "Confirm" },
		confirmClass: { type: String, default: "btn-primary" },
	});

	defineEmits(["confirm", "close"]);

	const modalId = `confirm-${Math.random().toString(36).slice(2)}`;
</script>
