// Shared TypeScript types for the Opticals app

export interface Category {
  id: number;
  name: string;
  slug: string;
}

export interface ProductImage {
  id: number;
  image_url: string;
  is_primary: number;
}

export interface Product {
  id: number;
  category_id: number;
  name: string;
  slug: string;
  brand: string;
  description: string | null;
  price: number;
  discount_price: number | null;
  gender: string | null;
  frame_shape: string | null;
  frame_type: string | null;
  frame_material: string | null;
  color: string | null;
  stock_quantity: number;
  rating_avg: number;
  promo_tag: string | null;
  created_at: string;
  images: ProductImage[];
  category: Category | null;
}

export interface ProductListResponse {
  products: Product[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface User {
  id: number;
  name: string;
  email: string;
  phone: string | null;
  created_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  user: User;
}

export interface CartProduct {
  id: number;
  name: string;
  slug: string;
  brand: string;
  price: number;
  discount_price: number | null;
  color: string | null;
  image_url: string | null;
}

export interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  has_power: boolean;
  created_at: string;
  product: CartProduct | null;
}

export interface WishlistItem {
  id: number;
  product_id: number;
  product: CartProduct | null;
}

export interface Address {
  id: number;
  user_id: number;
  full_name: string;
  phone: string;
  address_line1: string;
  address_line2: string | null;
  city: string;
  state: string;
  pincode: string;
  is_default: boolean;
}

export interface OrderItem {
  id: number;
  product_id: number;
  quantity: number;
  price_at_purchase: number;
  product_name: string | null;
  product_image: string | null;
}

export interface Order {
  id: number;
  user_id: number;
  address_id: number;
  status: string;
  payment_method: string;
  total_amount: number;
  created_at: string;
  items: OrderItem[];
  address: Address | null;
}

export interface Review {
  id: number;
  product_id: number;
  user_id: number;
  rating: number;
  comment: string | null;
  created_at: string;
  user_name: string | null;
}

export interface ProductFilters {
  category?: string;
  brand?: string;
  min_price?: number;
  max_price?: number;
  frame_shape?: string;
  gender?: string;
  frame_type?: string;
  sort?: string;
  page?: number;
  page_size?: number;
}
