<template>
	<BaseModal id="shopFormModal">
		<template #title>
			{{ isEdit ? "Record update" : "Shop details" }}
		</template>

		<template #body>
			<!-- Notice the specific ID given to this form -->
			<form
				@submit.prevent="handleSubmit"
				id="shopForm"
			>
				<div class="mb-2">
					<label class="form-label">Name*</label>
					<input
						v-model="form.name"
						class="form-control form-control-sm"
						required
					/>
				</div>
				<div class="mb-2">
					<label class="form-label">Street</label>
					<input
						v-model="form.street"
						class="form-control form-control-sm"
					/>
				</div>
				<div class="mb-2">
					<label class="form-label">City</label>
					<input
						v-model="form.city"
						class="form-control form-control-sm"
					/>
				</div>
				<div class="mb-2">
					<label class="form-label">Zip Code</label>
					<input
						v-model="form.zip_code"
						class="form-control form-control-sm"
					/>
				</div>
				<div class="text-danger mt-2 text-small">* required field</div>
			</form>
		</template>

		<!-- Injecting the submit button into the footer slot -->
		<template #footer>
			<button
				type="button"
				class="btn btn-sm btn-secondary"
				data-bs-dismiss="modal"
			>
				Cancel
			</button>
			<!-- The 'form' attribute links this button to the form above -->
			<button
				type="submit"
				form="shopForm"
				class="btn btn-sm btn-primary"
				data-bs-dismiss="modal"
			>
				{{ isEdit ? "Update record" : "Add shop" }}
			</button>
		</template>
	</BaseModal>
</template>

<script setup>
	import { ref, computed, watch } from "vue";
	import BaseModal from "../base/BaseModal.vue";

	const props = defineProps({
		shop: { type: Object, default: () => null },
	});

	const emit = defineEmits(["save"]);

	const form = ref({ name: "", street: "", city: "", zip_code: "" });
	const isEdit = computed(() => !!props.shop && !!props.shop.id);

	watch(
		() => props.shop,
		(newShop) => {
			if (newShop) {
				form.value = { ...newShop };
			} else {
				form.value = { name: "", street: "", city: "", zip_code: "" };
			}
		},
		{ immediate: true },
	);

	function handleSubmit() {
		emit("save", {
			id: isEdit.value ? props.shop.id : null,
			data: form.value,
		});
	}
</script>
