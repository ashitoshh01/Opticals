import {
  Category, Product, ProductListResponse, ProductFilters,
  AuthToken, CartItem, WishlistItem, Address, Order, Review, User
} from './types';

const API = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string> || {}),
  };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const res = await fetch(`${API}${path}`, { ...options, headers });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || 'Request failed');
  }
  if (res.status === 204) return undefined as T;
  return res.json();
}

// Auth
export const authApi = {
  signup: (data: { name: string; email: string; password: string; phone?: string }) =>
    request<AuthToken>('/auth/signup', { method: 'POST', body: JSON.stringify(data) }),
  login: (data: { email: string; password: string }) =>
    request<AuthToken>('/auth/login', { method: 'POST', body: JSON.stringify(data) }),
  me: () => request<User>('/auth/me'),
};

// Categories
export const categoriesApi = {
  list: () => request<Category[]>('/categories'),
};

// Products
export const productsApi = {
  list: (filters: ProductFilters = {}) => {
    const params = new URLSearchParams();
    Object.entries(filters).forEach(([k, v]) => {
      if (v !== undefined && v !== null && v !== '') params.set(k, String(v));
    });
    return request<ProductListResponse>(`/products?${params}`);
  },
  get: (slug: string) => request<Product>(`/products/${slug}`),
  getReviews: (productId: number) => request<Review[]>(`/products/${productId}/reviews`),
  addReview: (productId: number, data: { rating: number; comment?: string }) =>
    request<Review>(`/products/${productId}/reviews`, { method: 'POST', body: JSON.stringify(data) }),
};

// Search
export const searchApi = {
  search: (q: string, page = 1) =>
    request<ProductListResponse>(`/search?q=${encodeURIComponent(q)}&page=${page}`),
};

// Cart
export const cartApi = {
  list: () => request<CartItem[]>('/cart'),
  add: (product_id: number, quantity = 1, has_power = false) =>
    request<CartItem>('/cart', { method: 'POST', body: JSON.stringify({ product_id, quantity, has_power }) }),
  update: (itemId: number, data: { quantity?: number; has_power?: boolean }) =>
    request<CartItem>(`/cart/${itemId}`, { method: 'PATCH', body: JSON.stringify(data) }),
  remove: (itemId: number) =>
    request<void>(`/cart/${itemId}`, { method: 'DELETE' }),
};

// Wishlist
export const wishlistApi = {
  list: () => request<WishlistItem[]>('/wishlist'),
  add: (product_id: number) =>
    request<WishlistItem>('/wishlist', { method: 'POST', body: JSON.stringify({ product_id }) }),
  remove: (product_id: number) =>
    request<void>(`/wishlist/${product_id}`, { method: 'DELETE' }),
};

// Addresses
export const addressesApi = {
  list: () => request<Address[]>('/addresses'),
  create: (data: Omit<Address, 'id' | 'user_id'>) =>
    request<Address>('/addresses', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: Omit<Address, 'id' | 'user_id'>) =>
    request<Address>(`/addresses/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  remove: (id: number) =>
    request<void>(`/addresses/${id}`, { method: 'DELETE' }),
};

// Orders
export const ordersApi = {
  create: (address_id: number) =>
    request<Order>('/orders', { method: 'POST', body: JSON.stringify({ address_id }) }),
  list: () => request<Order[]>('/orders'),
  get: (id: number) => request<Order>(`/orders/${id}`),
};
