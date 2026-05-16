-- Run this in your Supabase SQL Editor (https://supabase.com/dashboard → SQL Editor)

-- Products table
CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  price NUMERIC NOT NULL DEFAULT 0,
  badge TEXT DEFAULT '',
  description TEXT DEFAULT '',
  sizes JSONB DEFAULT '[]',
  stock INTEGER DEFAULT 0,
  featured BOOLEAN DEFAULT false,
  image TEXT DEFAULT '',
  sold_out BOOLEAN DEFAULT false,
  added_at BIGINT DEFAULT 0
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
  id TEXT PRIMARY KEY,
  product_id TEXT,
  product_name TEXT NOT NULL,
  size TEXT NOT NULL,
  qty INTEGER NOT NULL DEFAULT 1,
  price NUMERIC NOT NULL DEFAULT 0,
  total NUMERIC NOT NULL DEFAULT 0,
  customer_name TEXT NOT NULL,
  phone TEXT NOT NULL,
  address TEXT NOT NULL,
  note TEXT DEFAULT '',
  status TEXT DEFAULT 'active',
  placed_at BIGINT DEFAULT 0
);

-- Allow public access (anon key)
ALTER TABLE products ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public read products" ON products FOR SELECT USING (true);
CREATE POLICY "Public insert products" ON products FOR INSERT WITH CHECK (true);
CREATE POLICY "Public update products" ON products FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "Public delete products" ON products FOR DELETE USING (true);

CREATE POLICY "Public read orders" ON orders FOR SELECT USING (true);
CREATE POLICY "Public insert orders" ON orders FOR INSERT WITH CHECK (true);
CREATE POLICY "Public update orders" ON orders FOR UPDATE USING (true) WITH CHECK (true);
CREATE POLICY "Public delete orders" ON orders FOR DELETE USING (true);
