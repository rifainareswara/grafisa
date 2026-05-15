<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { api } from '$lib/api.js';

	let order = $state(null);
	let loading = $state(true);

	onMount(async () => {
		const orderId = $page.url.searchParams.get('order_id');
		if (orderId) {
			try {
				order = await api.getOrder(orderId);
			} catch (e) {
				console.error(e);
			}
		}
		loading = false;
	});

	function formatPrice(price) {
		return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price);
	}
</script>

<svelte:head>
	<title>Pembayaran Berhasil - Grafisa</title>
</svelte:head>

<div class="max-w-2xl mx-auto px-4 py-16 text-center">
	{#if loading}
		<div class="animate-pulse space-y-4">
			<div class="h-20 w-20 bg-gray-100 rounded-full mx-auto"></div>
			<div class="h-8 bg-gray-100 rounded w-1/2 mx-auto"></div>
		</div>
	{:else if order}
		<div class="bg-white rounded-3xl shadow-lg border border-gray-100 p-10">
			<div class="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
				<svg class="w-10 h-10 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
				</svg>
			</div>

			{#if order.status === 'paid'}
				<h1 class="text-3xl font-extrabold text-gray-900 mb-3">Pembayaran Berhasil! 🎉</h1>
				<p class="text-gray-500 mb-8">Terima kasih <strong class="text-gray-700">{order.buyer_name}</strong>! Link template sudah dikirim ke <strong class="text-indigo-600">{order.buyer_email}</strong>.</p>

				<div class="bg-indigo-50 rounded-2xl p-5 mb-6 text-left space-y-3">
					<h3 class="font-bold text-gray-800 mb-2">Template kamu:</h3>
					{#each order.items as item}
						<div class="flex items-center gap-3 p-3 bg-white rounded-xl border border-indigo-100">
							<div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center text-white text-xs font-bold">✓</div>
							<div>
								<p class="font-semibold text-gray-900 text-sm">{item.product_name}</p>
								<p class="text-indigo-600 text-xs">{formatPrice(item.price)}</p>
							</div>
						</div>
					{/each}
				</div>
			{:else}
				<h1 class="text-3xl font-extrabold text-gray-900 mb-3">Order Diterima!</h1>
				<p class="text-gray-500 mb-6">Order kamu sedang diproses. Cek email setelah pembayaran dikonfirmasi.</p>
			{/if}

			<div class="text-sm text-gray-400 mb-6">
				Order ID: <span class="font-mono font-semibold text-gray-600">{order.order_id}</span>
			</div>

			<div class="flex gap-3 justify-center">
				<a href="/" class="bg-indigo-600 text-white font-bold px-6 py-3 rounded-xl hover:bg-indigo-700 transition-colors">
					Kembali ke Beranda
				</a>
				<a href="/products" class="border-2 border-gray-200 text-gray-700 font-bold px-6 py-3 rounded-xl hover:border-indigo-300 transition-colors">
					Lihat Produk Lain
				</a>
			</div>
		</div>
	{:else}
		<div>
			<h1 class="text-3xl font-extrabold text-gray-900 mb-3">Terima Kasih!</h1>
			<p class="text-gray-500 mb-6">Pembayaran kamu sedang diproses.</p>
			<a href="/" class="bg-indigo-600 text-white font-bold px-6 py-3 rounded-xl hover:bg-indigo-700 transition-colors">
				Kembali ke Beranda
			</a>
		</div>
	{/if}
</div>
