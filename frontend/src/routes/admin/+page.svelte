<script>
	import { api } from '$lib/api.js';
	import { goto } from '$app/navigation';
	import { browser } from '$app/environment';
	import { onMount } from 'svelte';

	let username = $state('');
	let password = $state('');
	let loading = $state(false);
	let error = $state('');

	onMount(() => {
		if (browser && localStorage.getItem('admin_token')) {
			goto('/admin/dashboard');
		}
	});

	async function handleLogin(e) {
		e.preventDefault();
		loading = true;
		error = '';
		try {
			const res = await api.adminLogin({ username, password });
			localStorage.setItem('admin_token', res.access_token);
			goto('/admin/dashboard');
		} catch (e) {
			error = e.message || 'Login gagal';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Admin Login - Grafisa</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-indigo-50 to-gray-100 flex items-center justify-center p-4">
	<div class="bg-white rounded-3xl shadow-xl border border-gray-100 w-full max-w-md p-10">
		<div class="text-center mb-8">
			<div class="w-14 h-14 bg-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
				<span class="text-white font-extrabold text-xl">GR</span>
			</div>
			<h1 class="text-2xl font-extrabold text-gray-900">Admin Panel</h1>
			<p class="text-gray-500 text-sm mt-1">Masuk untuk mengelola toko</p>
		</div>

		<form onsubmit={handleLogin} class="space-y-4">
			{#if error}
				<div class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl text-sm">{error}</div>
			{/if}

			<div>
				<label class="block text-sm font-semibold text-gray-700 mb-1.5" for="username">Username</label>
				<input
					id="username"
					type="text"
					bind:value={username}
					required
					class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800"
				/>
			</div>

			<div>
				<label class="block text-sm font-semibold text-gray-700 mb-1.5" for="password">Password</label>
				<input
					id="password"
					type="password"
					bind:value={password}
					required
					class="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 text-gray-800"
				/>
			</div>

			<button
				type="submit"
				disabled={loading}
				class="w-full bg-indigo-600 text-white font-bold py-3 rounded-xl hover:bg-indigo-700 transition-colors disabled:opacity-60 mt-2"
			>
				{loading ? 'Masuk...' : 'Masuk'}
			</button>
		</form>

		<p class="text-center text-xs text-gray-400 mt-6">Default: admin / admin123</p>
	</div>
</div>
