<template>
	<app-navbar />
	<div class="container text-center container-pages">
		<router-view />
	</div>
	<footer class="text-center text-small p-1 fixed-bottom bg-light">
		Warranty App, v2.0 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Powered by Vue +
		FastAPI &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Copyright © 2026
		<router-link to="/about">Tomáš Mühr</router-link>
	</footer>
</template>

<script setup>
	import AppNavbar from "./components/AppNavbar.vue";
</script>
