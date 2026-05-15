<script>
	import { cart, cartTotal, removeFromCart } from '$lib/stores/cart.js';

	function formatPrice(price) {
		return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price);
	}
</script>

<svelte:head>
	<title>Keranjang - Grafisa</title>
</svelte:head>

<div class="max-w-3xl mx-auto px-4 py-12">
	<h1 class="text-3xl font-extrabold text-gray-900 mb-8">Keranjang Belanja</h1>

	{#if $cart.length === 0}
		<div class="text-center py-20">
			<div class="text-6xl mb-4">🛒</div>
			<p class="text-gray-500 text-lg mb-6">Keranjang kamu masih kosong</p>
			<a href="/products" class="bg-indigo-600 text-white font-bold px-8 py-3 rounded-xl hover:bg-indigo-700 transition-colors">
				Lihat Produk
			</a>
		</div>
	{:else}
		<div class="space-y-4 mb-8">
			{#each $cart as item}
				<div class="bg-white rounded-2xl border border-gray-100 p-4 flex gap-4 shadow-sm">
					<img
						src={item.image_url || 'https://placehold.co/100x100/6366f1/white?text=TC'}
						alt={item.name}
						class="w-20 h-20 rounded-xl object-cover flex-shrink-0"
					/>
					<div class="flex-1 min-w-0">
						<span class="text-xs text-indigo-600 font-semibold bg-indigo-50 px-2 py-0.5 rounded-full">{item.category}</span>
						<h3 class="font-bold text-gray-900 mt-1 truncate">{item.name}</h3>
						<p class="text-gray-500 text-sm line-clamp-1">{item.description}</p>
					</div>
					<div class="flex flex-col items-end gap-2 flex-shrink-0">
						<span class="font-bold text-indigo-700 text-lg">{formatPrice(item.price)}</span>
						<button
							onclick={() => removeFromCart(item.id)}
							class="text-xs text-red-500 hover:text-red-700 hover:underline font-medium"
						>
							Hapus
						</button>
					</div>
				</div>
			{/each}
		</div>

		<div class="bg-gray-50 rounded-2xl p-6 border border-gray-100">
			<div class="flex justify-between items-center mb-2">
				<span class="text-gray-600">Subtotal ({$cart.length} item)</span>
				<span class="font-semibold text-gray-900">{formatPrice($cartTotal)}</span>
			</div>
			<div class="flex justify-between items-center mb-5 pb-4 border-b border-gray-200">
				<span class="text-gray-600">Biaya layanan</span>
				<span class="font-semibold text-green-600">Gratis</span>
			</div>
			<div class="flex justify-between items-center text-xl font-extrabold text-gray-900 mb-6">
				<span>Total</span>
				<span class="text-indigo-700">{formatPrice($cartTotal)}</span>
			</div>
			<a
				href="/checkout"
				class="block w-full text-center bg-indigo-600 text-white font-bold py-3.5 rounded-xl hover:bg-indigo-700 transition-colors text-lg shadow-md"
			>
				Lanjut ke Checkout →
			</a>
		</div>

		<div class="mt-4 text-center">
			<a href="/products" class="text-indigo-600 hover:underline text-sm font-medium">← Lanjutkan Belanja</a>
		</div>
	{/if}
</div>
