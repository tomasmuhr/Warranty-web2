<template>
	<div
		v-if="message"
		:class="`alert alert-${type} alert-dismissible fade show`"
		role="alert"
	>
		{{ message }}
		<button
			type="button"
			class="btn-close"
			aria-label="Close"
			@click="$emit('close')"
		></button>
	</div>
</template>

<script setup>
	defineProps({
		message: { type: String, default: "" },
		type: { type: String, default: "success" },
	});

	defineEmits(["close"]);
</script>
