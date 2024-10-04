from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True)
    number = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False, default=3)
    role = db.relationship('Role', backref='users')
    carts = db.relationship('Cart', backref='buyer', lazy=True)
    orders = db.relationship('Order', backref='customer', lazy=True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)
    
class status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(255), nullable=False)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    part_name = db.Column(db.String(255), nullable=False)
    part_number = db.Column(db.String(255), nullable=False)
    compatibility = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    condition = db.Column(db.String(255), nullable=False)
    warranty = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    discount = db.Column(db.Numeric(precision=5, scale=2), nullable=True)
    stock_quantity = db.Column(db.Integer, nullable=False)
    availability_status = db.Column(db.String(50), nullable=False)
    image = db.Column(db.Text, nullable=True)
    secondary_image = db.Column(db.Text, nullable=True)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref='items')
    brand_id = db.Column(db.Integer, db.ForeignKey('brand.id'), nullable=False)
    brand = db.relationship('Brand', backref='items')

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'), nullable=False)
    item = db.relationship('Item', backref='cart_item')
    quantity = db.Column(db.String(255), nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False)
    order = db.Column(db.Integer, primary_key=True, unique=True, nullable=False)
    buyer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id', ondelete='CASCADE'), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="pending")
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    total_price = db.Column(db.Integer, nullable=False)
    buyer = db.relationship('User', backref='customer')
    item = db.relationship('Item', backref='ordered_item')

class Brand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)