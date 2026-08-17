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

	<div class="row g-2 align-items-end justify-content-center mb-3 text-start">
		<div class="col-auto">
			<label
				class="form-label form-label-sm mb-0"
				for="filterStatus"
				>Status</label
			>
			<select
				id="filterStatus"
				v-model="filters.status"
				class="form-select form-select-sm"
				@change="applyFilters"
			>
				<option value="">All</option>
				<option value="active">Active</option>
				<option value="expiring">Expiring soon</option>
				<option value="expired">Expired</option>
			</select>
		</div>
		<div class="col-auto">
			<label
				class="form-label form-label-sm mb-0"
				for="filterShop"
				>Shop</label
			>
			<select
				id="filterShop"
				v-model="filters.shop"
				class="form-select form-select-sm"
				@change="applyFilters"
			>
				<option value="">All shops</option>
				<option value="none">No shop linked</option>
				<option
					v-for="shop in shopChoices"
					:key="shop.id"
					:value="String(shop.id)"
				>
					{{ shop.name }}
				</option>
			</select>
		</div>
		<div class="col-auto">
			<button
				type="button"
				class="btn btn-sm btn-outline-secondary"
				:disabled="!hasActiveFilters"
				@click="clearFilters"
			>
				Clear filters
			</button>
		</div>
	</div>

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
			<tr v-if="!items.length">
				<td
					colspan="11"
					class="text-center text-muted"
				>
					No items match the current filters.
				</td>
			</tr>
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
	import { computed, onMounted, reactive, ref } from "vue";
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
	const filters = reactive({ status: "", shop: "" });

	const hasActiveFilters = computed(
		() => !!filters.status || !!filters.shop,
	);

	function buildFilterParams() {
		return {
			status: filters.status || undefined,
			shopId:
				filters.shop && filters.shop !== "none"
					? Number(filters.shop)
					: undefined,
			noShop: filters.shop === "none",
		};
	}

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

	function applyFilters() {
		loadItems(1);
	}

	function clearFilters() {
		filters.status = "";
		filters.shop = "";
		loadItems(1);
	}

	async function loadItems(targetPage = page.value) {
		const data = await getItems(
			targetPage,
			sortBy.value,
			sortDir.value,
			buildFilterParams(),
		);
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
