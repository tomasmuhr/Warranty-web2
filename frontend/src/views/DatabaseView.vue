<template>
	<BaseMessage
		:message="alert.message"
		:type="alert.type"
		@close="alert.message = ''"
	/>

	<div class="text-center text-small card card-title">
		<p>{{ dbPath }}</p>
	</div>

	<div class="text-center">
		<div class="row row-cols-1 row-cols-md-3 g-4">
			<BaseCard
				tag="a"
				:href="exportDatabaseUrl()"
				icon="⬇️"
				title="Backup DB"
				text="Backup your database to your local machine."
				footerText="Backup DB"
			/>

			<BaseCard
				tag="button"
				type="button"
				data-bs-toggle="modal"
				data-bs-target="#restoreDBModal"
				icon="⬆️"
				title="Restore DB"
				text="Restore your previously backed up database."
				footerText="Restore DB"
			/>

			<BaseCard
				tag="button"
				type="button"
				data-bs-toggle="modal"
				data-bs-target="#purgeDBModal"
				icon="🧹"
				title="Purge DB"
				text="Delete orphaned warranties and/or empty shops."
				footerText="Purge database"
			/>
		</div>
	</div>

	<!-- Modals remain unchanged below -->
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
	import BaseMessage from "../components/base/BaseMessage.vue";
	import BaseCard from "../components/base/BaseCard.vue"; // Adjust path as needed
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
