<template>
	<div
		class="modal fade"
		:id="modalId"
		tabindex="-1"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title">{{ title }}</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<form @submit.prevent="handleSubmit">
					<div class="modal-body">
						<div class="mb-2">
							<label class="form-label">Name*</label>
							<input
								v-model="formData.name"
								class="form-control form-control-sm"
								required
							/>
						</div>
						<div class="mb-2">
							<label class="form-label">Shop</label>
							<select
								v-model="formData.shop_id"
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
								v-model="formData.receipt_nr"
								class="form-control form-control-sm"
							/>
						</div>
						<div class="mb-2">
							<label class="form-label">Amount</label>
							<input
								v-model="formData.amount"
								type="number"
								min="0"
								class="form-control form-control-sm"
							/>
						</div>
						<div class="mb-2">
							<label class="form-label">Price per piece</label>
							<input
								v-model="formData.price_per_piece"
								type="number"
								step="0.01"
								class="form-control form-control-sm"
							/>
						</div>
						<div class="mb-2">
							<label class="form-label">Comment</label>
							<input
								v-model="formData.comment"
								class="form-control form-control-sm"
							/>
						</div>
						<div class="mb-2">
							<label class="form-label">Purchase date*</label>
							<input
								v-model="formData.purchase_date"
								type="date"
								class="form-control form-control-sm"
								required
							/>
						</div>
						<div class="mb-2">
							<label class="form-label"
								>Warranty length (months)*</label
							>
							<input
								v-model="formData.warranty_months"
								type="number"
								min="1"
								class="form-control form-control-sm"
								required
							/>
						</div>
						<button
							type="submit"
							class="btn btn-sm btn-primary"
						>
							{{ submitText }}
						</button>
						<div class="text-danger mt-2">* required field</div>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { reactive, watch } from "vue";

	const props = defineProps({
		modalId: { type: String, required: true },
		title: { type: String, required: true },
		submitText: { type: String, required: true },
		shops: { type: Array, default: () => [] },
		initialData: { type: Object, default: () => ({}) },
		isAdd: { type: Boolean, default: false },
	});

	const emit = defineEmits(["submit"]);

	const formData = reactive({ ...props.initialData });

	watch(
		() => props.initialData,
		(newData) => {
			Object.assign(formData, newData);
		},
		{ deep: true },
	);

	function handleSubmit() {
		emit("submit", { ...formData });
	}
</script>
