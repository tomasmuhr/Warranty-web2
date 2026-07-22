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
			<ItemWarranties
				v-if="itemsData"
				:under-warranty="itemsData.under_warranty"
				:out-of-warranty="itemsData.out_of_warranty"
			/>
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
	import ItemWarranties from "../items/ItemWarranties.vue";

	defineProps({
		shop: { type: Object, default: () => null },
		itemsData: { type: Object, default: () => null },
	});
</script>
