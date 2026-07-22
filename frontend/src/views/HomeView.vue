<template>
	<div class="text-center">
		<h6 style="color: darkgrey">Welcome to</h6>
		<h3>Warranty App</h3>
		<br /><br />
		<div class="row row-cols-1 row-cols-md-3 g-4">
			<BaseCard
				tag="router-link"
				to="/items"
				icon="🛡️"
				title="Warranties"
				text="Show all your warranties."
				:footerText="`${warrantyLabel(stats.items_count)} in the database`"
			/>

			<BaseCard
				tag="router-link"
				to="/shops"
				icon="🏪"
				title="Shops"
				text="Show all your shops."
				:footerText="`${shopLabel(stats.shops_count)} in the database`"
			/>

			<BaseCard
				tag="router-link"
				to="/database"
				icon="💾"
				title="Database"
				text="Manage your database."
				footerText="3 actions available"
			/>
		</div>
	</div>
</template>

<script setup>
	import { onMounted, ref } from "vue";
	import { getStats } from "../api/client";
	import BaseCard from "../components/base/BaseCard.vue";

	const stats = ref({ items_count: 0, shops_count: 0 });

	onMounted(async () => {
		stats.value = await getStats();
	});

	function warrantyLabel(count) {
		if (count === 0) return "No warranties";
		if (count === 1) return "1 warranty";
		return `${count} warranties`;
	}

	function shopLabel(count) {
		if (count === 0) return "No shops";
		if (count === 1) return "1 shop";
		return `${count} shops`;
	}
</script>
