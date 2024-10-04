from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import asc
from .models import User, Role, Item, Cart, Category, Brand, Order
from sqlalchemy.sql import func
from . import db
import uuid

admin = Blueprint("admin", __name__)

@admin.route("/admin")
def admin_dashboard():
    order = Order.query.order_by(Order.date_created.desc()).all()
    return render_template('admin.html', user=current_user, order=order)

@admin.route("/products", methods=["GET", "POST"])
def products():
    if request.method == "POST":
        part_name = request.form.get('partName')
        part_number = request.form.get('partNumber')
        compatibility = request.form.get('compatibility')
        description = request.form.get('description')
        condition = request.form.get('condition')
        warranty = request.form.get('warranty')
        price = request.form.get('price')
        discount = request.form.get('discount')
        stock_quantity = request.form.get('stockQuantity')
        availability_status = request.form.get('availabilityStatus')
        category_id = request.form.get('category')
        brand_id = request.form.get('brand')
        img = str(uuid.uuid4())
        img_x = str(uuid.uuid4())
        image = request.files.get('image')
        image_x = request.files.get('secondaryImage')
        image_filename = f'website/static/products/{img}.jpg'
        image_x_filename = f'website/static/products/{img_x}.jpg'
        if not part_name:
            flash('Part Name cannot be empty', category='error')
        elif not part_number:
            flash('Part Number cannot be empty', category='error')
        elif not description:
            flash('Description cannot be empty', category='error')
        elif not compatibility:
            flash('Compatibility cannot be empty', category='error')
        elif not condition:
            flash('Condition cannot be empty', category='error')
        elif not warranty:
            flash('Warranty cannot be empty', category='error')
        elif not category_id:
            flash('Category cannot be empty', category='error')
        elif not brand_id:
            flash('Brand cannot be empty', category='error')
        elif not price:
            flash('Price cannot be empty', category='error')
        elif not stock_quantity:
            flash('Stock Quantity cannot be empty', category='error')
        elif not availability_status:
            flash('Availability Status cannot be empty', category='error')
        elif not image:
            flash('At least one primary image is required', category='error')
        elif not image_x:
            flash('At least one secondary image is required', category='error')
        else:
            image.save(image_filename)
            image_x.save(image_x_filename)
            category = Category.query.get(category_id)
            brand = Brand.query.get(brand_id)
            if not category:
                flash('Invalid category selected', category='error')
                return redirect(url_for('admin.products'))
            if not brand:
                flash('Invalid brand selected', category='error')
                return redirect(url_for('admin.products'))
        
            new_item = Item(
                part_name=part_name,
                part_number=part_number,
                description=description,
                compatibility=compatibility,
                condition=condition,
                warranty=warranty,
                price=price,
                discount=discount,
                stock_quantity=stock_quantity,
                availability_status=availability_status,
                category=category,
                brand=brand,
                image=image_filename,
                secondary_image=image_x_filename
            )
            db.session.add(new_item)
            db.session.commit()
            flash('Added new product!', category='success')
            return redirect(url_for('admin.products'))
    brand = Brand.query.all()
    category = Category.query.all()
    item = Item.query.all()

    return render_template('products.html', category=category, brand=brand, item=item, user=current_user)

@admin.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    item = Item.query.filter_by(id=id).first()

    if request.method == "POST":
        part_name = request.form.get('editPartName')
        part_number = request.form.get('editPartNumber')
        compatibility = request.form.get('editCompatibility')
        description = request.form.get('editDescription')
        condition = request.form.get('editCondition')
        warranty = request.form.get('editWarranty')
        price = request.form.get('editPrice')
        discount = request.form.get('editDiscount')
        stock_quantity = request.form.get('editStockQuantity')
        availability_status = request.form.get('editAvailabilityStatus')
        category_id = request.form.get('editCategory')
        brand_id = request.form.get('editBrand')

        if not part_name or not price:
            flash('Part name and price are required!', category='error')
            return redirect(url_for('admin.edit', id=id))

        item.part_name = part_name
        item.part_number = part_number
        item.compatibility = compatibility
        item.description = description
        item.condition = condition
        item.warranty = warranty
        item.price = price
        item.discount = discount
        item.stock_quantity = stock_quantity
        item.availability_status = availability_status
        item.category_id = category_id
        item.brand_id = brand_id

        db.session.commit()
        flash('Product updated successfully!', category='success')

        return redirect(url_for('admin.products'))

    return redirect(url_for('admin.products'))

@admin.route("/delete/<id>")
def delete(id):
    item = Item.query.filter_by(id=id).first()

    if not item:
        flash("Item does not exist.", category='error')
    else:
        db.session.delete(item)
        db.session.commit()
        flash('item deleted.', category='success')

    return redirect(url_for('admin.products'))

@admin.route("/user")
def user():
    user = User.query.order_by(asc(User.date_created)).all()
    role = Role.query.all()
    return render_template('user.html', users=user, role=role, user=current_user)

@admin.route("/new_role", methods=['GET', 'POST'])
def new_role():
    if request.method == "POST":
        role_name = request.form.get('roleName')
        if not role_name:
            flash('Role name cannot be empty', category='error')
        else:
            role = Role(role_name=role_name)
            db.session.add(role)
            db.session.commit()
            flash('Role and permissions created!', category='success')
            return redirect(url_for('admin.user'))

@admin.route("/orders", methods=['GET', 'POST'])
@login_required
def orders():
    order = Order.query.all()
    buyer = Order.query
    print(buyer)
    return render_template('orders.html', user=current_user, order = order)

@admin.route("/order", methods=['GET', 'POST'])
@login_required
def order():    
    search = request.args.get("orderId")
    print(search)
    if search:
        order = Order.query.filter(Order.order.like(search)).all()
        print(order)

    return render_template('order.html', user=current_user)

@admin.route("/update/<order>", methods=['GET', 'POST'])
@login_required
def update(order):
    order = Order.query.filter_by(order=order).first()
    
    if request.method == "POST":
        status = request.form.get('status')
        if status:
            order.status = status
            db.session.commit()
            flash('Order updated successfully!', category='success')
            
    return redirect(url_for('admin.orders'))