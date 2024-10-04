from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import asc
from .models import User, Role, Item, Cart, Category, Brand, Order
from .cart import get_cart_count
from sqlalchemy.sql import func
from . import db
import uuid
import random

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    item = Item.query.all()
    cart_count = get_cart_count(current_user)
    return render_template('index.html', item=item, user=current_user, cart_count = cart_count)

@views.route("/track-order")
def track():
    cart_count = get_cart_count(current_user)
    return render_template('tracker.html', user=current_user, cart_count = cart_count)

@views.route("/compare")
def compare():
    cart_count = get_cart_count(current_user)
    return render_template('compare.html', user=current_user, cart_count=cart_count)

@views.route("/category", methods=["GET", "POST"])
def category():
    if request.method == "POST":
        categoryName = request.form.get('categoryName')
        print(categoryName)
        
        if not categoryName:
            flash('Category Name cannot be empty', category='error')
        else:
                new_cat = Category(name = categoryName)
                db.session.add(new_cat)
                db.session.commit()
                flash('Added new category!', category='success')
                return redirect(url_for('admin.products'))
            
    category = Category.query.all()
    cart_count = get_cart_count(current_user)
    return render_template('category.html', category = category, user=current_user, cart_count = cart_count)


@views.route("/category/<category>")
def category_page(category):
    item = Item.query.filter_by(category_id=category).all()
    cart_count = get_cart_count(current_user)
    return render_template('category_page.html', user=current_user, item=item, cart_count = cart_count)

@views.route("/brand", methods=["GET", "POST"])
def brand():
    if request.method == "POST":
        brandName = request.form.get('brandName')
        print(brandName)
        
        if not brandName:
            flash('Brand Name cannot be empty', category='error')
        else:
                new_bar = Brand(name = brandName)
                db.session.add(new_bar)
                db.session.commit()
                flash('Added new category!', category='success')
                return redirect(url_for('admin.products'))

@views.route("/flash-sales")
def sales():
    cart_count = get_cart_count(current_user)
    return render_template('sales.html', user=current_user, cart_count=cart_count)

@views.route("/review")
def review():
    cart_count = get_cart_count(current_user)
    return render_template('review.html', user=current_user, cart_count = cart_count)

@views.route("/add-to-cart/<int:id>", methods=["GET", "POST"])
@login_required
def addToCart(id):
    product = Item.query.get_or_404(id)
    if request.method == "POST":
        quantity = request.form.get("quantity")
    cart_item = Cart(item_id=product.id, buyer_id=current_user.id, quantity = quantity)
    db.session.add(cart_item)
    db.session.commit()
    
    return redirect(url_for('views.home'))           

@views.route("/cart")
def cart():
    item = 0
    if current_user.is_authenticated:
        item= Cart.query.filter_by(buyer_id=current_user.id).all()
        cart_count = len(item)
    else:
        cart_count = 0
    return render_template('cart.html', user=current_user, cart_count=cart_count, item=item)
    


@views.route("/checkout", methods=["GET", "POST"])
def checkout():
    order = random.randint(10000,99999)
    total_price = db.session.query(db.func.sum(Item.price * Cart.quantity)).join(Cart, Cart.item_id == Item.id).filter(Cart.buyer_id == current_user.id).scalar()
    print(total_price)
    item_id = db.session.query(Cart.item_id).filter_by(buyer_id=current_user.id).scalar()
    print(item_id)
    
    orders = Order(order = order, 
                    buyer_id = current_user.id,
                    item_id = item_id,
                    total_price = total_price)
    db.session.add(orders)
    db.session.commit()
    
    cart_items = Cart.query.filter(Cart.buyer_id == current_user.id).all()
    print(cart_items)    
    for item in cart_items:
        db.session.delete(item)
        db.session.commit()
    return redirect(url_for('views.cart'))

@views.route("/search")
def search():
    cart_count = get_cart_count(current_user)
    
    search = request.args.get("search")
    
    if search:
        item = Item.query.filter(Item.part_name.like(search)).all()

    return render_template('list.html', user=current_user, cart_count =cart_count, item = item)

@views.route("/delete-cart/<id>")
def delete_cart(id):
    cart = Cart.query.filter_by(id=id).first()

    if not cart:
        flash("No item in cart.", category='error')
    else:
        db.session.delete(cart)
        db.session.commit()
        flash('Post deleted.', category='success')

    return redirect(url_for('views.cart'))