<template>
	<div>
		<h6>Under warranty</h6>
		<span v-if="!underWarranty.length">None.</span>
		<table
			v-else
			class="table table-striped table-hover"
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
					v-for="(row, index) in underWarranty"
					:key="`under-${index}`"
				>
					<td>{{ row.name }}</td>
					<td>{{ row.purchase_date }}</td>
					<td>{{ row.expiration_date }}</td>
				</tr>
			</tbody>
		</table>

		<br /><br />

		<h6>Out of warranty</h6>
		<span v-if="!outOfWarranty.length">None.</span>
		<table
			v-else
			class="table table-striped table-hover"
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
					v-for="(row, index) in outOfWarranty"
					:key="`out-${index}`"
				>
					<td>{{ row.name }}</td>
					<td>{{ row.purchase_date }}</td>
					<td>{{ row.expiration_date }}</td>
				</tr>
			</tbody>
		</table>
	</div>
</template>

<script setup>
	defineProps({
		underWarranty: { type: Array, default: () => [] },
		outOfWarranty: { type: Array, default: () => [] },
	});
</script>
