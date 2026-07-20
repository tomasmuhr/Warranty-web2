<template>
	<div class="text-center">
		<h6 style="color: darkgrey">Welcome to</h6>
		<h3>Warranty App</h3>
		<br /><br />
		<div class="row row-cols-1 row-cols-md-3 g-4">
			<div class="col">
				<div class="card h-100">
					<RouterLink
						to="/items"
						class="card-link"
					>
						<div class="card-body pt-4">
							<div class="card-icon">🛡️</div>
							<h5 class="card-title mt-3">Warranties</h5>
							<p class="card-text">Show all your warranties.</p>
						</div>
						<div class="card-footer">
							<small class="text-muted"
								>{{ warrantyLabel(stats.items_count) }} in the
								database</small
							>
						</div>
					</RouterLink>
				</div>
			</div>
			<div class="col">
				<div class="card h-100">
					<RouterLink
						to="/shops"
						class="card-link"
					>
						<div class="card-body pt-4">
							<div class="card-icon">🏪</div>
							<h5 class="card-title mt-3">Shops</h5>
							<p class="card-text">Show all your shops.</p>
						</div>
						<div class="card-footer">
							<small class="text-muted"
								>{{ shopLabel(stats.shops_count) }} in the
								database</small
							>
						</div>
					</RouterLink>
				</div>
			</div>
			<div class="col">
				<div class="card h-100">
					<RouterLink
						to="/database"
						class="card-link"
					>
						<div class="card-body pt-4">
							<div class="card-icon">💾</div>
							<h5 class="card-title mt-3">Database</h5>
							<p class="card-text">Manage your database.</p>
						</div>
						<div class="card-footer">
							<small class="text-muted"
								>3 actions available</small
							>
						</div>
					</RouterLink>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { onMounted, ref } from "vue";
	import { getStats } from "../api/client";

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
