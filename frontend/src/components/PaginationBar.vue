<template>
	<nav
		v-if="pages > 1"
		aria-label="Page navigation"
	>
		<ul class="pagination pagination-sm justify-content-center">
			<li :class="['page-item', { disabled: page <= 1 }]">
				<button
					class="page-link"
					:disabled="page <= 1"
					@click="$emit('change', page - 1)"
				>
					Previous
				</button>
			</li>
			<li
				v-for="number in pages"
				:key="number"
				:class="['page-item', { active: page === number }]"
			>
				<button
					class="page-link"
					@click="$emit('change', number)"
				>
					{{ number }}
				</button>
			</li>
			<li :class="['page-item', { disabled: page >= pages }]">
				<button
					class="page-link"
					:disabled="page >= pages"
					@click="$emit('change', page + 1)"
				>
					Next
				</button>
			</li>
		</ul>
	</nav>
</template>

<script setup>
	defineProps({
		page: { type: Number, required: true },
		pages: { type: Number, required: true },
	});

	defineEmits(["change"]);
</script>
