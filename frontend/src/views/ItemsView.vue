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

		<div
			class="modal fade"
			id="itemAdd"
			tabindex="-1"
			aria-hidden="true"
		>
			<div class="modal-dialog">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">Item details</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<form @submit.prevent="submitAdd">
						<div class="modal-body text-start">
							<div class="mb-2">
								<label class="form-label">Name*</label>
								<input
									v-model="addForm.name"
									class="form-control form-control-sm"
									required
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Shop</label>
								<select
									v-model="addForm.shop_id"
									class="form-select form-select-sm"
								>
									<option value="">—</option>
									<option
										v-for="shop in shopSelectOptions"
										:key="shop.name"
										:value="shop.id"
									>
										{{ shop.name }}
									</option>
								</select>
							</div>
							<div class="mb-2">
								<label class="form-label">Receipt Nr</label>
								<input
									v-model="addForm.receipt_nr"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Amount</label>
								<input
									v-model="addForm.amount"
									type="number"
									min="0"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label"
									>Price per piece</label
								>
								<input
									v-model="addForm.price_per_piece"
									type="number"
									step="0.01"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Comment</label>
								<input
									v-model="addForm.comment"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Purchase date*</label>
								<input
									v-model="addForm.purchase_date"
									type="date"
									class="form-control form-control-sm"
									required
								/>
							</div>
							<div class="mb-2">
								<label class="form-label"
									>Warranty length (months)*</label
								>
								<input
									v-model="addForm.warranty_months"
									type="number"
									min="1"
									class="form-control form-control-sm"
									required
								/>
							</div>
							<button
								type="submit"
								class="btn btn-sm btn-primary"
							>
								Add item
							</button>
							<div class="text-danger mt-2">* required field</div>
						</div>
					</form>
				</div>
			</div>
		</div>
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
			<tr
				v-for="item in items"
				:key="item.id"
			>
				<td>{{ item.id }}</td>
				<td>{{ item.name }}</td>
				<td>
					<button
						v-if="item.shop_name"
						type="button"
						class="btn btn-outline-primary btn-sm"
						data-bs-toggle="modal"
						:data-bs-target="`#shopView_${item.id}`"
						@click="openShopDetails(item.shop_id)"
					>
						{{ item.shop_name }}
					</button>
				</td>
				<td>{{ item.receipt_nr }}</td>
				<td>{{ item.amount ?? "" }}</td>
				<td>{{ item.price_per_piece ?? "" }}</td>
				<td>{{ item.comment }}</td>
				<td>{{ item.purchase_date }}</td>
				<td>{{ item.warranty_months }}</td>
				<td>{{ item.expiration_date }}</td>
				<td>
					<button
						type="button"
						class="btn btn-primary btn-sm"
						data-bs-toggle="modal"
						:data-bs-target="`#itemEdit_${item.id}`"
					>
						Edit
					</button>
					<confirm-delete-button @confirm="removeItem(item.id)">
						Are you sure you want to delete this record?<br /><b>{{
							item.name
						}}</b>
					</confirm-delete-button>
				</td>
			</tr>
		</tbody>
	</table>

	<pagination-bar
		:page="page"
		:pages="pages"
		@change="loadItems"
	/>

	<template
		v-for="item in items"
		:key="`modals-${item.id}`"
	>
		<div
			v-if="item.shop_id"
			class="modal fade"
			:id="`shopView_${item.id}`"
			tabindex="-1"
			aria-hidden="true"
		>
			<div class="modal-dialog modal-md">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">Shop details</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<div
						v-if="shopDetails[item.shop_id]"
						class="modal-body"
					>
						<h5>{{ shopDetails[item.shop_id].name }}</h5>
						<table class="table table-striped table-hover">
							<tbody>
								<tr>
									<td>Street</td>
									<td>
										{{ shopDetails[item.shop_id].street }}
									</td>
								</tr>
								<tr>
									<td>City</td>
									<td>
										{{ shopDetails[item.shop_id].city }}
									</td>
								</tr>
								<tr>
									<td>Zip code</td>
									<td>
										{{ shopDetails[item.shop_id].zip_code }}
									</td>
								</tr>
								<tr>
									<td>Linked warranties</td>
									<td>
										{{
											shopDetails[item.shop_id]
												.items_count
										}}
									</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>

		<div
			class="modal fade"
			:id="`itemEdit_${item.id}`"
			tabindex="-1"
			aria-hidden="true"
		>
			<div class="modal-dialog modal-md">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">Record update</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<form @submit.prevent="submitEdit(item.id)">
						<div class="modal-body text-start">
							<div class="mb-2">
								<label class="form-label">Name*</label>
								<input
									v-model="editForms[item.id].name"
									class="form-control form-control-sm"
									required
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Shop</label>
								<select
									v-model="editForms[item.id].shop_id"
									class="form-select form-select-sm"
								>
									<option value="">—</option>
									<option
										v-for="shop in shopSelectOptions"
										:key="`edit-${item.id}-${shop.name}`"
										:value="shop.id"
									>
										{{ shop.name }}
									</option>
								</select>
							</div>
							<div class="mb-2">
								<label class="form-label">Receipt nr</label>
								<input
									v-model="editForms[item.id].receipt_nr"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Amount</label>
								<input
									v-model="editForms[item.id].amount"
									type="number"
									min="0"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label"
									>Price per piece</label
								>
								<input
									v-model="editForms[item.id].price_per_piece"
									type="number"
									step="0.01"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Comment</label>
								<input
									v-model="editForms[item.id].comment"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Purchase date*</label>
								<input
									v-model="editForms[item.id].purchase_date"
									type="date"
									class="form-control form-control-sm"
									required
								/>
							</div>
							<div class="mb-2">
								<label class="form-label"
									>Warranty length (months)*</label
								>
								<input
									v-model="editForms[item.id].warranty_months"
									type="number"
									min="1"
									class="form-control form-control-sm"
									required
								/>
							</div>
							<button
								type="submit"
								class="btn btn-sm btn-primary"
							>
								Update record
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>
	</template>
</template>

<script setup>
	import { computed, onMounted, reactive, ref } from "vue";
	import AlertMessage from "../components/AlertMessage.vue";
	import ConfirmDeleteButton from "../components/ConfirmDeleteButton.vue";
	import PaginationBar from "../components/PaginationBar.vue";
	import {
		createItem,
		deleteItem,
		getItems,
		getShop,
		getShopChoices,
		updateItem,
	} from "../api/client";

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
