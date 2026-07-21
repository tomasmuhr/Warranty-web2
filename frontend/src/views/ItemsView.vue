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
			data-bs-target="#itemAdd"
		>
			Add new item
		</button>

		<!-- Re-added the Add Item Modal component -->
		<item-details-modal
			modal-id="itemAdd"
			title="Item details"
			submit-text="Add item"
			:shops="shopSelectOptions"
			:initial-data="addForm"
			:is-add="true"
			@submit="submitAdd"
		/>
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
			<item-row
				v-for="item in items"
				:key="item.id"
				:item="item"
				@open-shop="openShopDetails"
				@delete="removeItem"
			></item-row>
		</tbody>
	</table>

	<pagination-bar
		:page="page"
		:pages="pages"
		@change="loadItems"
	/>
</template>

<script setup>
	import { computed, onMounted, reactive, ref } from "vue";
	import AlertMessage from "../components/AlertMessage.vue";
	// import ConfirmDeleteButton from "../components/ConfirmDeleteButton.vue";
	import PaginationBar from "../components/PaginationBar.vue";
	// import ItemDetailsModal from "../components/items/ItemDetailsModal.vue";
	// import ShopDetailsModal from "../components/shops/ShopDetailsModal.vue";
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
	const shopDetails = ref({});

	const addForm = reactive({
		name: "",
		shop_id: "",
		receipt_nr: "",
		amount: "",
		price_per_piece: "",
		comment: "",
		purchase_date: new Date().toISOString().slice(0, 10),
		warranty_months: 12,
	});

	const editForms = ref({});

	const shopSelectOptions = computed(() => shopChoices.value);

	function showAlert(message, type = "success") {
		alert.message = message;
		alert.type = type;
	}

	function emptyAddForm() {
		addForm.name = "";
		addForm.shop_id = "";
		addForm.receipt_nr = "";
		addForm.amount = "";
		addForm.price_per_piece = "";
		addForm.comment = "";
		addForm.purchase_date = new Date().toISOString().slice(0, 10);
		addForm.warranty_months = 12;
	}

	function buildPayload(form) {
		return {
			name: form.name,
			shop_id: form.shop_id ? Number(form.shop_id) : null,
			receipt_nr: form.receipt_nr,
			amount: form.amount === "" ? null : Number(form.amount),
			price_per_piece:
				form.price_per_piece === ""
					? null
					: Number(form.price_per_piece),
			comment: form.comment,
			purchase_date: form.purchase_date,
			warranty_months: Number(form.warranty_months),
		};
	}

	async function loadItems(targetPage = page.value) {
		const data = await getItems(targetPage);
		items.value = data.items;
		page.value = data.page;
		pages.value = data.pages;
		editForms.value = Object.fromEntries(
			data.items.map((item) => [
				item.id,
				{
					name: item.name,
					shop_id: item.shop_id ?? "",
					receipt_nr: item.receipt_nr ?? "",
					amount: item.amount ?? "",
					price_per_piece: item.price_per_piece ?? "",
					comment: item.comment ?? "",
					purchase_date: item.purchase_date,
					warranty_months: item.warranty_months,
				},
			]),
		);
	}

	async function loadSupportData() {
		shopChoices.value = await getShopChoices();
	}

	onMounted(async () => {
		await Promise.all([loadItems(), loadSupportData()]);
	});

	async function submitAdd() {
		try {
			await createItem(buildPayload(addForm));
			showAlert("The record has been successfully added.");
			emptyAddForm();
			await Promise.all([loadItems(1), loadSupportData()]);
		} catch (error) {
			showAlert(
				error.response?.data?.detail || "Failed to add item.",
				"danger",
			);
		}
	}

	async function submitEdit(itemId) {
		try {
			await updateItem(itemId, buildPayload(editForms.value[itemId]));
			showAlert("The record has been successfully edited.");
			await loadItems();
		} catch (error) {
			showAlert(
				error.response?.data?.detail || "Failed to update item.",
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
