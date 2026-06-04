from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import json

app = Flask(__name__)
app.secret_key = 'fashionstore_secret_2024'

# ─── Sample Product Data ───────────────────────────────────────────────────────
PRODUCTS = [
    {"id": 1,  "name": "Urban Slim Fit Jeans",      "brand": "Levi's",      "price": 1499, "original_price": 2999, "category": "men",   "sub": "jeans",   "image": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&q=80", "rating": 4.3, "reviews": 2340, "sizes": ["28","30","32","34","36"], "colors": ["Blue","Black","Grey"], "badge": "BESTSELLER"},
    {"id": 2,  "name": "Floral Wrap Dress",          "brand": "Zara",        "price": 1299, "original_price": 2499, "category": "women", "sub": "dresses", "image": "https://images.unsplash.com/photo-1496747611176-843222e1e57c?w=400&q=80", "rating": 4.5, "reviews": 1820, "sizes": ["XS","S","M","L","XL"], "colors": ["Pink","Blue","Green"], "badge": "NEW"},
    {"id": 3,  "name": "Classic White Oxford Shirt", "brand": "H&M",         "price": 899,  "original_price": 1599, "category": "men",   "sub": "shirts",  "image": "https://images.unsplash.com/photo-1598033129183-c4f50c736f10?w=400&q=80", "rating": 4.1, "reviews": 980,  "sizes": ["S","M","L","XL","XXL"], "colors": ["White","Blue","Pink"], "badge": ""},
    {"id": 4,  "name": "Boho Maxi Skirt",            "brand": "FabIndia",    "price": 1099, "original_price": 1999, "category": "women", "sub": "skirts",  "image": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=400&q=80", "rating": 4.4, "reviews": 650,  "sizes": ["XS","S","M","L","XL"], "colors": ["Orange","Red","Yellow"], "badge": "TRENDING"},
    {"id": 5,  "name": "Cargo Jogger Pants",         "brand": "Nike",        "price": 2199, "original_price": 3499, "category": "men",   "sub": "pants",   "image": "https://images.unsplash.com/photo-1607522370275-f14206abe5d3?w=400&q=80", "rating": 4.6, "reviews": 3210, "sizes": ["S","M","L","XL","XXL"], "colors": ["Black","Khaki","Grey"], "badge": "HOT"},
    {"id": 6,  "name": "Embroidered Kurti",          "brand": "Biba",        "price": 849,  "original_price": 1499, "category": "women", "sub": "kurtis",  "image": "https://images.unsplash.com/photo-1594938298603-c8148c4b4f35?w=400&q=80", "rating": 4.2, "reviews": 1450, "sizes": ["XS","S","M","L","XL"], "colors": ["Teal","Purple","Red"], "badge": ""},
    {"id": 7,  "name": "Oversized Graphic Tee",      "brand": "H&M",         "price": 599,  "original_price": 999,  "category": "men",   "sub": "tshirts", "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400&q=80", "rating": 4.0, "reviews": 560,  "sizes": ["S","M","L","XL","XXL"], "colors": ["White","Black","Red"], "badge": ""},
    {"id": 8,  "name": "Off-Shoulder Crop Top",      "brand": "Zara",        "price": 699,  "original_price": 1299, "category": "women", "sub": "tops",    "image": "https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=400&q=80", "rating": 4.3, "reviews": 890,  "sizes": ["XS","S","M","L"], "colors": ["White","Black","Pink"], "badge": "NEW"},
    {"id": 9,  "name": "Leather Biker Jacket",       "brand": "Roadster",    "price": 3499, "original_price": 5999, "category": "men",   "sub": "jackets", "image": "https://images.unsplash.com/photo-1551028719-00167b16eac5?w=400&q=80", "rating": 4.7, "reviews": 2100, "sizes": ["S","M","L","XL","XXL"], "colors": ["Black","Brown"], "badge": "BESTSELLER"},
    {"id": 10, "name": "Pleated Palazzo Pants",      "brand": "W",           "price": 1199, "original_price": 1999, "category": "women", "sub": "pants",   "image": "https://images.unsplash.com/photo-1509631179647-0177331693ae?w=400&q=80", "rating": 4.1, "reviews": 430,  "sizes": ["XS","S","M","L","XL"], "colors": ["Black","White","Navy"], "badge": ""},
    {"id": 11, "name": "Denim Trucker Jacket",       "brand": "Levi's",      "price": 2799, "original_price": 4499, "category": "men",   "sub": "jackets", "image": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400&q=80", "rating": 4.5, "reviews": 1760, "sizes": ["S","M","L","XL","XXL"], "colors": ["Blue","Black"], "badge": "TRENDING"},
    {"id": 12, "name": "Silk Satin Midi Dress",      "brand": "Mango",       "price": 2499, "original_price": 4299, "category": "women", "sub": "dresses", "image": "https://images.unsplash.com/photo-1539008835657-9e8e9680c956?w=400&q=80", "rating": 4.6, "reviews": 980,  "sizes": ["XS","S","M","L"], "colors": ["Cream","Rose","Black"], "badge": "LUXURY"},
]

def get_cart():
    return session.get('cart', {})

def save_cart(cart):
    session['cart'] = cart
    session.modified = True

def cart_count():
    cart = get_cart()
    return sum(item['qty'] for item in cart.values())

def cart_total():
    cart = get_cart()
    total = 0
    for key, item in cart.items():
        pid = int(key.split('_')[0])
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if product:
            total += product['price'] * item['qty']
    return total

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route('/')
def index():
    featured = PRODUCTS[:8]
    return render_template('index.html', products=featured,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/products')
def products():
    category = request.args.get('category', 'all')
    sub = request.args.get('sub', '')
    sort = request.args.get('sort', 'popular')
    search = request.args.get('q', '').lower()

    filtered = PRODUCTS
    if category != 'all':
        filtered = [p for p in filtered if p['category'] == category]
    if sub:
        filtered = [p for p in filtered if p['sub'] == sub]
    if search:
        filtered = [p for p in filtered if search in p['name'].lower() or search in p['brand'].lower()]

    if sort == 'price_low':
        filtered.sort(key=lambda x: x['price'])
    elif sort == 'price_high':
        filtered.sort(key=lambda x: x['price'], reverse=True)
    elif sort == 'rating':
        filtered.sort(key=lambda x: x['rating'], reverse=True)
    elif sort == 'discount':
        filtered.sort(key=lambda x: x['original_price'] - x['price'], reverse=True)

    return render_template('products.html', products=filtered, category=category,
                           sub=sub, sort=sort, search=search,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/product/<int:pid>')
def product_detail(pid):
    product = next((p for p in PRODUCTS if p['id'] == pid), None)
    if not product:
        flash('Product not found!', 'error')
        return redirect(url_for('products'))
    related = [p for p in PRODUCTS if p['category'] == product['category'] and p['id'] != pid][:4]
    return render_template('product_detail.html', product=product, related=related,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    pid = int(request.form.get('product_id'))
    size = request.form.get('size', 'M')
    qty = int(request.form.get('qty', 1))
    key = f"{pid}_{size}"

    cart = get_cart()
    if key in cart:
        cart[key]['qty'] += qty
    else:
        cart[key] = {'pid': pid, 'size': size, 'qty': qty}
    save_cart(cart)
    flash('Item added to cart! 🛍️', 'success')

    next_page = request.form.get('next', url_for('cart'))
    if next_page == 'stay':
        return redirect(url_for('product_detail', pid=pid))
    return redirect(url_for('cart'))

@app.route('/remove_from_cart/<key>')
def remove_from_cart(key):
    cart = get_cart()
    if key in cart:
        del cart[key]
        save_cart(cart)
        flash('Item removed from cart.', 'info')
    return redirect(url_for('cart'))

@app.route('/update_cart', methods=['POST'])
def update_cart():
    key = request.form.get('key')
    qty = int(request.form.get('qty', 1))
    cart = get_cart()
    if key in cart:
        if qty <= 0:
            del cart[key]
        else:
            cart[key]['qty'] = qty
        save_cart(cart)
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    cart = get_cart()
    cart_items = []
    subtotal = 0
    for key, item in cart.items():
        pid = item['pid']
        product = next((p for p in PRODUCTS if p['id'] == pid), None)
        if product:
            line_total = product['price'] * item['qty']
            subtotal += line_total
            cart_items.append({
                'key': key, 'product': product,
                'size': item['size'], 'qty': item['qty'],
                'line_total': line_total
            })
    discount = int(subtotal * 0.05) if subtotal > 1999 else 0
    delivery = 0 if subtotal >= 999 else 79
    total = subtotal - discount + delivery
    return render_template('cart.html', cart_items=cart_items, subtotal=subtotal,
                           discount=discount, delivery=delivery, total=total,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if not get_cart():
        flash('Your cart is empty!', 'error')
        return redirect(url_for('products'))
    if request.method == 'POST':
        # Simulate order placement
        session['cart'] = {}
        session.modified = True
        flash('🎉 Order placed successfully! Track it in My Orders.', 'success')
        return redirect(url_for('order_success'))
    cart = get_cart()
    subtotal = cart_total()
    discount = int(subtotal * 0.05) if subtotal > 1999 else 0
    delivery = 0 if subtotal >= 999 else 79
    total = subtotal - discount + delivery
    return render_template('checkout.html', subtotal=subtotal, discount=discount,
                           delivery=delivery, total=total,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/order-success')
def order_success():
    import random, string
    order_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return render_template('order_success.html', order_id=order_id, cart_count=0)

@app.route('/wishlist')
def wishlist():
    wishlist_ids = session.get('wishlist', [])
    wished = [p for p in PRODUCTS if p['id'] in wishlist_ids]
    return render_template('wishlist.html', products=wished,
                           cart_count=cart_count(), cart_total=cart_total())

@app.route('/toggle_wishlist/<int:pid>')
def toggle_wishlist(pid):
    wl = session.get('wishlist', [])
    if pid in wl:
        wl.remove(pid)
        flash('Removed from wishlist', 'info')
    else:
        wl.append(pid)
        flash('Added to wishlist ❤️', 'success')
    session['wishlist'] = wl
    session.modified = True
    return redirect(request.referrer or url_for('products'))

@app.context_processor
def inject_globals():
    return dict(wishlist_ids=session.get('wishlist', []))

if __name__ == '__main__':
    app.run(debug=True)
