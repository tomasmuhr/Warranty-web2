<template>
	<div class="col">
		<div class="card h-100">
			<!-- The dynamic component allows us to switch between router-link, a, or button -->
			<component
				:is="tag"
				class="card-link"
				:class="{
					'btn btn-link border-0 w-100 h-100': tag === 'button',
				}"
				v-bind="$attrs"
			>
				<div class="card-body pt-4">
					<div class="card-icon">{{ icon }}</div>
					<h5 class="card-title mt-3">{{ title }}</h5>
					<p class="card-text">{{ text }}</p>
				</div>
				<div class="card-footer">
					<small class="text-muted">{{ footerText }}</small>
				</div>
			</component>
		</div>
	</div>
</template>

<script setup>
	defineOptions({
		inheritAttrs: false,
	});

	defineProps({
		tag: {
			type: String,
			default: "div",
		},
		icon: {
			type: String,
			required: true,
		},
		title: {
			type: String,
			required: true,
		},
		text: {
			type: String,
			required: true,
		},
		footerText: {
			type: String,
			required: true,
		},
	});
</script>
