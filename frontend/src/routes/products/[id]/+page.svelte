<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { api } from '$lib/api.js';
	import { addToCart, cart } from '$lib/stores/cart.js';

	let product = $state(null);
	let loading = $state(true);
	let added = $state(false);

	const inCart = $derived($cart.some((i) => i.id === product?.id));

	onMount(async () => {
		try {
			product = await api.getProduct($page.params.id);
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	});

	function handleAdd() {
		if (!product) return;
		addToCart(product);
		added = true;
	}

	function formatPrice(price) {
		return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price);
	}
</script>

<svelte:head>
	<title>{product?.name ?? 'Detail Produk'} - Grafisa</title>
</svelte:head>

<div class="max-w-5xl mx-auto px-4 py-12">
	{#if loading}
		<div class="grid md:grid-cols-2 gap-10 animate-pulse">
			<div class="bg-gray-100 rounded-2xl h-80"></div>
			<div class="space-y-4">
				<div class="h-6 bg-gray-100 rounded w-1/3"></div>
				<div class="h-8 bg-gray-100 rounded w-2/3"></div>
				<div class="h-4 bg-gray-100 rounded w-full"></div>
				<div class="h-4 bg-gray-100 rounded w-4/5"></div>
			</div>
		</div>
	{:else if !product}
		<div class="text-center py-20 text-gray-400">
			<p class="text-5xl mb-4">😢</p>
			<p class="text-xl font-semibold">Produk tidak ditemukan</p>
			<a href="/products" class="mt-4 inline-block text-indigo-600 hover:underline">← Kembali ke produk</a>
		</div>
	{:else}
		<a href="/products" class="text-indigo-600 hover:underline text-sm font-medium mb-8 inline-block">← Kembali ke semua produk</a>
		<div class="grid md:grid-cols-2 gap-10 mt-4">
			<div>
				<img
					src={product.image_url || 'https://placehold.co/600x400/6366f1/white?text=Template'}
					alt={product.name}
					class="w-full rounded-2xl shadow-lg object-cover"
				/>
			</div>
			<div>
				<span class="inline-block text-xs font-semibold text-indigo-600 bg-indigo-50 px-3 py-1 rounded-full mb-3">{product.category}</span>
				<h1 class="text-3xl font-extrabold text-gray-900 mb-3">{product.name}</h1>
				<p class="text-gray-500 leading-relaxed mb-5">{product.description}</p>

				<div class="bg-gray-50 rounded-xl p-4 mb-6 space-y-2">
					<div class="flex gap-2">
						<span class="text-sm font-semibold text-gray-600 w-24">Target:</span>
						<span class="text-sm text-gray-700">{product.target}</span>
					</div>
					<div class="flex gap-2">
						<span class="text-sm font-semibold text-gray-600 w-24">Kategori:</span>
						<span class="text-sm text-gray-700">{product.category}</span>
					</div>
				</div>

				<div class="flex items-center gap-3 mb-6">
					<span class="text-3xl font-extrabold text-indigo-700">{formatPrice(product.price)}</span>
				</div>

				<div class="flex gap-3">
					{#if inCart || added}
						<a
							href="/cart"
							class="flex-1 text-center bg-green-600 text-white font-bold py-3 rounded-xl hover:bg-green-700 transition-colors"
						>
							✓ Lihat Keranjang
						</a>
					{:else}
						<button
							onclick={handleAdd}
							class="flex-1 bg-indigo-600 text-white font-bold py-3 rounded-xl hover:bg-indigo-700 transition-colors"
						>
							+ Tambah ke Keranjang
						</button>
					{/if}
					<a href="/cart" class="flex-1 text-center border-2 border-indigo-600 text-indigo-600 font-bold py-3 rounded-xl hover:bg-indigo-50 transition-colors">
						Beli Sekarang
					</a>
				</div>

				<div class="mt-6 p-4 bg-yellow-50 border border-yellow-200 rounded-xl">
					<p class="text-sm text-yellow-800 font-medium">💡 Setelah pembayaran berhasil, link template Canva akan dikirim ke email kamu.</p>
				</div>
			</div>
		</div>
	{/if}
</div>
