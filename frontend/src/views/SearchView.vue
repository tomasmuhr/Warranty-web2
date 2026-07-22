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
				<tr
					v-for="item in results.items"
					:key="item.id"
				>
					<td>{{ item.id }}</td>
					<td>{{ item.name }}</td>
					<td>{{ item.shop_name }}</td>
					<td>{{ item.receipt_nr }}</td>
					<td>{{ item.amount }}</td>
					<td>{{ item.price_per_piece }}</td>
					<td>{{ item.comment }}</td>
					<td>{{ item.purchase_date }}</td>
					<td>{{ item.warranty_months }}</td>
					<td>{{ item.expiration_date }}</td>
					<td>
						<button
							type="button"
							class="btn btn-primary btn-sm"
							data-bs-toggle="modal"
							:data-bs-target="`#searchItemEdit_${item.id}`"
						>
							Edit
						</button>
						<confirm-delete-button @confirm="removeItem(item.id)">
							Are you sure you want to delete this record?<br /><b
								>{{ item.name }}</b
							>
						</confirm-delete-button>
					</td>
				</tr>
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
							:data-bs-target="`#searchShopEdit_${shop.id}`"
						>
							Edit
						</button>
						<button
							type="button"
							class="btn btn-danger btn-sm"
							data-bs-toggle="modal"
							:data-bs-target="`#searchShopDelete_${shop.id}`"
						>
							Delete
						</button>
					</td>
				</tr>
			</tbody>
		</table>
	</div>
	<h6 v-else>Nothing found in shops.</h6>

	<template
		v-for="item in results.items"
		:key="`search-item-${item.id}`"
	>
		<div
			class="modal fade"
			:id="`searchItemEdit_${item.id}`"
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
					<form @submit.prevent="submitItemEdit(item.id)">
						<div class="modal-body text-start">
							<div class="mb-2">
								<label class="form-label">Name*</label>
								<input
									v-model="editItemForms[item.id].name"
									class="form-control form-control-sm"
									required
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Shop</label>
								<select
									v-model="editItemForms[item.id].shop_id"
									class="form-select form-select-sm"
								>
									<option value="">—</option>
									<option
										v-for="shop in shopSelectOptions"
										:key="`search-${item.id}-${shop.id}`"
										:value="shop.id"
									>
										{{ shop.name }}
									</option>
								</select>
							</div>
							<div class="mb-2">
								<label class="form-label">Receipt nr</label>
								<input
									v-model="editItemForms[item.id].receipt_nr"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Amount</label>
								<input
									v-model="editItemForms[item.id].amount"
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
									v-model="
										editItemForms[item.id].price_per_piece
									"
									type="number"
									step="0.01"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Comment</label>
								<input
									v-model="editItemForms[item.id].comment"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Purchase date*</label>
								<input
									v-model="
										editItemForms[item.id].purchase_date
									"
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
									v-model="
										editItemForms[item.id].warranty_months
									"
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

	<template
		v-for="shop in results.shops"
		:key="`search-shop-${shop.id}`"
	>
		<div
			class="modal fade"
			:id="`searchShopEdit_${shop.id}`"
			tabindex="-1"
			aria-hidden="true"
		>
			<div class="modal-dialog modal-md">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">Record Update</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<form @submit.prevent="submitShopEdit(shop.id)">
						<div class="modal-body text-start">
							<div class="mb-2">
								<label class="form-label">Name*</label>
								<input
									v-model="editShopForms[shop.id].name"
									class="form-control form-control-sm"
									required
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Street</label>
								<input
									v-model="editShopForms[shop.id].street"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">City</label>
								<input
									v-model="editShopForms[shop.id].city"
									class="form-control form-control-sm"
								/>
							</div>
							<div class="mb-2">
								<label class="form-label">Zip code</label>
								<input
									v-model="editShopForms[shop.id].zip_code"
									class="form-control form-control-sm"
								/>
							</div>
							<button
								type="submit"
								class="btn btn-sm btn-primary"
							>
								Update Record
							</button>
						</div>
					</form>
				</div>
			</div>
		</div>

		<div
			class="modal fade"
			:id="`searchShopDelete_${shop.id}`"
			tabindex="-1"
			aria-hidden="true"
		>
			<div class="modal-dialog modal-sm">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title">Confirm Deletion</h5>
						<button
							type="button"
							class="btn-close"
							data-bs-dismiss="modal"
							aria-label="Close"
						></button>
					</div>
					<div class="modal-body">
						Are you sure you want to delete this record?<br /><b>{{
							shop.name
						}}</b>
						<br /><br />
						<button
							class="btn btn-sm btn-primary"
							data-bs-dismiss="modal"
							@click="removeShop(shop.id, false)"
						>
							Delete record
						</button>
						<br /><br />
						<button
							class="btn btn-sm btn-primary"
							data-bs-dismiss="modal"
							@click="removeShop(shop.id, true)"
						>
							Delete record + linked warranties
						</button>
					</div>
				</div>
			</div>
		</div>
	</template>
</template>

<script setup>
	import { computed, onMounted, reactive, ref, watch } from "vue";
	import { useRoute } from "vue-router";
	import BaseMessage from "../components/base/BaseMessage.vue";
	import ConfirmDeleteButton from "../components/ConfirmDeleteButton.vue";
	import {
		deleteItem,
		deleteShop,
		getShopChoices,
		searchItemsAndShops,
		updateItem,
		updateShop,
	} from "../api/client";

	const route = useRoute();
	const query = computed(() => String(route.query.q || ""));
	const results = ref({ items: [], shops: [] });
	const shopChoices = ref([]);
	const editItemForms = ref({});
	const editShopForms = ref({});
	const alert = reactive({ message: "", type: "success" });

	const shopSelectOptions = computed(() => shopChoices.value);

	function showAlert(message, type = "success") {
		alert.message = message;
		alert.type = type;
	}

	function buildItemPayload(form) {
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

	async function loadResults() {
		if (!query.value.trim()) return;
		results.value = await searchItemsAndShops(query.value.trim());
		editItemForms.value = Object.fromEntries(
			results.value.items.map((item) => [
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
		editShopForms.value = Object.fromEntries(
			results.value.shops.map((shop) => [
				shop.id,
				{
					name: shop.name,
					street: shop.street,
					city: shop.city,
					zip_code: shop.zip_code,
				},
			]),
		);
	}

	onMounted(async () => {
		shopChoices.value = await getShopChoices();
		await loadResults();
	});

	watch(query, loadResults);

	async function submitItemEdit(itemId) {
		try {
			await updateItem(
				itemId,
				buildItemPayload(editItemForms.value[itemId]),
			);
			showAlert("The record has been successfully edited.");
			await loadResults();
		} catch (error) {
			showAlert(
				error.response?.data?.detail || "Failed to update item.",
				"danger",
			);
		}
	}

	async function submitShopEdit(shopId) {
		try {
			await updateShop(shopId, editShopForms.value[shopId]);
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

	async function removeShop(shopId, linkedItems = false) {
		await deleteShop(shopId, linkedItems);
		showAlert("The record has been successfully deleted.");
		await loadResults();
	}
</script>
