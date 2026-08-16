<template>
	<nav
		v-if="pages > 1"
		aria-label="Page navigation"
	>
		<ul class="pagination pagination-sm justify-content-center">
			<!-- Previous Button -->
			<li :class="['page-item', { disabled: page <= 1 }]">
				<button
					class="page-link"
					:disabled="page <= 1"
					@click="$emit('change', page - 1)"
				>
					Previous
				</button>
			</li>

			<!-- Dynamic Page Items & Ellipses -->
			<template
				v-for="(item, index) in visiblePages"
				:key="index"
			>
				<li
					v-if="item === '...'"
					class="page-item disabled"
				>
					<span class="page-link">&hellip;</span>
				</li>
				<li
					v-else
					:class="['page-item', { active: page === item }]"
				>
					<button
						class="page-link"
						@click="$emit('change', item)"
					>
						{{ item }}
					</button>
				</li>
			</template>

			<!-- Next Button -->
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
	import { computed } from "vue";

	const props = defineProps({
		page: { type: Number, required: true },
		pages: { type: Number, required: true },
		delta: { type: Number, default: 2 }, // Number of pages to show to left & right
	});

	defineEmits(["change"]);

	const visiblePages = computed(() => {
		const { page, pages, delta } = props;
		const range = [];
		const result = [];
		let last;

		// 1. Calculate which page numbers to include
		for (let i = 1; i <= pages; i++) {
			if (
				i === 1 ||
				i === pages ||
				(i >= page - delta && i <= page + delta)
			) {
				range.push(i);
			}
		}

		// 2. Insert '...' where gaps exist between numbers
		for (const i of range) {
			if (last) {
				if (i - last === 2) {
					result.push(last + 1);
				} else if (i - last !== 1) {
					result.push("...");
				}
			}
			result.push(i);
			last = i;
		}

		return result;
	});
</script>
