<template>
	<BaseMessage
		:message="alert.message"
		:type="alert.type"
		@close="alert.message = ''"
	/>

	<div class="text-center">
		<button
			type="button"
			class="btn btn-sm btn-primary"
			data-bs-toggle="modal"
			data-bs-target="#itemFormModal"
			@click="targetItem = null"
		>
			Add new item
		</button>
	</div>

	<hr />

	<table class="table table-sm table-striped table-hover table-responsive">
		<thead>
			<tr>
				<sortable-th
					@sort="toggleSort('id')"
					:active="sortBy === 'id'"
					:direction="sortDir"
				>
					#
				</sortable-th>
				<sortable-th
					@sort="toggleSort('name')"
					:active="sortBy === 'name'"
					:direction="sortDir"
				>
					Item Name
				</sortable-th>
				<sortable-th
					@sort="toggleSort('shop_name')"
					:active="sortBy === 'shop_name'"
					:direction="sortDir"
				>
					Shop
				</sortable-th>
				<sortable-th
					@sort="toggleSort('receipt_nr')"
					:active="sortBy === 'receipt_nr'"
					:direction="sortDir"
				>
					Receipt nr
				</sortable-th>
				<sortable-th
					@sort="toggleSort('amount')"
					:active="sortBy === 'amount'"
					:direction="sortDir"
				>
					Amount
				</sortable-th>
				<sortable-th
					@sort="toggleSort('price_per_piece')"
					:active="sortBy === 'price_per_piece'"
					:direction="sortDir"
				>
					Price
				</sortable-th>
				<sortable-th
					@sort="toggleSort('comment')"
					:active="sortBy === 'comment'"
					:direction="sortDir"
				>
					Comment
				</sortable-th>
				<sortable-th
					@sort="toggleSort('purchase_date')"
					:active="sortBy === 'purchase_date'"
					:direction="sortDir"
				>
					Purchase Date
				</sortable-th>
				<sortable-th
					@sort="toggleSort('warranty_months')"
					:active="sortBy === 'warranty_months'"
					:direction="sortDir"
				>
					W. Length
				</sortable-th>
				<sortable-th
					@sort="toggleSort('expiration_date')"
					:active="sortBy === 'expiration_date'"
					:direction="sortDir"
				>
					W. Expiration
				</sortable-th>
				<th>Actions</th>
			</tr>
		</thead>
		<tbody>
			<ItemRow
				v-for="item in items"
				:key="item.id"
				:item="item"
				@edit="targetItem = item"
				@open-shop="openShopDetails"
				@delete="removeItem"
			></ItemRow>
		</tbody>
	</table>

	<PaginationBar
		:page="page"
		:pages="pages"
		@change="loadItems"
	/>

	<!-- Extracted Single Form Modal -->
	<ItemForm
		:item="targetItem"
		:shops="shopChoices"
		@save="handleSaveItem"
	/>

	<ShopItems
		:shop="targetShop"
		:items-data="warrantyItems[targetShop?.id]"
	/>
</template>

<script setup>
	import { onMounted, reactive, ref } from "vue";
	import BaseMessage from "../components/base/BaseMessage.vue";
	import PaginationBar from "../components/layout/PaginationBar.vue";
	import ItemForm from "../components/items/ItemForm.vue";
	import ItemRow from "../components/items/ItemRow.vue";
	import ShopItems from "../components/shops/ShopItems.vue";
	import SortableTh from "../components/utils/SortableTh.vue";
	import {
		createItem,
		deleteItem,
		getItems,
		getShop,
		getShopChoices,
		getShopWarrantyItems,
		updateItem,
	} from "../api/client.js";

	const items = ref([]);
	const shopChoices = ref([]);
	const page = ref(1);
	const pages = ref(1);
	const alert = reactive({ message: "", type: "success" });

	const targetItem = ref(null);
	const targetShop = ref(null);
	const warrantyItems = ref({});
	const sortBy = ref("id");
	const sortDir = ref("asc");

	function showAlert(message, type = "success") {
		alert.message = message;
		alert.type = type;
	}

	function toggleSort(column) {
		if (sortBy.value === column) {
			sortDir.value = sortDir.value === "desc" ? "asc" : "desc";
		} else {
			sortBy.value = column;
			sortDir.value = "asc";
		}
		loadItems(1);
	}

	async function loadItems(targetPage = page.value) {
		const data = await getItems(targetPage, sortBy.value, sortDir.value);
		items.value = data.items;
		page.value = data.page;
		pages.value = data.pages;
	}

	async function loadSupportData() {
		shopChoices.value = await getShopChoices();
	}

	onMounted(async () => {
		await Promise.all([loadItems(), loadSupportData()]);
	});

	async function handleSaveItem({ id, data }) {
		try {
			if (id) {
				await updateItem(id, data);
				showAlert("The record has been successfully edited.");
			} else {
				await createItem(data);
				showAlert("The record has been successfully added.");
			}
			await Promise.all([loadItems(), loadSupportData()]);
		} catch (error) {
			showAlert(
				error.response?.data?.detail || "Operation failed.",
				"danger",
			);
		}
	}

	async function removeItem(itemId) {
		await deleteItem(itemId);
		showAlert("The record has been successfully deleted.");
		await Promise.all([loadItems(), loadSupportData()]);
	}

	async function openShopDetails(shopId) {
		const item = items.value.find((i) => i.shop_id === shopId);
		targetShop.value = item
			? { id: shopId, name: item.shop_name }
			: { id: shopId };

		if (!warrantyItems.value[shopId]) {
			warrantyItems.value[shopId] = await getShopWarrantyItems(shopId);
		}

		targetShop.value = await getShop(shopId);
	}
</script>
