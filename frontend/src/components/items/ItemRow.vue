<template>
	<tr>
		<td>{{ item.id }}</td>
		<td>{{ item.name }}</td>
		<td>
			<button
				v-if="item.shop_name"
				type="button"
				class="btn btn-outline-primary btn-sm"
				data-bs-toggle="modal"
				:data-bs-target="`#shopView_${item.id}`"
				@click="$emit('open-shop', item.shop_id)"
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

			<confirm-delete-button @confirm="$emit('delete', item.id)">
				Are you sure you want to delete this record?<br /><b>{{
					item.name
				}}</b>
			</confirm-delete-button>
		</td>
	</tr>
	<div
		v-for="item in items"
		:key="`modals-${item.id}`"
	>
		<shop-form-modal
			v-if="item.shop_id"
			:modal-id="`shopView_${item.id}`"
			:shop="shopDetails[item.shop_id]"
		/>

		<item-form
			:modal-id="`itemEdit_${item.id}`"
			title="Record update"
			submit-text="Update record"
			:shops="shopSelectOptions"
			:initial-data="editForms[item.id]"
			@submit="(payload) => submitEdit(item.id, payload)"
		/>
	</div>
</template>

<script setup>
	import { ref } from "vue";
	import ConfirmDeleteButton from "../ConfirmDeleteButton.vue";
	import ItemForm from "./ItemForm.vue";
	import ShopFormModal from "../shops/ShopForm.vue";

	defineProps({
		item: { type: Object, required: true },
	});

	defineEmits(["delete", "open-shop"]);
</script>
