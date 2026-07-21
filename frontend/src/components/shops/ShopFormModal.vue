<template>
	<div
		class="modal fade"
		:id="modalId"
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
					v-if="shop"
					class="modal-body"
				>
					<h5>{{ shop.name }}</h5>
					<table class="table table-striped table-hover">
						<tbody>
							<tr>
								<td>Street</td>
								<td>{{ shop.street }}</td>
							</tr>
							<tr>
								<td>City</td>
								<td>{{ shop.city }}</td>
							</tr>
							<tr>
								<td>Zip code</td>
								<td>{{ shop.zip_code }}</td>
							</tr>
							<tr>
								<td>Linked warranties</td>
								<td>{{ shop.items_count }}</td>
							</tr>
						</tbody>
					</table>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	defineProps({
		modalId: { type: String, required: true },
		shop: { type: Object, default: null },
	});
</script>
