<script>
	import { cart, cartTotal, clearCart } from '$lib/stores/cart.js';
	import { api } from '$lib/api.js';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';

	let name = $state('');
	let email = $state('');
	let phone = $state('');
	let loading = $state(false);
	let error = $state('');

	function formatPrice(price) {
		return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price);
	}

	async function handleCheckout(e) {
		e.preventDefault();
		if ($cart.length === 0) return;

		loading = true;
		error = '';

		try {
			const orderData = {
				buyer_name: name,
				buyer_email: email,
				buyer_phone: phone,
				items: $cart.map((item) => ({ product_id: item.id, quantity: 1 }))
			};

			const order = await api.createOrder(orderData);
			const payment = await api.createPayment(order.order_id);

			clearCart();

			if (browser && window.snap) {
				window.snap.pay(payment.token, {
					onSuccess: () => goto(`/payment/success?order_id=${order.order_id}`),
					onPending: () => goto(`/payment/success?order_id=${order.order_id}`),
					onError: () => { error = 'Pembayaran gagal. Silakan coba lagi.'; loading = false; },
					onClose: () => { loading = false; }
				});
			} else {
				window.location.href = payment.redirect_url;
			}
		} catch (e) {
			error = e.message || 'Terjadi kesalahan. Silakan coba lagi.';
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Checkout - Grafisa</title>
	<script src="https://app.sandbox.midtrans.com/snap/snap.js" data-client-key="SB-Mid-client-placeholder"></script>
</svelte:head>

<div class="max-w-4xl mx-auto px-4 py-12">
	<h1 class="text-3xl font-extrabold text-gray-900 mb-8">Checkout</h1>

	{#if $cart.length === 0}
		<div class="text-center py-20">
			<p class="text-gray-500 text-lg mb-6">Keranjang kamu kosong</p>
			<a href="/products" class="bg-indigo-600 text-white font-bold px-8 py-3 rounded-xl hover:bg-indigo-700 transition-colors">
				Lihat Produk
			</a>
		</div>
	{:else}
		<div class="grid md:grid-cols-5 gap-8">
			<div class="md:col-span-3">
				<form onsubmit={handleCheckout} class="space-y-5">
					<h2 class="text-lg font-bold text-gray-800">Informasi Pembeli</h2>

					{#if error}
						<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">{error}</div>
					{/if}

					<div>
						<label class="block text-sm font-semibold text-gray-700 mb-1.5" for="name">Nama Lengkap *</label>
						<input
							id="name"
							type="text"
							bind:value={name}
							required
							placeholder="Masukkan nama lengkap"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800"
						/>
					</div>

					<div>
						<label class="block text-sm font-semibold text-gray-700 mb-1.5" for="email">Email *</label>
						<input
							id="email"
							type="email"
							bind:value={email}
							required
							placeholder="email@kamu.com"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800"
						/>
						<p class="text-xs text-gray-400 mt-1">Link template akan dikirim ke email ini setelah pembayaran</p>
					</div>

					<div>
						<label class="block text-sm font-semibold text-gray-700 mb-1.5" for="phone">No. HP (opsional)</label>
						<input
							id="phone"
							type="tel"
							bind:value={phone}
							placeholder="08xxxxxxxxxx"
							class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800"
						/>
					</div>

					<button
						type="submit"
						disabled={loading}
						class="w-full bg-indigo-600 text-white font-bold py-3.5 rounded-xl hover:bg-indigo-700 transition-colors text-lg shadow-md disabled:opacity-60 disabled:cursor-not-allowed mt-2"
					>
						{#if loading}
							<span class="flex items-center justify-center gap-2">
								<svg class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
									<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
									<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
								</svg>
								Memproses...
							</span>
						{:else}
							Bayar Sekarang · {formatPrice($cartTotal)}
						{/if}
					</button>
				</form>
			</div>

			<div class="md:col-span-2">
				<div class="bg-gray-50 rounded-2xl p-5 border border-gray-100 sticky top-24">
					<h3 class="font-bold text-gray-900 mb-4">Ringkasan Order</h3>
					<div class="space-y-3">
						{#each $cart as item}
							<div class="flex justify-between text-sm">
								<span class="text-gray-700 truncate pr-2">{item.name}</span>
								<span class="text-gray-900 font-semibold flex-shrink-0">{formatPrice(item.price)}</span>
							</div>
						{/each}
					</div>
					<div class="border-t border-gray-200 mt-4 pt-4 flex justify-between font-bold text-gray-900">
						<span>Total</span>
						<span class="text-indigo-700 text-lg">{formatPrice($cartTotal)}</span>
					</div>
					<div class="mt-4 p-3 bg-green-50 rounded-lg">
						<p class="text-xs text-green-700 font-medium">🔒 Pembayaran aman via Midtrans</p>
						<p class="text-xs text-green-600 mt-0.5">Transfer Bank · GoPay · OVO · QRIS · dll</p>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
