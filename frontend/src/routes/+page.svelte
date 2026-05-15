<script>
	import { onMount } from 'svelte';
	import { api } from '$lib/api.js';
	import { addToCart, cartCount } from '$lib/stores/cart.js';

	let products = $state([]);
	let loading = $state(true);
	let addedIds = $state(new Set());

	onMount(async () => {
		try {
			products = await api.getProducts();
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	});

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
	<title>Grafisa - Template Canva untuk Bisnis Online</title>
</svelte:head>

<!-- Hero Section -->
<section class="bg-gradient-to-br from-indigo-600 via-indigo-700 to-purple-800 text-white">
	<div class="max-w-6xl mx-auto px-4 py-20 md:py-28 text-center">
		<span class="inline-block bg-white/20 text-white text-sm font-semibold px-4 py-1.5 rounded-full mb-5">
			✨ Template Canva Siap Pakai
		</span>
		<h1 class="text-4xl md:text-5xl lg:text-6xl font-extrabold leading-tight mb-6">
			Desain Profesional<br />
			<span class="text-yellow-300">Tanpa Ribet</span>
		</h1>
		<p class="text-lg md:text-xl text-indigo-100 max-w-2xl mx-auto mb-10">
			Template Canva siap edit untuk UMKM dan online shop. Ganti teks & foto—langsung posting dalam hitungan menit.
		</p>
		<div class="flex flex-col sm:flex-row gap-4 justify-center">
			<a href="/products" class="bg-white text-indigo-700 font-bold px-8 py-3.5 rounded-xl hover:bg-yellow-50 transition-colors shadow-lg text-base">
				Lihat Semua Template →
			</a>
			<a href="/cart" class="border-2 border-white text-white font-bold px-8 py-3.5 rounded-xl hover:bg-white/10 transition-colors text-base">
				Keranjang ({$cartCount})
			</a>
		</div>
	</div>
</section>

<!-- Features -->
<section class="py-14 bg-gray-50">
	<div class="max-w-6xl mx-auto px-4">
		<div class="grid grid-cols-1 md:grid-cols-3 gap-6">
			{#each [
				{ icon: '', title: 'Siap Edit', desc: 'Langsung edit di Canva, tidak perlu skill desain khusus.' },
				{ icon: '', title: 'Profesional', desc: 'Desain yang menarik perhatian dan meningkatkan penjualan.' },
				{ icon: '', title: 'Akses Selamanya', desc: 'Beli sekali, gunakan selamanya tanpa biaya tambahan.' }
			] as f}
				<div class="bg-white rounded-2xl p-6 text-center shadow-sm border border-gray-100">
					<div class="text-3xl mb-3">{f.icon}</div>
					<h3 class="font-bold text-gray-900 text-lg mb-2">{f.title}</h3>
					<p class="text-gray-500 text-sm">{f.desc}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- Products -->
<section class="py-16">
	<div class="max-w-6xl mx-auto px-4">
		<div class="text-center mb-12">
			<h2 class="text-3xl md:text-4xl font-extrabold text-gray-900 mb-3">Template Pilihan</h2>
			<p class="text-gray-500 text-lg">Pilih template yang sesuai kebutuhan bisnis kamu</p>
		</div>

		{#if loading}
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
				{#each Array(4) as _}
					<div class="bg-gray-100 rounded-2xl h-80 animate-pulse"></div>
				{/each}
			</div>
		{:else}
			<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
				{#each products as product}
					<div class="bg-white rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow overflow-hidden group">
						<a href="/products/{product.id}">
							<img
								src={product.image_url || 'https://placehold.co/600x400/6366f1/white?text=Template'}
								alt={product.name}
								class="w-full h-44 object-cover group-hover:scale-105 transition-transform duration-300"
							/>
						</a>
						<div class="p-4">
							<span class="text-xs font-semibold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded-full">{product.category}</span>
							<a href="/products/{product.id}">
								<h3 class="font-bold text-gray-900 mt-2 mb-1 hover:text-indigo-600 transition-colors">{product.name}</h3>
							</a>
							<p class="text-gray-500 text-sm line-clamp-2 mb-3">{product.description}</p>
							<div class="flex items-center justify-between">
								<span class="text-indigo-700 font-bold text-lg">{formatPrice(product.price)}</span>
								<button
									onclick={() => handleAdd(product)}
									class="text-sm font-semibold px-3 py-1.5 rounded-lg transition-colors {addedIds.has(product.id) ? 'bg-green-100 text-green-700' : 'bg-indigo-600 text-white hover:bg-indigo-700'}"
								>
									{addedIds.has(product.id) ? '✓ Ditambahkan' : '+ Keranjang'}
								</button>
							</div>
						</div>
					</div>
				{/each}
			</div>
		{/if}

		<div class="text-center mt-10">
			<a href="/products" class="inline-block bg-indigo-600 text-white font-bold px-8 py-3 rounded-xl hover:bg-indigo-700 transition-colors">
				Lihat Semua →
			</a>
		</div>
	</div>
</section>

<!-- CTA -->
<section class="bg-indigo-600 py-16">
	<div class="max-w-3xl mx-auto px-4 text-center text-white">
		<h2 class="text-3xl font-extrabold mb-4">Siap upgrade konten bisnis kamu?</h2>
		<p class="text-indigo-100 text-lg mb-8">Ribuan UMKM sudah percaya Grafisa untuk konten yang menjual.</p>
		<a href="/products" class="bg-white text-indigo-700 font-bold px-8 py-3.5 rounded-xl hover:bg-yellow-50 transition-colors text-base shadow-lg">
			Mulai Sekarang →
		</a>
	</div>
</section>
