# DRIP — Fashion Shopping App 🛍️
### Flask-based Online Clothing Store (Myntra-style)
College Major Project | Python + Flask + Jinja2

---

## 🚀 Run karne ka tarika

```bash
# 1. Install dependencies
pip install flask

# 2. Project folder mein jao
cd fashionstore

# 3. App run karo
python app.py

# 4. Browser mein kholein
# http://127.0.0.1:5000
```

---

## 📁 Project Structure

```
fashionstore/
├── app.py                    ← Main Flask application
├── requirements.txt          ← Dependencies
└── templates/
    ├── base.html             ← Navbar + Footer layout
    ├── index.html            ← Homepage (hero, featured products)
    ├── products.html         ← Product listing with filters
    ├── product_detail.html   ← Product page (size picker, add to cart)
    ├── cart.html             ← Shopping cart (qty update, remove)
    ├── checkout.html         ← Checkout form (address + payment)
    ├── order_success.html    ← Order confirmation page
    └── wishlist.html         ← Saved/wishlist items
```

---

## ✨ Features

| Feature | Description |
|---|---|
| 🏠 Homepage | Hero banner, featured products, category strips |
| 🛍 Product Listing | Filter by category/sub-category, sort by price/rating/discount |
| 🔍 Search | Search by product name or brand |
| 📋 Product Detail | Image, size selector, add to cart, wishlist |
| 🛒 Shopping Cart | Add/remove items, update quantity, price breakdown |
| 💳 Checkout | Address form, payment method selection |
| ❤️ Wishlist | Save & manage favorite items |
| ✅ Order Confirmation | Success page with order ID |
| 🎨 Myntra-like UI | Dark navbar, product cards, flash messages |

---

## 🛠 Tech Stack

- **Backend:** Python 3 + Flask
- **Frontend:** Jinja2 HTML templates + CSS3 + Vanilla JS
- **Session:** Flask session (cart & wishlist)
- **Fonts:** Google Fonts (Bebas Neue, DM Sans, DM Serif Display)
- **Icons:** Font Awesome 6

---

## 📝 Notes for Viva/Presentation

- Products data is stored as a Python list (no database needed)
- Cart uses Flask session (stored in browser cookies)
- For production: replace with SQLite/PostgreSQL + user authentication
- Payment is simulated (no real gateway integration)
