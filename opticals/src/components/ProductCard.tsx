'use client';
import Link from 'next/link';
import { Product } from '@/lib/types';

interface Props {
  product: Product;
}

export default function ProductCard({ product }: Props) {
  const primaryImage = product.images.find(i => i.is_primary) || product.images[0];
  const discount = product.discount_price
    ? Math.round(((product.price - product.discount_price) / product.price) * 100)
    : 0;
  const categorySlug = product.category?.slug || 'eyeglasses';

  return (
    <Link href={`/products/${categorySlug}/${product.slug}`} className="product-card">
      <div className="product-card-image-wrap">
        <img
          src={primaryImage?.image_url || 'https://placehold.co/400x300/222/FFC609?text=No+Image'}
          alt={product.name}
          className="product-card-image"
          loading="lazy"
        />
        {product.promo_tag && (
          <span className="promo-badge">{product.promo_tag}</span>
        )}
        {discount > 0 && (
          <span className="discount-badge">-{discount}%</span>
        )}
      </div>
      <div className="product-card-body">
        <p className="product-brand">{product.brand}</p>
        <h3 className="product-name">{product.name}</h3>
        <div className="product-price-row">
          {product.discount_price ? (
            <>
              <span className="price-current">₹{product.discount_price.toLocaleString()}</span>
              <span className="price-original">₹{product.price.toLocaleString()}</span>
            </>
          ) : (
            <span className="price-current">₹{product.price.toLocaleString()}</span>
          )}
        </div>
        <div className="product-meta">
          <span className="product-rating">★ {product.rating_avg.toFixed(1)}</span>
          {product.color && <span className="product-color">{product.color}</span>}
        </div>
      </div>
    </Link>
  );
}
