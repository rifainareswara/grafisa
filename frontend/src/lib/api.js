import { env } from '$env/dynamic/public';

const BASE_URL = env.PUBLIC_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
	const token = typeof localStorage !== 'undefined' ? localStorage.getItem('admin_token') : null;
	const headers = { 'Content-Type': 'application/json', ...options.headers };
	if (token) headers['Authorization'] = `Bearer ${token}`;

	const res = await fetch(`${BASE_URL}${path}`, { ...options, headers });
	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: 'Terjadi kesalahan' }));
		throw new Error(err.detail || 'Request gagal');
	}
	return res.json();
}

export const api = {
	getProducts: () => request('/api/products/'),
	getProduct: (id) => request(`/api/products/${id}`),
	createProduct: (data) => request('/api/products/', { method: 'POST', body: JSON.stringify(data) }),
	updateProduct: (id, data) => request(`/api/products/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
	deleteProduct: (id) => request(`/api/products/${id}`, { method: 'DELETE' }),

	createOrder: (data) => request('/api/orders/', { method: 'POST', body: JSON.stringify(data) }),
	getOrder: (orderId) => request(`/api/orders/${orderId}`),
	listOrders: () => request('/api/orders/'),

	createPayment: (orderId) => request(`/api/payment/create/${orderId}`, { method: 'POST' }),

	adminLogin: (data) => request('/api/admin/login', { method: 'POST', body: JSON.stringify(data) }),
	getStats: () => request('/api/admin/stats'),
};
