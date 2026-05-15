<script>
	import '../app.css';
	import { page } from '$app/stores';
	import { cartCount } from '$lib/stores/cart.js';

	let mobileMenuOpen = $state(false);
	let { children } = $props();

	const isAdmin = $derived($page.url.pathname.startsWith('/admin'));
</script>

<svelte:head>
	<title>Grafisa - Template Canva</title>
</svelte:head>

<div class={isAdmin ? '' : 'min-h-screen flex flex-col'}>
{#if !isAdmin}
	<nav class="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
		<div class="max-w-6xl mx-auto px-4">
			<div class="flex items-center justify-between h-16">
				<a href="/" class="flex items-center gap-2">
					<div class="w-8 h-8 bg-indigo-600 rounded-lg flex items-center justify-center">
						<span class="text-white font-bold text-sm">GR</span>
					</div>
					<span class="font-bold text-gray-900 text-lg">Grafisa</span>
				</a>

				<div class="hidden md:flex items-center gap-6">
					<a href="/" class="text-gray-600 hover:text-indigo-600 font-medium transition-colors">Beranda</a>
					<a href="/products" class="text-gray-600 hover:text-indigo-600 font-medium transition-colors">Produk</a>
					<a href="/cart" class="relative flex items-center gap-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors font-medium text-sm">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
						</svg>
						Keranjang
						{#if $cartCount > 0}
							<span class="bg-white text-indigo-600 text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">{$cartCount}</span>
						{/if}
					</a>
				</div>

				<button
					aria-label="Toggle menu"
					class="md:hidden p-2 rounded-lg text-gray-600 hover:bg-gray-100"
					onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
					</svg>
				</button>
			</div>

			{#if mobileMenuOpen}
				<div class="md:hidden pb-4 flex flex-col gap-3">
					<a href="/" class="text-gray-700 font-medium py-2" onclick={() => (mobileMenuOpen = false)}>Beranda</a>
					<a href="/products" class="text-gray-700 font-medium py-2" onclick={() => (mobileMenuOpen = false)}>Produk</a>
					<a href="/cart" class="text-gray-700 font-medium py-2 flex items-center gap-2" onclick={() => (mobileMenuOpen = false)}>
						Keranjang {#if $cartCount > 0}<span class="bg-indigo-600 text-white text-xs rounded-full px-2 py-0.5">{$cartCount}</span>{/if}
					</a>
				</div>
			{/if}
		</div>
	</nav>
{/if}

<div class={isAdmin ? '' : 'flex-1'}>
	{@render children()}
</div>

{#if !isAdmin}
	<footer class="bg-gray-900 text-gray-400 py-10">
		<div class="max-w-6xl mx-auto px-4 text-center">
			<div class="flex items-center justify-center gap-2 mb-3">
				<div class="w-7 h-7 bg-indigo-500 rounded-lg flex items-center justify-center">
					<span class="text-white font-bold text-xs">GR</span>
				</div>
				<span class="text-white font-bold">Grafisa</span>
			</div>
			<p class="text-sm">Template Canva profesional untuk bisnis online kamu.</p>
			<p class="text-xs mt-4">© 2026 Grafisa.</p>
		</div>
	</footer>
{/if}
</div>
