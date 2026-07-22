<template>
	<tr>
		<td>{{ item.id }}</td>
		<td>{{ item.name }}</td>
		<td>
			<button
				v-if="item.shop_name"
				type="button"
				class="btn btn-outline-primary btn-sm"
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
				data-bs-target="#itemFormModal"
				@click="$emit('edit', item)"
			>
				Edit
			</button>

			<ConfirmDeleteButton @confirm="$emit('delete', item.id)">
				Are you sure you want to delete this record?<br /><b>{{
					item.name
				}}</b>
			</ConfirmDeleteButton>
		</td>
	</tr>
</template>

<script setup>
	import ConfirmDeleteButton from "../utils/ConfirmDeleteButton.vue";

	defineProps({
		item: { type: Object, required: true },
	});

	defineEmits(["delete", "open-shop", "edit"]);
</script>
