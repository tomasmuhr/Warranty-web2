<template>
	<alert-message
		:message="alert.message"
		:type="alert.type"
		@close="alert.message = ''"
	/>

	<div class="text-center">
		<button
			type="button"
			class="btn btn-sm btn-primary"
			data-bs-toggle="modal"
			data-bs-target="#shopFormModal"
			@click="targetShop = null"
		>
			Add new shop
		</button>
	</div>

	<hr />

	<table class="table table-sm table-striped table-hover table-responsive">
		<thead>
			<tr>
				<th>#</th>
				<th>Name</th>
				<th>Street</th>
				<th>City</th>
				<th>Zip code</th>
				<th>Warranties</th>
				<th>Actions</th>
			</tr>
		</thead>
		<tbody>
			<tr
				v-for="shop in shops"
				:key="shop.id"
			>
				<td>{{ shop.id }}</td>
				<td>{{ shop.name }}</td>
				<td>{{ shop.street }}</td>
				<td>{{ shop.city }}</td>
				<td>{{ shop.zip_code }}</td>
				<td>
					<button
						v-if="shop.items_count"
						type="button"
						class="btn btn-outline-primary btn-sm"
						data-bs-toggle="modal"
						data-bs-target="#shopItemsModal"
						@click="openItems(shop)"
					>
						{{ shop.items_count }}
					</button>
					<span v-else>0</span>
				</td>
				<td>
					<button
						type="button"
						class="btn btn-primary btn-sm"
						data-bs-toggle="modal"
						data-bs-target="#shopFormModal"
						@click="targetShop = shop"
					>
						Edit
					</button>
					<button
						type="button"
						class="btn btn-danger btn-sm"
						data-bs-toggle="modal"
						data-bs-target="#shopDeleteModal"
						@click="targetShop = shop"
					>
						Delete
					</button>
				</td>
			</tr>
		</tbody>
	</table>

	<pagination-bar
		:page="page"
		:pages="pages"
		@change="loadShops"
	/>

	<!-- Extracted Modals -->
	<shop-form-modal
		:shop="targetShop"
		@save="handleSaveShop"
	/>
	<shop-delete-modal
		:shop="targetShop"
		@confirm="handleDeleteShop"
	/>
	<shop-items-modal
		:shop="targetShop"
		:items-data="warrantyItems[targetShop?.id]"
	/>
</template>

<script setup>
	import { onMounted, reactive, ref } from "vue";
	import AlertMessage from "../components/AlertMessage.vue";
	import PaginationBar from "../components/PaginationBar.vue";
	import ShopFormModal from "../components/shops/ShopFormModal.vue";
	import ShopDeleteModal from "../components/shops/ShopDeleteModal.vue";
	import ShopItemsModal from "../components/shops/ShopItemsModal.vue";
	import {
		createShop,
		deleteShop,
		getShopWarrantyItems,
		getShops,
		updateShop,
	} from "../api/client";

	const shops = ref([]);
	const page = ref(1);
	const pages = ref(1);
	const alert = reactive({ message: "", type: "success" });

	// Replaces individual form dictionaries
	const targetShop = ref(null);
	const warrantyItems = ref({});

	function showAlert(message, type = "success") {
		alert.message = message;
		alert.type = type;
	}

	async function loadShops(targetPage = page.value) {
		const data = await getShops(targetPage);
		shops.value = data.items;
		page.value = data.page;
		pages.value = data.pages;
	}

	onMounted(loadShops);

	async function handleSaveShop({ id, data }) {
		try {
			if (id) {
				await updateShop(id, data);
				showAlert("The record has been successfully updated.");
			} else {
				await createShop(data);
				showAlert("The record has been successfully added!");
			}
			await loadShops();
		} catch (error) {
			showAlert(
				error.response?.data?.detail || "Operation failed.",
				"danger",
			);
		}
	}

	async function handleDeleteShop({ id, linkedItems }) {
		try {
			await deleteShop(id, linkedItems);
			showAlert(
				linkedItems
					? "Record and linked items deleted."
					: "Record deleted.",
			);
			await loadShops();
		} catch (error) {
			showAlert("Failed to delete shop.", "danger");
		}
	}

	async function openItems(shop) {
		targetShop.value = shop;
		if (!warrantyItems.value[shop.id]) {
			warrantyItems.value[shop.id] = await getShopWarrantyItems(shop.id);
		}
	}
</script>
