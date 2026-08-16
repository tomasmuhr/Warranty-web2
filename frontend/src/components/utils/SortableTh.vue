<!-- SortableTh.vue -->
<template>
	<th
		role="button"
		class="sortable"
		:aria-sort="
			active ? (direction === 'asc' ? 'ascending' : 'descending') : 'none'
		"
		@click="$emit('sort')"
	>
		<slot />
		<span v-if="active">{{ direction === "asc" ? "▲" : "▼" }}</span>
	</th>
</template>

<script setup>
	defineProps({
		active: Boolean,
		direction: { type: String, default: "asc" },
	});
	defineEmits(["sort"]);
</script>
