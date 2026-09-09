<template>
	<BaseModal
		id="shopItemsModal"
		size="md"
	>
		<template #title>
			<span v-if="shop">{{ shop.name }}</span>
			<span v-else>Loading...</span>
		</template>

		<template #body>
			<div v-if="itemsData">
				<h6 class="table-success p-2 rounded">Under warranty</h6>
				<span v-if="!itemsData.under_warranty.length">None.</span>
				<table
					v-else
					class="table table-striped table-hover table-sm"
				>
					<thead>
						<tr>
							<th>Name</th>
							<th>Purchase date</th>
							<th>Expiry date</th>
						</tr>
					</thead>
					<tbody>
						<tr
							v-for="(row, index) in itemsData.under_warranty"
							:key="`under-${index}`"
						>
							<td>{{ row.name }}</td>
							<td>{{ row.purchase_date }}</td>
							<td>{{ row.expiration_date }}</td>
						</tr>
					</tbody>
				</table>

				<br /><br />

				<h6 class="table-danger p-2 rounded">Out of warranty</h6>
				<span v-if="!itemsData.out_of_warranty.length">None.</span>
				<table
					v-else
					class="table table-striped table-hover table-sm"
				>
					<thead>
						<tr>
							<th>Name</th>
							<th>Purchase date</th>
							<th>Expiry date</th>
						</tr>
					</thead>
					<tbody>
						<tr
							v-for="(row, index) in itemsData.out_of_warranty"
							:key="`out-${index}`"
						>
							<td>{{ row.name }}</td>
							<td>{{ row.purchase_date }}</td>
							<td>{{ row.expiration_date }}</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div
				v-else
				class="text-center"
			>
				Loading...
			</div>
		</template>
	</BaseModal>
</template>

<script setup>
	import BaseModal from "../base/BaseModal.vue";

	defineProps({
		shop: { type: Object, default: () => null },
		itemsData: { type: Object, default: () => null },
	});
</script>
