import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

const stored = browser ? JSON.parse(localStorage.getItem('cart') || '[]') : [];
export const cart = writable(stored);

if (browser) {
	cart.subscribe((value) => {
		localStorage.setItem('cart', JSON.stringify(value));
	});
}

export const cartCount = derived(cart, ($cart) => $cart.length);
export const cartTotal = derived(cart, ($cart) => $cart.reduce((sum, item) => sum + item.price, 0));

export function addToCart(product) {
	cart.update((items) => {
		if (items.find((i) => i.id === product.id)) return items;
		return [...items, product];
	});
}

export function removeFromCart(productId) {
	cart.update((items) => items.filter((i) => i.id !== productId));
}

export function clearCart() {
	cart.set([]);
}
