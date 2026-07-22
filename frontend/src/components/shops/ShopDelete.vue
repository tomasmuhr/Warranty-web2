<template>
	<!-- Wrap everything in the BaseModal and provide the required ID -->
	<base-modal
		id="shopDeleteModal"
		size="sm"
	>
		<!-- Inject the Title -->
		<template #title> Confirm Deletion </template>

		<!-- Inject the Body -->
		<template #body>
			<div v-if="shop">
				Are you sure you want to delete this record?<br />
				<b>{{ shop.name }}</b>
				<br /><br />

				<button
					class="btn btn-sm btn-primary w-100 mb-2"
					data-bs-dismiss="modal"
					@click="
						$emit('confirm', { id: shop.id, linkedItems: false })
					"
				>
					Delete record
				</button>

				<button
					class="btn btn-sm btn-primary w-100"
					data-bs-dismiss="modal"
					@click="
						$emit('confirm', { id: shop.id, linkedItems: true })
					"
				>
					Delete record + linked warranties
				</button>
			</div>
		</template>
	</base-modal>
</template>

<script setup>
	import BaseModal from "../base/BaseModal.vue";

	defineProps({
		shop: { type: Object, default: () => null },
	});
	defineEmits(["confirm"]);
</script>
