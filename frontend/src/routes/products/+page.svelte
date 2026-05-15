<script>
	import { onMount } from 'svelte';
	import { api } from '$lib/api.js';
	import { addToCart } from '$lib/stores/cart.js';

	let products = $state([]);
	let loading = $state(true);
	let addedIds = $state(new Set());
	let search = $state('');

	onMount(async () => {
		try {
			products = await api.getProducts();
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	});

	const filtered = $derived(
		products.filter(
			(p) =>
				p.name.toLowerCase().includes(search.toLowerCase()) ||
				p.category?.toLowerCase().includes(search.toLowerCase())
		)
	);

	function handleAdd(product) {
		addToCart(product);
		addedIds = new Set([...addedIds, product.id]);
		setTimeout(() => {
			addedIds = new Set([...addedIds].filter((id) => id !== product.id));
		}, 1500);
	}

	function formatPrice(price) {
		return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price);
	}
</script>

<svelte:head>
	<title>Semua Template - Grafisa</title>
</svelte:head>

<div class="max-w-6xl mx-auto px-4 py-12">
	<div class="mb-10">
		<h1 class="text-3xl font-extrabold text-gray-900 mb-2">Semua Template</h1>
		<p class="text-gray-500">Template Canva siap edit untuk berbagai kebutuhan bisnis</p>
	</div>

	<div class="mb-8">
		<input
			type="text"
			bind:value={search}
			placeholder="Cari template..."
			class="w-full md:w-80 px-4 py-2.5 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-700"
		/>
	</div>

	{#if loading}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each Array(4) as _}
				<div class="bg-gray-100 rounded-2xl h-96 animate-pulse"></div>
			{/each}
		</div>
	{:else if filtered.length === 0}
		<div class="text-center py-20 text-gray-400">
			<p class="text-5xl mb-4">🔍</p>
			<p class="text-lg">Tidak ada template ditemukan</p>
		</div>
	{:else}
		<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
			{#each filtered as product}
				<div class="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow overflow-hidden">
					<a href="/products/{product.id}">
						<img
							src={product.image_url || 'https://placehold.co/600x400/6366f1/white?text=Template'}
							alt={product.name}
							class="w-full h-48 object-cover hover:scale-105 transition-transform duration-300"
						/>
					</a>
					<div class="p-5">
						<span class="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">{product.category}</span>
						<a href="/products/{product.id}">
							<h3 class="font-bold text-gray-900 text-lg mt-2 mb-2 hover:text-indigo-600">{product.name}</h3>
						</a>
						<p class="text-gray-500 text-sm mb-3 line-clamp-3">{product.description}</p>
						<div class="text-xs text-gray-400 mb-4">
							<span class="font-medium text-gray-600">Target:</span> {product.target}
						</div>
						<div class="flex items-center justify-between pt-3 border-t border-gray-100">
							<span class="text-indigo-700 font-bold text-xl">{formatPrice(product.price)}</span>
							<div class="flex gap-2">
								<a href="/products/{product.id}" class="text-sm px-3 py-1.5 rounded-lg border border-gray-200 text-gray-600 hover:border-indigo-300 hover:text-indigo-600 transition-colors font-medium">
									Detail
								</a>
								<button
									onclick={() => handleAdd(product)}
									class="text-sm font-semibold px-3 py-1.5 rounded-lg transition-colors {addedIds.has(product.id) ? 'bg-green-100 text-green-700' : 'bg-indigo-600 text-white hover:bg-indigo-700'}"
								>
									{addedIds.has(product.id) ? '✓ Added' : '+ Keranjang'}
								</button>
							</div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
