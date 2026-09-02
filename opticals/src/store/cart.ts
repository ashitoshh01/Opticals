'use client';
import { create } from 'zustand';
import { CartItem } from '@/lib/types';
import { cartApi } from '@/lib/api';

interface CartState {
  items: CartItem[];
  loading: boolean;
  fetchCart: () => Promise<void>;
  addToCart: (productId: number, quantity?: number) => Promise<void>;
  updateItem: (itemId: number, quantity: number) => Promise<void>;
  removeItem: (itemId: number) => Promise<void>;
  clearLocal: () => void;
  totalItems: () => number;
  totalPrice: () => number;
}

export const useCartStore = create<CartState>((set, get) => ({
  items: [],
  loading: false,

  fetchCart: async () => {
    set({ loading: true });
    try {
      const items = await cartApi.list();
      set({ items, loading: false });
    } catch {
      set({ loading: false });
    }
  },

  addToCart: async (productId, quantity = 1) => {
    await cartApi.add(productId, quantity);
    await get().fetchCart();
  },

  updateItem: async (itemId, quantity) => {
    if (quantity <= 0) {
      await get().removeItem(itemId);
      return;
    }
    await cartApi.update(itemId, { quantity });
    await get().fetchCart();
  },

  removeItem: async (itemId) => {
    await cartApi.remove(itemId);
    set({ items: get().items.filter(i => i.id !== itemId) });
  },

  clearLocal: () => set({ items: [] }),

  totalItems: () => get().items.reduce((sum, i) => sum + i.quantity, 0),

  totalPrice: () =>
    get().items.reduce((sum, i) => {
      const price = i.product?.discount_price ?? i.product?.price ?? 0;
      return sum + price * i.quantity;
    }, 0),
}));
