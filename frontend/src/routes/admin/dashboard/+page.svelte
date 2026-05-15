<script>
	import { onMount } from 'svelte';
	import { api } from '$lib/api.js';

	let stats = $state(null);
	let recentOrders = $state([]);
	let loading = $state(true);

	onMount(async () => {
		try {
			const [s, orders] = await Promise.all([api.getStats(), api.listOrders()]);
			stats = s;
			recentOrders = orders.slice(0, 5);
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	});

	function formatPrice(price) {
		return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price);
	}

	function statusColor(status) {
		return { paid: 'bg-green-100 text-green-700', pending: 'bg-yellow-100 text-yellow-700', cancelled: 'bg-red-100 text-red-700' }[status] || '';
	}
</script>

<svelte:head>
	<title>Dashboard - Admin Grafisa</title>
</svelte:head>

<div>
	<h1 class="text-2xl font-extrabold text-gray-900 mb-6">Dashboard</h1>

	{#if loading}
		<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
			{#each Array(4) as _}
				<div class="bg-gray-100 rounded-2xl h-28 animate-pulse"></div>
			{/each}
		</div>
	{:else if stats}
		<div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
			{#each [
				{ label: 'Total Revenue', value: formatPrice(stats.total_revenue), color: 'bg-indigo-600', icon: '💰' },
				{ label: 'Order Dibayar', value: stats.paid_orders, color: 'bg-green-600', icon: '✅' },
				{ label: 'Order Pending', value: stats.pending_orders, color: 'bg-yellow-500', icon: '⏳' },
				{ label: 'Total Produk', value: stats.total_products, color: 'bg-purple-600', icon: '🗂️' },
			] as card}
				<div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm">
					<div class="flex items-center justify-between mb-3">
						<span class="text-gray-500 text-sm font-medium">{card.label}</span>
						<span class="text-xl">{card.icon}</span>
					</div>
					<p class="text-2xl font-extrabold text-gray-900">{card.value}</p>
				</div>
			{/each}
		</div>
	{/if}

	<div class="bg-white rounded-2xl border border-gray-100 shadow-sm">
		<div class="p-5 border-b border-gray-100 flex justify-between items-center">
			<h2 class="font-bold text-gray-900">Order Terbaru</h2>
			<a href="/admin/orders" class="text-sm text-indigo-600 hover:underline font-medium">Lihat semua →</a>
		</div>
		<div class="overflow-x-auto">
			{#if recentOrders.length === 0}
				<div class="text-center py-10 text-gray-400">Belum ada order</div>
			{:else}
				<table class="w-full">
					<thead>
						<tr class="text-xs font-semibold text-gray-500 uppercase bg-gray-50">
							<th class="px-5 py-3 text-left">Order ID</th>
							<th class="px-5 py-3 text-left">Pembeli</th>
							<th class="px-5 py-3 text-left">Total</th>
							<th class="px-5 py-3 text-left">Status</th>
							<th class="px-5 py-3 text-left">Tanggal</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-50">
						{#each recentOrders as order}
							<tr class="hover:bg-gray-50 transition-colors">
								<td class="px-5 py-3 font-mono text-sm font-semibold text-gray-700">{order.order_id}</td>
								<td class="px-5 py-3">
									<div class="text-sm font-medium text-gray-900">{order.buyer_name}</div>
									<div class="text-xs text-gray-400">{order.buyer_email}</div>
								</td>
								<td class="px-5 py-3 font-semibold text-gray-900 text-sm">{formatPrice(order.total_amount)}</td>
								<td class="px-5 py-3">
									<span class="text-xs font-semibold px-2.5 py-1 rounded-full {statusColor(order.status)}">{order.status}</span>
								</td>
								<td class="px-5 py-3 text-xs text-gray-400">{new Date(order.created_at).toLocaleDateString('id-ID')}</td>
							</tr>
						{/each}
					</tbody>
				</table>
			{/if}
		</div>
	</div>
</div>
