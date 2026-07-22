<template>
	<BaseModal id="itemFormModal">
		<template #title>
			{{ isEdit ? "Record update" : "Item details" }}
		</template>

		<template #body>
			<form
				id="itemForm"
				@submit.prevent="handleSubmit"
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
					<label class="form-label">Shop</label>
					<select
						v-model="form.shop_id"
						class="form-select form-select-sm"
					>
						<option value="">—</option>
						<option
							v-for="shop in shops"
							:key="shop.id"
							:value="shop.id"
						>
							{{ shop.name }}
						</option>
					</select>
				</div>
				<div class="mb-2">
					<label class="form-label">Receipt Nr</label>
					<input
						v-model="form.receipt_nr"
						class="form-control form-control-sm"
					/>
				</div>
				<div class="mb-2">
					<label class="form-label">Amount</label>
					<input
						v-model="form.amount"
						type="number"
						min="0"
						class="form-control form-control-sm"
					/>
				</div>
				<div class="mb-2">
					<label class="form-label">Price per piece</label>
					<input
						v-model="form.price_per_piece"
						type="number"
						step="0.01"
						class="form-control form-control-sm"
					/>
				</div>
				<div class="mb-2">
					<label class="form-label">Comment</label>
					<input
						v-model="form.comment"
						class="form-control form-control-sm"
					/>
				</div>
				<div class="mb-2">
					<label class="form-label">Purchase date*</label>
					<input
						v-model="form.purchase_date"
						type="date"
						class="form-control form-control-sm"
						required
					/>
				</div>
				<div class="mb-2">
					<label class="form-label">Warranty length (months)*</label>
					<input
						v-model="form.warranty_months"
						type="number"
						min="1"
						class="form-control form-control-sm"
						required
					/>
				</div>
				<div class="text-danger mt-2 text-small">* required field</div>
			</form>
		</template>

		<template #footer>
			<button
				type="button"
				class="btn btn-sm btn-secondary"
				data-bs-dismiss="modal"
			>
				Cancel
			</button>
			<button
				type="submit"
				form="itemForm"
				class="btn btn-sm btn-primary"
				data-bs-dismiss="modal"
			>
				{{ isEdit ? "Update record" : "Add item" }}
			</button>
		</template>
	</BaseModal>
</template>

<script setup>
	import { ref, computed, watch } from "vue";
	import BaseModal from "../base/BaseModal.vue";

	const props = defineProps({
		item: { type: Object, default: () => null },
		shops: { type: Array, default: () => [] },
	});

	const emit = defineEmits(["save"]);

	// const defaultFormState = () => ({
	const defaultFormState = {
		name: "",
		shop_id: "",
		receipt_nr: "",
		amount: "",
		price_per_piece: "",
		comment: "",
		purchase_date: new Date().toISOString().slice(0, 10),
		warranty_months: 12,
	};

	// const form = ref(defaultFormState());
	const form = ref(defaultFormState);
	const isEdit = computed(() => !!props.item && !!props.item.id);

	watch(
		() => props.item,
		(newItem) => {
			if (newItem) {
				form.value = {
					name: newItem.name ?? "",
					shop_id: newItem.shop_id ?? "",
					receipt_nr: newItem.receipt_nr ?? "",
					amount: newItem.amount ?? "",
					price_per_piece: newItem.price_per_piece ?? "",
					comment: newItem.comment ?? "",
					purchase_date:
						newItem.purchase_date ??
						new Date().toISOString().slice(0, 10),
					warranty_months: newItem.warranty_months ?? 12,
				};
			} else {
				// form.value = defaultFormState();
				form.value = defaultFormState;
			}
		},
		{ immediate: true },
	);

	function handleSubmit() {
		emit("save", {
			id: isEdit.value ? props.item.id : null,
			data: {
				...form.value,
				shop_id: form.value.shop_id ? Number(form.value.shop_id) : null,
				amount:
					form.value.amount === "" ? null : Number(form.value.amount),
				price_per_piece:
					form.value.price_per_piece === ""
						? null
						: Number(form.value.price_per_piece),
				warranty_months: Number(form.value.warranty_months),
			},
		});
	}
</script>
