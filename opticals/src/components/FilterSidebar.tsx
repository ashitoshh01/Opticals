'use client';

interface Props {
  filters: {
    brand?: string;
    gender?: string;
    frame_shape?: string;
    frame_type?: string;
    min_price?: number;
    max_price?: number;
  };
  onChange: (filters: Props['filters']) => void;
}

const BRANDS = ['Vincent Chase', 'Lenskart Air', 'John Jacobs', 'Lenskart Blu', 'Lenskart Studio', 'Lenskart Junior', 'Aqualens', 'Lenskart Hustlr', 'Lenskart Active', 'Vincent Chase Kids'];
const GENDERS = ['men', 'women', 'unisex', 'kids'];
const SHAPES = ['round', 'rectangle', 'aviator', 'cat-eye', 'wayfarer'];
const TYPES = ['full-rim', 'half-rim', 'rimless'];
const PRICE_RANGES = [
  { label: 'Under ₹1000', min: 0, max: 999 },
  { label: '₹1000 - ₹2000', min: 1000, max: 2000 },
  { label: '₹2000 - ₹3000', min: 2000, max: 3000 },
  { label: 'Above ₹3000', min: 3000, max: undefined },
];

export default function FilterSidebar({ filters, onChange }: Props) {
  const setFilter = (key: string, value: string | number | undefined) => {
    onChange({ ...filters, [key]: value });
  };

  const clearFilters = () => {
    onChange({});
  };

  const hasFilters = Object.values(filters).some(v => v !== undefined && v !== '');

  return (
    <aside className="filter-sidebar">
      <div className="filter-header">
        <h3>Filters</h3>
        {hasFilters && (
          <button onClick={clearFilters} className="clear-filters-btn">Clear All</button>
        )}
      </div>

      {/* Gender */}
      <div className="filter-section">
        <h4>Gender</h4>
        <div className="filter-options">
          {GENDERS.map(g => (
            <button
              key={g}
              className={`filter-chip ${filters.gender === g ? 'active' : ''}`}
              onClick={() => setFilter('gender', filters.gender === g ? undefined : g)}
            >
              {g.charAt(0).toUpperCase() + g.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Frame Shape */}
      <div className="filter-section">
        <h4>Frame Shape</h4>
        <div className="filter-options">
          {SHAPES.map(s => (
            <button
              key={s}
              className={`filter-chip ${filters.frame_shape === s ? 'active' : ''}`}
              onClick={() => setFilter('frame_shape', filters.frame_shape === s ? undefined : s)}
            >
              {s.charAt(0).toUpperCase() + s.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Frame Type */}
      <div className="filter-section">
        <h4>Frame Type</h4>
        <div className="filter-options">
          {TYPES.map(t => (
            <button
              key={t}
              className={`filter-chip ${filters.frame_type === t ? 'active' : ''}`}
              onClick={() => setFilter('frame_type', filters.frame_type === t ? undefined : t)}
            >
              {t.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Price Range */}
      <div className="filter-section">
        <h4>Price Range</h4>
        <div className="filter-options filter-options-col">
          {PRICE_RANGES.map(r => {
            const isActive = filters.min_price === r.min && filters.max_price === r.max;
            return (
              <button
                key={r.label}
                className={`filter-chip ${isActive ? 'active' : ''}`}
                onClick={() => {
                  if (isActive) {
                    setFilter('min_price', undefined);
                    onChange({ ...filters, min_price: undefined, max_price: undefined });
                  } else {
                    onChange({ ...filters, min_price: r.min, max_price: r.max });
                  }
                }}
              >
                {r.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* Brand */}
      <div className="filter-section">
        <h4>Brand</h4>
        <div className="filter-options filter-options-col">
          {BRANDS.slice(0, 6).map(b => (
            <button
              key={b}
              className={`filter-chip ${filters.brand === b ? 'active' : ''}`}
              onClick={() => setFilter('brand', filters.brand === b ? undefined : b)}
            >
              {b}
            </button>
          ))}
        </div>
      </div>
    </aside>
  );
}
