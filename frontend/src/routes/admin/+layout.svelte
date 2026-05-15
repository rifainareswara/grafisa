<script>
	import { page } from '$app/stores';
	import { browser } from '$app/environment';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let { children } = $props();

	const isLoginPage = $derived($page.url.pathname === '/admin');

	onMount(() => {
		if (!isLoginPage) {
			const token = localStorage.getItem('admin_token');
			if (!token) goto('/admin');
		}
	});

	function logout() {
		localStorage.removeItem('admin_token');
		goto('/admin');
	}

	const navLinks = [
		{ href: '/admin/dashboard', label: 'Dashboard', icon: '📊' },
		{ href: '/admin/products', label: 'Produk', icon: '🗂️' },
		{ href: '/admin/orders', label: 'Orders', icon: '📦' },
	];
</script>

{#if isLoginPage}
	{@render children()}
{:else}
	<div class="min-h-screen bg-gray-100 flex">
		<aside class="w-56 bg-white border-r border-gray-200 flex flex-col fixed h-full">
			<div class="p-5 border-b border-gray-100">
				<div class="flex items-center gap-2">
					<div class="w-7 h-7 bg-indigo-600 rounded-lg flex items-center justify-center">
						<span class="text-white font-bold text-xs">TC</span>
					</div>
					<span class="font-bold text-gray-900">Admin Panel</span>
				</div>
			</div>
			<nav class="flex-1 p-4 space-y-1">
				{#each navLinks as link}
					<a
						href={link.href}
						class="flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium transition-colors {$page.url.pathname.startsWith(link.href) ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'}"
					>
						<span>{link.icon}</span>
						{link.label}
					</a>
				{/each}
			</nav>
			<div class="p-4 border-t border-gray-100">
				<button
					onclick={logout}
					class="w-full flex items-center gap-2 px-3 py-2.5 text-sm font-medium text-red-600 hover:bg-red-50 rounded-xl transition-colors"
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
					</svg>
					Logout
				</button>
				<a href="/" class="mt-1 flex items-center gap-2 px-3 py-2 text-xs text-gray-400 hover:text-indigo-600 transition-colors">
					← Lihat website
				</a>
			</div>
		</aside>
		<main class="flex-1 ml-56 p-8">
			{@render children()}
		</main>
	</div>
{/if}
