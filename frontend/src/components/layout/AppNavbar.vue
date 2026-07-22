<template>
	<nav class="navbar navbar-light navbar-expand-md shadow fixed-top">
		<div class="container">
			<router-link
				class="navbar-brand"
				to="/"
				><b>Warranty App</b></router-link
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
					<router-link
						:class="navClass('items')"
						to="/items"
						>Items</router-link
					>
					<router-link
						:class="navClass('shops')"
						to="/shops"
						>Shops</router-link
					>
					<router-link
						:class="navClass('database')"
						to="/database"
						>Database</router-link
					>
					<router-link
						:class="navClass('about')"
						to="/about"
						>About</router-link
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
