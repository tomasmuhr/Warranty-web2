<template>
	<BaseMessage
		:message="alert.message"
		:type="alert.type"
		@close="alert.message = ''"
	/>

	<div class="text-center">
		<h3>Search Results for '{{ query }}'</h3>
		<br /><br />
	</div>

	<div>
		<h4>Items</h4>
	</div>
	<div
		v-if="results.items.length"
		class="table-responsive"
	>
		<table class="table table-sm table-striped table-hover">
			<thead>
				<tr>
					<th>#</th>
					<th>Name</th>
					<th>Shop</th>
					<th>Receipt nr</th>
					<th>Amount</th>
					<th>Price</th>
					<th>Comment</th>
					<th>Purchase Date</th>
					<th>W. Length</th>
					<th>W. Expiration</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				<ItemRow
					v-for="item in results.items"
					:key="item.id"
					:item="item"
					@edit="targetItem = item"
					@open-shop="openShopDetails"
					@delete="removeItem"
				/>
			</tbody>
		</table>
	</div>
	<h6 v-else>Nothing found in items.</h6>

	<hr />

	<div>
		<h4>Shops</h4>
	</div>
	<div
		v-if="results.shops.length"
		class="table-responsive"
	>
		<table class="table table-sm table-striped table-hover">
			<thead>
				<tr>
					<th>#</th>
					<th>Name</th>
					<th>Street</th>
					<th>City</th>
					<th>Zip code</th>
					<th>Records</th>
					<th>Actions</th>
				</tr>
			</thead>
			<tbody>
				<tr
					v-for="shop in results.shops"
					:key="shop.id"
				>
					<td>{{ shop.id }}</td>
					<td>{{ shop.name }}</td>
					<td>{{ shop.street }}</td>
					<td>{{ shop.city }}</td>
					<td>{{ shop.zip_code }}</td>
					<td>{{ shop.items_count || 0 }}</td>
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
	</div>
	<h6 v-else>Nothing found in shops.</h6>

	<ItemForm
		:item="targetItem"
		:shops="shopChoices"
		@save="handleSaveItem"
	/>
	<ShopForm
		:shop="targetShop"
		@save="handleSaveShop"
	/>
	<ShopDelete
		:shop="targetShop"
		@confirm="handleDeleteShop"
	/>
	<ShopItems
		:shop="targetShop"
		:items-data="warrantyItems[targetShop?.id]"
	/>
</template>

<script setup>
	import { computed, onMounted, ref, watch } from "vue";
	import { useRoute } from "vue-router";
	import BaseMessage from "../components/base/BaseMessage.vue";
	import ItemForm from "../components/items/ItemForm.vue";
	import ItemRow from "../components/items/ItemRow.vue";
	import ShopDelete from "../components/shops/ShopDelete.vue";
	import ShopForm from "../components/shops/ShopForm.vue";
	import ShopItems from "../components/shops/ShopItems.vue";
	import { useAlert } from "../composables/useAlert";
	import {
		deleteItem,
		deleteShop,
		getShop,
		getShopChoices,
		getShopWarrantyItems,
		searchItemsAndShops,
		updateItem,
		updateShop,
	} from "../api/client";

	const route = useRoute();
	const query = computed(() => String(route.query.q || ""));
	const results = ref({ items: [], shops: [] });
	const shopChoices = ref([]);
	const targetItem = ref(null);
	const targetShop = ref(null);
	const warrantyItems = ref({});
	const { alert, showAlert } = useAlert();

	async function loadResults() {
		if (!query.value.trim()) return;
		results.value = await searchItemsAndShops(query.value.trim());
	}

	onMounted(async () => {
		shopChoices.value = await getShopChoices();
		await loadResults();
	});

	watch(query, loadResults);

	async function handleSaveItem({ id, data }) {
		try {
			await updateItem(id, data);
			showAlert("The record has been successfully edited.");
			await loadResults();
		} catch (error) {
			showAlert(
				error.response?.data?.detail || "Failed to update item.",
				"danger",
			);
		}
	}

	async function handleSaveShop({ id, data }) {
		try {
			await updateShop(id, data);
			showAlert("The record has been successfully updated.");
			await loadResults();
		} catch (error) {
			showAlert(
				error.response?.data?.detail || "Failed to update shop.",
				"danger",
			);
		}
	}

	async function removeItem(itemId) {
		await deleteItem(itemId);
		showAlert("The record has been successfully deleted.");
		await loadResults();
	}

	async function handleDeleteShop({ id, linkedItems }) {
		try {
			await deleteShop(id, linkedItems);
			showAlert("The record has been successfully deleted.");
			await loadResults();
		} catch (error) {
			showAlert("Failed to delete shop.", "danger");
		}
	}

	async function openShopDetails(shopId) {
		const item = results.value.items.find((i) => i.shop_id === shopId);
		targetShop.value = item
			? { id: shopId, name: item.shop_name }
			: { id: shopId };

		if (!warrantyItems.value[shopId]) {
			warrantyItems.value[shopId] = await getShopWarrantyItems(shopId);
		}

		targetShop.value = await getShop(shopId);
	}
</script>
