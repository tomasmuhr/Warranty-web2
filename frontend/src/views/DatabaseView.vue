<template>
	<AlertMessage
		:message="alert.message"
		:type="alert.type"
		@close="alert.message = ''"
	/>

	<div class="text-center text-small card card-title">
		<p>{{ dbPath }}</p>
	</div>

	<div class="text-center">
		<div class="row row-cols-1 row-cols-md-3 g-4">
			<div class="col">
				<div class="card h-100">
					<a
						:href="exportDatabaseUrl()"
						class="card-link"
					>
						<div class="card-body pt-4">
							<div class="card-icon">⬇️</div>
							<h5 class="card-title mt-3">Backup DB</h5>
							<p class="card-text">
								Backup your database into a file.
							</p>
						</div>
						<div class="card-footer">
							<small class="text-muted">Backup DB</small>
						</div>
					</a>
				</div>
			</div>

			<div class="col">
				<div class="card h-100">
					<button
						type="button"
						class="btn btn-link card-link border-0 w-100 h-100"
						data-bs-toggle="modal"
						data-bs-target="#restoreDBModal"
					>
						<div class="card-body pt-4">
							<div class="card-icon">⬆️</div>
							<h5 class="card-title mt-3">Restore DB</h5>
							<p class="card-text">
								Restore your previously backed up database.
							</p>
						</div>
						<div class="card-footer">
							<small class="text-muted">Restore DB</small>
						</div>
					</button>
				</div>
			</div>

			<div class="col">
				<div class="card h-100">
					<button
						type="button"
						class="btn btn-link card-link border-0 w-100 h-100"
						data-bs-toggle="modal"
						data-bs-target="#purgeDBModal"
					>
						<div class="card-body pt-4">
							<div class="card-icon">🧹</div>
							<h5 class="card-title mt-3">Purge DB</h5>
							<p class="card-text">
								Delete orphaned warranties and/or empty shops.
							</p>
						</div>
						<div class="card-footer">
							<small class="text-muted">Purge database</small>
						</div>
					</button>
				</div>
			</div>
		</div>
	</div>

	<div
		class="modal fade"
		id="restoreDBModal"
		tabindex="-1"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content text-black">
				<div class="modal-header">
					<h5 class="modal-title">Restore DB</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					<p>Restore the database by previously backed up file.</p>
					<h5 class="text-red">Warning!</h5>
					<p class="text-red">
						The content of your current database will be overwritten
						by selected file.
					</p>
					<input
						type="file"
						class="form-control form-control-sm"
						accept=".db"
						@change="restoreFile = $event.target.files[0]"
					/>
					<button
						class="btn btn-sm btn-primary mt-3"
						@click="submitRestore"
					>
						Restore DB
					</button>
				</div>
			</div>
		</div>
	</div>

	<div
		class="modal fade"
		id="purgeDBModal"
		tabindex="-1"
		aria-hidden="true"
	>
		<div class="modal-dialog">
			<div class="modal-content text-black">
				<div class="modal-header">
					<h5 class="modal-title">Purge DB</h5>
					<button
						type="button"
						class="btn-close"
						data-bs-dismiss="modal"
						aria-label="Close"
					></button>
				</div>
				<div class="modal-body">
					<p>
						Delete warranties without linked shops and/or shops
						without linked warranties.
					</p>
					<h5 class="text-red">Warning!</h5>
					<p class="text-red">
						The records will be permanently deleted.
					</p>
					<div class="form-check">
						<input
							id="purge-warranties"
							v-model="purgeOption"
							class="form-check-input"
							type="radio"
							value="warranties"
						/>
						<label
							class="form-check-label"
							for="purge-warranties"
							>warranties</label
						>
					</div>
					<div class="form-check">
						<input
							id="purge-shops"
							v-model="purgeOption"
							class="form-check-input"
							type="radio"
							value="shops"
						/>
						<label
							class="form-check-label"
							for="purge-shops"
							>shops</label
						>
					</div>
					<div class="form-check">
						<input
							id="purge-both"
							v-model="purgeOption"
							class="form-check-input"
							type="radio"
							value="both"
						/>
						<label
							class="form-check-label"
							for="purge-both"
							>warranties and shops</label
						>
					</div>
					<button
						class="btn btn-sm btn-primary mt-3"
						data-bs-dismiss="modal"
						@click="submitPurge"
					>
						Purge DB
					</button>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
	import { onMounted, reactive, ref } from "vue";
	import AlertMessage from "../components/AlertMessage.vue";
	import {
		exportDatabaseUrl,
		getDatabaseInfo,
		purgeDatabase,
		restoreDatabase,
	} from "../api/client";

	const dbPath = ref("");
	const alert = reactive({ message: "", type: "success" });
	const purgeOption = ref("both");
	const restoreFile = ref(null);

	function showAlert(message, type = "success") {
		alert.message = message;
		alert.type = type;
	}

	onMounted(async () => {
		const info = await getDatabaseInfo();
		dbPath.value = info.path;
	});

	async function submitRestore() {
		if (!restoreFile.value) {
			showAlert("No file selected.", "danger");
			return;
		}
		try {
			const result = await restoreDatabase(restoreFile.value);
			showAlert(result.message);
			restoreFile.value = null;
			const info = await getDatabaseInfo();
			dbPath.value = info.path;
		} catch (error) {
			showAlert(
				error.response?.data?.detail || "Database restoration failed.",
				"danger",
			);
		}
	}

	async function submitPurge() {
		const result = await purgeDatabase(purgeOption.value);
		showAlert(result.message);
	}
</script>
