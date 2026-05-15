<script>
	import { onMount } from 'svelte';
	import { api } from '$lib/api.js';

	let orders = $state([]);
	let loading = $state(true);
	let filter = $state('all');

	onMount(async () => {
		try {
			orders = await api.listOrders();
		} catch (e) {
			console.error(e);
		} finally {
			loading = false;
		}
	});

	const filtered = $derived(filter === 'all' ? orders : orders.filter((o) => o.status === filter));

	function formatPrice(price) {
		return new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(price);
	}

	function statusColor(status) {
		return { paid: 'bg-green-100 text-green-700', pending: 'bg-yellow-100 text-yellow-700', cancelled: 'bg-red-100 text-red-700' }[status] || '';
	}
</script>

<svelte:head>
	<title>Orders - Admin Grafisa</title>
</svelte:head>

<div>
	<h1 class="text-2xl font-extrabold text-gray-900 mb-6">Semua Order</h1>

	<div class="flex gap-2 mb-6">
		{#each ['all', 'paid', 'pending', 'cancelled'] as f}
			<button
				onclick={() => (filter = f)}
				class="px-4 py-1.5 rounded-full text-sm font-semibold transition-colors capitalize {filter === f ? 'bg-indigo-600 text-white' : 'bg-white border border-gray-200 text-gray-600 hover:border-indigo-300'}"
			>
				{f === 'all' ? 'Semua' : f}
			</button>
		{/each}
	</div>

	<div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-x-auto">
		{#if loading}
			<div class="p-8 text-center text-gray-400">Memuat data...</div>
		{:else if filtered.length === 0}
			<div class="p-8 text-center text-gray-400">Tidak ada order</div>
		{:else}
			<table class="w-full">
				<thead>
					<tr class="text-xs font-semibold text-gray-500 uppercase bg-gray-50">
						<th class="px-5 py-3 text-left">Order ID</th>
						<th class="px-5 py-3 text-left">Pembeli</th>
						<th class="px-5 py-3 text-left">Item</th>
						<th class="px-5 py-3 text-left">Total</th>
						<th class="px-5 py-3 text-left">Status</th>
						<th class="px-5 py-3 text-left">Tanggal</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-50">
					{#each filtered as order}
						<tr class="hover:bg-gray-50 transition-colors">
							<td class="px-5 py-3 font-mono text-sm font-semibold text-gray-700">{order.order_id}</td>
							<td class="px-5 py-3">
								<div class="text-sm font-medium text-gray-900">{order.buyer_name}</div>
								<div class="text-xs text-gray-400">{order.buyer_email}</div>
								{#if order.buyer_phone}
									<div class="text-xs text-gray-400">{order.buyer_phone}</div>
								{/if}
							</td>
							<td class="px-5 py-3 text-sm text-gray-600">
								{#each order.items as item}
									<div class="truncate max-w-40">{item.product_name}</div>
								{/each}
							</td>
							<td class="px-5 py-3 font-semibold text-gray-900 text-sm">{formatPrice(order.total_amount)}</td>
							<td class="px-5 py-3">
								<span class="text-xs font-semibold px-2.5 py-1 rounded-full {statusColor(order.status)}">{order.status}</span>
							</td>
							<td class="px-5 py-3 text-xs text-gray-400">
								{new Date(order.created_at).toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' })}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		{/if}
	</div>
</div>
