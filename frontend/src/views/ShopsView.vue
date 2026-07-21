<template><alert-message :message="alert.message" :type="alert.type" @close="alert.message = ''" />

<div class="text-center">
	<button type="button" class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#addShop">
		Add new shop
	</button>

	<div class="modal fade" id="addShop" tabindex="-1" aria-hidden="true">
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Shop details</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<form @submit.prevent="submitAdd">
					<div class="modal-body text-start">
						<div class="mb-2">
							<label class="form-label">Name*</label>
							<input v-model="addForm.name" class="form-control form-control-sm" required />
						</div>
						<div class="mb-2">
							<label class="form-label">Street</label>
							<input v-model="addForm.street" class="form-control form-control-sm" />
						</div>
						<div class="mb-2">
							<label class="form-label">City</label>
							<input v-model="addForm.city" class="form-control form-control-sm" />
						</div>
						<div class="mb-2">
							<label class="form-label">Zip Code</label>
							<input v-model="addForm.zip_code" class="form-control form-control-sm" />
						</div>
						<button type="submit" class="btn btn-sm btn-primary">
							Add shop
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
			<th>Name</th>
			<th>Street</th>
			<th>City</th>
			<th>Zip code</th>
			<th>Warranties</th>
			<th>Actions</th>
		</tr>
	</thead>
	<tbody>
		<tr v-for="shop in shops" :key="shop.id">
			<td>{{ shop.id }}</td>
			<td>{{ shop.name }}</td>
			<td>{{ shop.street }}</td>
			<td>{{ shop.city }}</td>
			<td>{{ shop.zip_code }}</td>
			<td>
				<button v-if="shop.items_count" type="button" class="btn btn-outline-primary btn-sm" data-bs-toggle="modal"
					:data-bs-target="`#shopItems_${shop.id}`" @click="loadWarrantyItems(shop.id)">
					{{ shop.items_count }}
				</button>
				<span v-else>0</span>
			</td>
			<td>
				<button type="button" class="btn btn-primary btn-sm" data-bs-toggle="modal"
					:data-bs-target="`#shopEdit_${shop.id}`">
					Edit
				</button>
				<button type="button" class="btn btn-danger btn-sm" data-bs-toggle="modal"
					:data-bs-target="`#shopDelete_${shop.id}`">
					Delete
				</button>
			</td>
		</tr>
	</tbody>
</table>

<pagination-bar :page="page" :pages="pages" @change="loadShops" />

<template v-for="shop in shops" :key="`shop-modals-${shop.id}`">
	<div class="modal fade" :id="`shopItems_${shop.id}`" tabindex="-1" aria-hidden="true">
		<div class="modal-dialog modal-md">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">{{ shop.name }}</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<warranty-items-table v-if="warrantyItems[shop.id]" :under-warranty="warrantyItems[shop.id].under_warranty
						" :out-of-warranty="warrantyItems[shop.id].out_of_warranty
								" />
				</div>
			</div>
		</div>
	</div>

	<div class="modal fade" :id="`shopEdit_${shop.id}`" tabindex="-1" aria-hidden="true">
		<div class="modal-dialog modal-md">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Record update</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<form @submit.prevent="submitEdit(shop.id)">
					<div class="modal-body text-start">
						<div class="mb-2">
							<label class="form-label">Name*</label>
							<input v-model="editForms[shop.id].name" class="form-control form-control-sm" required />
						</div>
						<div class="mb-2">
							<label class="form-label">Street</label>
							<input v-model="editForms[shop.id].street" class="form-control form-control-sm" />
						</div>
						<div class="mb-2">
							<label class="form-label">City</label>
							<input v-model="editForms[shop.id].city" class="form-control form-control-sm" />
						</div>
						<div class="mb-2">
							<label class="form-label">Zip code</label>
							<input v-model="editForms[shop.id].zip_code" class="form-control form-control-sm" />
						</div>
						<button type="submit" class="btn btn-sm btn-primary">
							Update record
						</button>
					</div>
				</form>
			</div>
		</div>
	</div>

	<div class="modal fade" :id="`shopDelete_${shop.id}`" tabindex="-1" aria-hidden="true">
		<div class="modal-dialog modal-sm">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">Confirm Deletion</h5>
					<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
				</div>
				<div class="modal-body">
					Are you sure you want to delete this record?<br /><b>{{
						shop.name
					}}</b>
					<br /><br />
					<button class="btn btn-sm btn-primary" data-bs-dismiss="modal" @click="removeShop(shop.id, false)">
						Delete record
					</button>
					<br /><br />
					<button class="btn btn-sm btn-primary" data-bs-dismiss="modal" @click="removeShop(shop.id, true)">
						Delete record + linked warranties
					</button>
				</div>
			</div>
		</div>
	</div>
</template>
</template>

<script setup>
import { onMounted, reactive, ref } from "vue";
import AlertMessage from "../components/AlertMessage.vue";
import PaginationBar from "../components/PaginationBar.vue";
import WarrantyItemsTable from "../components/WarrantyItemsTable.vue";
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
const warrantyItems = ref({});

const addForm = reactive({ name: "", street: "", city: "", zip_code: "" });
const editForms = ref({});

function showAlert(message, type = "success") {
	alert.message = message;
	alert.type = type;
}

async function loadShops(targetPage = page.value) {
	const data = await getShops(targetPage);
	shops.value = data.items;
	page.value = data.page;
	pages.value = data.pages;
	editForms.value = Object.fromEntries(
		data.items.map((shop) => [
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

onMounted(loadShops);

async function submitAdd() {
	try {
		await createShop(addForm);
		showAlert("The record has been successfully added!");
		Object.assign(addForm, {
			name: "",
			street: "",
			city: "",
			zip_code: "",
		});
		await loadShops(1);
	} catch (error) {
		showAlert(
			error.response?.data?.detail || "Failed to add shop.",
			"danger",
		);
	}
}

async function submitEdit(shopId) {
	try {
		await updateShop(shopId, editForms.value[shopId]);
		showAlert("The record has been successfully updated.");
		await loadShops();
	} catch (error) {
		showAlert(
			error.response?.data?.detail || "Failed to update shop.",
			"danger",
		);
	}
}

async function removeShop(shopId, linkedItems = false) {
	await deleteShop(shopId, linkedItems);
	showAlert(
		linkedItems
			? "The record and linked items have been successfully deleted."
			: "The record has been successfully deleted.",
	);
	await loadShops();
}

async function loadWarrantyItems(shopId) {
	warrantyItems.value[shopId] = await getShopWarrantyItems(shopId);
}
</script>
