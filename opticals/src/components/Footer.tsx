import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-inner">
        <div className="footer-grid">
          <div className="footer-col">
            <div className="footer-brand">
              <span className="logo-icon">◎</span>
              <span className="logo-text">OPTICALS</span>
            </div>
            <p className="footer-tagline">Premium eyewear for every style. Trusted by millions across India.</p>
          </div>
          <div className="footer-col">
            <h4>Shop</h4>
            <Link href="/products/eyeglasses">Eyeglasses</Link>
            <Link href="/products/sunglasses">Sunglasses</Link>
            <Link href="/products/contact-lenses">Contact Lenses</Link>
            <Link href="/products/kids-glasses">Kids Glasses</Link>
          </div>
          <div className="footer-col">
            <h4>Account</h4>
            <Link href="/account">My Account</Link>
            <Link href="/account/orders">Orders</Link>
            <Link href="/account/wishlist">Wishlist</Link>
            <Link href="/cart">Cart</Link>
          </div>
          <div className="footer-col">
            <h4>Support</h4>
            <span>help@opticals.in</span>
            <span>1800-000-0000</span>
            <span>Mon-Sat, 10am-7pm</span>
          </div>
        </div>
        <div className="footer-bottom">
          <p>&copy; 2026 Opticals. All rights reserved. This is a prototype clone.</p>
        </div>
      </div>
    </footer>
  );
}
