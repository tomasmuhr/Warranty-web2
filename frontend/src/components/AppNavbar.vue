<script setup>
	import { computed, ref } from "vue";
	import { useRoute, useRouter } from "vue-router";

	const route = useRoute();
	const router = useRouter();
	const query = ref(route.query.q || "");

	const navClass = (name) =>
		route.name === name ? "nav-link highlighted" : "nav-link";

	async function submitSearch() {
		const trimmed = query.value.trim();
		if (!trimmed) return;
		await router.push({ name: "search", query: { q: trimmed } });
	}
</script>

<template>
	<nav class="navbar navbar-light navbar-expand-md shadow fixed-top">
		<div class="container">
			<RouterLink
				class="navbar-brand"
				to="/"
				><b>Warranty App</b></RouterLink
			>
			<button
				class="navbar-toggler"
				type="button"
				data-bs-toggle="collapse"
				data-bs-target="#navbarNav"
				aria-controls="navbarNav"
				aria-expanded="false"
				aria-label="Toggle navigation"
			>
				<span class="navbar-toggler-icon"></span>
			</button>
			<div
				class="collapse navbar-collapse"
				id="navbarNav"
			>
				<div class="navbar-nav">
					<RouterLink
						:class="navClass('items')"
						to="/items"
						>Items</RouterLink
					>
					<RouterLink
						:class="navClass('shops')"
						to="/shops"
						>Shops</RouterLink
					>
					<RouterLink
						:class="navClass('database')"
						to="/database"
						>Database</RouterLink
					>
					<RouterLink
						:class="navClass('about')"
						to="/about"
						>About</RouterLink
					>
				</div>
			</div>
			<form
				class="d-flex"
				@submit.prevent="submitSearch"
			>
				<input
					v-model="query"
					class="form-control form-control-sm me-2"
					name="query"
					type="search"
					placeholder="Search"
					aria-label="Search"
					required
				/>
				<button
					class="btn btn-sm btn-outline-success"
					type="submit"
				>
					Search
				</button>
			</form>
		</div>
	</nav>
</template>
