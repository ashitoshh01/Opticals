'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useState, useEffect } from 'react';
import { useAuthStore } from '@/store/auth';
import { useCartStore } from '@/store/cart';

const categories = [
  { name: 'Eyeglasses', slug: 'eyeglasses' },
  { name: 'Sunglasses', slug: 'sunglasses' },
  { name: 'Contact Lenses', slug: 'contact-lenses' },
  { name: 'Kids Glasses', slug: 'kids-glasses' },
];

export default function Navbar() {
  const router = useRouter();
  const { user, logout, loadUser } = useAuthStore();
  const { totalItems, fetchCart } = useCartStore();
  const [searchQ, setSearchQ] = useState('');
  const [menuOpen, setMenuOpen] = useState(false);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    loadUser();
  }, [loadUser]);

  useEffect(() => {
    if (user) fetchCart();
  }, [user, fetchCart]);

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQ.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQ.trim())}`);
      setSearchQ('');
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        {/* Logo */}
        <Link href="/" className="navbar-logo">
          <span className="logo-icon">◎</span>
          <span className="logo-text">OPTICALS</span>
        </Link>

        {/* Desktop Categories */}
        <div className="navbar-categories">
          {categories.map((cat) => (
            <Link key={cat.slug} href={`/products/${cat.slug}`} className="nav-category-link">
              {cat.name}
            </Link>
          ))}
        </div>

        {/* Search */}
        <form onSubmit={handleSearch} className="navbar-search">
          <svg className="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="text"
            placeholder="Search eyewear..."
            value={searchQ}
            onChange={(e) => setSearchQ(e.target.value)}
            className="search-input"
          />
        </form>

        {/* Right Actions */}
        <div className="navbar-actions">
          {mounted && user ? (
            <>
              <Link href="/account/wishlist" className="nav-action-btn" title="Wishlist">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="nav-icon">
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
                </svg>
              </Link>
              <Link href="/cart" className="nav-action-btn cart-btn" title="Cart">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="nav-icon">
                  <path d="M6 2L3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z" /><line x1="3" y1="6" x2="21" y2="6" /><path d="M16 10a4 4 0 0 1-8 0" />
                </svg>
                {totalItems() > 0 && <span className="cart-badge">{totalItems()}</span>}
              </Link>
              <div className="nav-user-menu">
                <Link href="/account" className="nav-action-btn" title="Account">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="nav-icon">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" /><circle cx="12" cy="7" r="4" />
                  </svg>
                </Link>
                <button onClick={logout} className="nav-logout-btn">Logout</button>
              </div>
            </>
          ) : (
            <Link href="/login" className="nav-login-btn">Sign In</Link>
          )}

          {/* Mobile menu toggle */}
          <button className="mobile-menu-btn" onClick={() => setMenuOpen(!menuOpen)}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="nav-icon">
              {menuOpen ? (
                <><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></>
              ) : (
                <><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="18" x2="21" y2="18" /></>
              )}
            </svg>
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {menuOpen && (
        <div className="mobile-menu">
          {categories.map((cat) => (
            <Link key={cat.slug} href={`/products/${cat.slug}`} className="mobile-menu-link" onClick={() => setMenuOpen(false)}>
              {cat.name}
            </Link>
          ))}
          <form onSubmit={handleSearch} className="mobile-search-form">
            <input
              type="text"
              placeholder="Search..."
              value={searchQ}
              onChange={(e) => setSearchQ(e.target.value)}
              className="mobile-search-input"
            />
          </form>
        </div>
      )}
    </nav>
  );
}
