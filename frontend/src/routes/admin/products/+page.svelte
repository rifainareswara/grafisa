<script>
	import { onMount } from 'svelte';
	import { api } from '$lib/api.js';

	let products = $state([]);
	let loading = $state(true);
	let showForm = $state(false);
	let editingProduct = $state(null);
	let saving = $state(false);
	let deleteConfirmId = $state(null);

	let form = $state({ name: '', description: '', target: '', price: '', category: '', image_url: '', canva_link: '' });

	onMount(async () => {
		await loadProducts();
	});

	async function loadProducts() {
		loading = true;
		try {
			products = await api.getProducts();
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	}

	function openAdd() {
		editingProduct = null;
		form = { name: '', description: '', target: '', price: '', category: '', image_url: '', canva_link: '' };
		showForm = true;
	}

	function openEdit(product) {
		editingProduct = product;
		form = { ...product, price: String(product.price) };
		showForm = true;
	}

	async function handleSave(e) {
		e.preventDefault();
		saving = true;
		try {
			const data = { ...form, price: Number(form.price) };
			if (editingProduct) {
				await api.updateProduct(editingProduct.id, data);
			} else {
				await api.createProduct(data);
			}
			showForm = false;
			await loadProducts();
		} catch (e) {
			alert(e.message);
		} finally {
			saving = false;
		}
	}

	async function handleDelete(id) {
		try {
			await api.deleteProduct(id);
			deleteConfirmId = null;
			await loadProducts();
		} catch (e) {
			alert(e.message);
		}
	}

	function formatPrice(price) {
		return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price);
	}
</script>

<svelte:head>
	<title>Produk - Admin Grafisa</title>
</svelte:head>

<div>
	<div class="flex items-center justify-between mb-6">
		<h1 class="text-2xl font-extrabold text-gray-900">Kelola Produk</h1>
		<button
			onclick={openAdd}
			class="bg-indigo-600 text-white font-semibold px-5 py-2.5 rounded-xl hover:bg-indigo-700 transition-colors text-sm"
		>
			+ Tambah Produk
		</button>
	</div>

	{#if showForm}
		<div class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
			<div class="bg-white rounded-2xl shadow-xl w-full max-w-lg max-h-[90vh] overflow-y-auto p-6">
				<h2 class="text-lg font-bold text-gray-900 mb-5">{editingProduct ? 'Edit Produk' : 'Tambah Produk'}</h2>
				<form onsubmit={handleSave} class="space-y-4">
					{#each [
						{ key: 'name', label: 'Nama Produk', type: 'text', required: true },
						{ key: 'category', label: 'Kategori', type: 'text' },
						{ key: 'price', label: 'Harga (Rp)', type: 'number', required: true },
						{ key: 'target', label: 'Target Pembeli', type: 'text' },
						{ key: 'canva_link', label: 'Link Template Canva', type: 'url' },
						{ key: 'image_url', label: 'URL Gambar', type: 'url' },
					] as field}
						<div>
							<label class="block text-sm font-semibold text-gray-700 mb-1.5" for={field.key}>{field.label}</label>
							<input
								id={field.key}
								type={field.type}
								bind:value={form[field.key]}
								required={field.required}
								class="w-full px-3 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm"
							/>
						</div>
					{/each}
					<div>
						<label class="block text-sm font-semibold text-gray-700 mb-1.5" for="description">Deskripsi</label>
						<textarea
							id="description"
							bind:value={form.description}
							rows="3"
							class="w-full px-3 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-sm resize-none"
						></textarea>
					</div>
					<div class="flex gap-3 pt-2">
						<button
							type="submit"
							disabled={saving}
							class="flex-1 bg-indigo-600 text-white font-bold py-2.5 rounded-xl hover:bg-indigo-700 disabled:opacity-60 transition-colors"
						>
							{saving ? 'Menyimpan...' : 'Simpan'}
						</button>
						<button
							type="button"
							onclick={() => (showForm = false)}
							class="flex-1 border border-gray-200 text-gray-700 font-bold py-2.5 rounded-xl hover:bg-gray-50 transition-colors"
						>
							Batal
						</button>
					</div>
				</form>
			</div>
		</div>
	{/if}

	{#if deleteConfirmId}
		<div class="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
			<div class="bg-white rounded-2xl p-6 max-w-sm w-full shadow-xl">
				<h3 class="font-bold text-gray-900 mb-2">Hapus Produk?</h3>
				<p class="text-gray-500 text-sm mb-5">Aksi ini tidak bisa dibatalkan.</p>
				<div class="flex gap-3">
					<button onclick={() => handleDelete(deleteConfirmId)} class="flex-1 bg-red-600 text-white font-bold py-2.5 rounded-xl hover:bg-red-700">Hapus</button>
					<button onclick={() => (deleteConfirmId = null)} class="flex-1 border border-gray-200 text-gray-700 font-bold py-2.5 rounded-xl hover:bg-gray-50">Batal</button>
				</div>
			</div>
		</div>
	{/if}

	<div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-x-auto">
		{#if loading}
			<div class="p-8 text-center text-gray-400">Memuat data...</div>
		{:else if products.length === 0}
			<div class="p-8 text-center text-gray-400">Belum ada produk</div>
		{:else}
			<table class="w-full">
				<thead>
					<tr class="text-xs font-semibold text-gray-500 uppercase bg-gray-50">
						<th class="px-5 py-3 text-left">Produk</th>
						<th class="px-5 py-3 text-left">Kategori</th>
						<th class="px-5 py-3 text-left">Harga</th>
						<th class="px-5 py-3 text-left">Aksi</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-50">
					{#each products as product}
						<tr class="hover:bg-gray-50 transition-colors">
							<td class="px-5 py-3">
								<div class="flex items-center gap-3">
									<img
										src={product.image_url || 'https://placehold.co/60x60/6366f1/white?text=TC'}
										alt={product.name}
										class="w-10 h-10 rounded-lg object-cover flex-shrink-0"
									/>
									<div>
										<div class="font-semibold text-gray-900 text-sm">{product.name}</div>
										<div class="text-xs text-gray-400 truncate max-w-48">{product.description?.slice(0, 60)}...</div>
									</div>
								</div>
							</td>
							<td class="px-5 py-3 text-sm text-gray-600">{product.category}</td>
							<td class="px-5 py-3 font-semibold text-indigo-700 text-sm">{formatPrice(product.price)}</td>
							<td class="px-5 py-3">
								<div class="flex gap-2">
									<button
										onclick={() => openEdit(product)}
										class="text-xs px-3 py-1.5 bg-indigo-50 text-indigo-700 font-semibold rounded-lg hover:bg-indigo-100 transition-colors"
									>
										Edit
									</button>
									<button
										onclick={() => (deleteConfirmId = product.id)}
										class="text-xs px-3 py-1.5 bg-red-50 text-red-600 font-semibold rounded-lg hover:bg-red-100 transition-colors"
									>
										Hapus
									</button>
								</div>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}
	</div>
</div>
