<template>
	<!-- The 'id' prop allows Bootstrap to target this specific modal -->
	<div
		class="modal fade"
		:id="id"
		tabindex="-1"
		aria-hidden="true"
	>
		<!-- The 'size' prop allows us to easily make it modal-sm, modal-lg, etc. -->
		<div
			class="modal-dialog"
			:class="sizeClass"
		>
			<div class="modal-content">
				<div class="modal-header">
					<!-- * SLOT - TITLE -->
					<h5 class="modal-title">
						<slot name="title">Default Title</slot>
					</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>

				<!-- * SLOT - BODY -->
				<div class="modal-body">
					<slot name="body"></slot>
				</div>

				<!-- * SLOT - FOOTER. Only renders if content is passed to it. -->
				<div
					class="modal-footer"
					v-if="$slots.footer"
				>
					<slot name="footer"></slot>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { computed } from "vue";

	const props = defineProps({
		id: {
			type: String,
			required: true,
		},
		size: {
			type: String,
			default: "md", // Options: 'sm', 'md', 'lg', 'xl'
		},
	});

	const sizeClass = computed(() => {
		if (props.size === "md") return ""; // Bootstrap defaults to medium
		return `modal-${props.size}`;
	});
</script>
