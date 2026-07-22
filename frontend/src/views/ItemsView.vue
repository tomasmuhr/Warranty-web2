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
				<th>#</th>
				<th>Item Name</th>
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
</template>

<script setup>
	import { onMounted, reactive, ref } from "vue";
	import BaseMessage from "../components/base/BaseMessage.vue";
	import PaginationBar from "../components/layout/PaginationBar.vue";
	import ItemForm from "../components/items/ItemForm.vue";
	import ItemRow from "../components/items/ItemRow.vue";
	import {
		createItem,
		deleteItem,
		getItems,
		getShop,
		getShopChoices,
		updateItem,
	} from "../api/client.js";

	const items = ref([]);
	const shopChoices = ref([]);
	const page = ref(1);
	const pages = ref(1);
	const alert = reactive({ message: "", type: "success" });

	const targetItem = ref(null);
	const shopDetails = ref({});

	function showAlert(message, type = "success") {
		alert.message = message;
		alert.type = type;
	}

	async function loadItems(targetPage = page.value) {
		const data = await getItems(targetPage);
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
		shopDetails.value[shopId] = await getShop(shopId);
	}
</script>
