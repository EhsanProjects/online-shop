from flask import Blueprint, render_template, request, session, redirect, abort, url_for,flash
import config

from extensions import db
from models.cart import Cart
from models.product import Product

app = Blueprint("admin", __name__)


@app.before_request
def before_request():
    # print(request.endpoint)
    if session.get('admin_login', None) is None and request.endpoint != "admin.login":
        abort(403)


@app.route('/admin/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)

        if username == config.ADMIN_USERNAME and password == config.ADMIN_PASSWORD:
            session['admin_login'] = username
            return redirect("/admin/dashboard")
        else:
            return redirect("/admin/login")
    else:
        return render_template("/admin/login.html")


@app.route('/admin/dashboard', methods=["GET"])
def dashboard():
    # carts = Cart.query.filter(Cart.status != "pending").all()
    carts = Cart.query.all()

    return render_template("admin/dashboard.html", carts=carts)


@app.route('/admin/dashboard/order/<id>', methods=["GET", "POST"])
def order(id):
    cart = Cart.query.filter(Cart.id == id).first_or_404()
    if request.method == "GET":

        return render_template("admin/order.html", cart=cart)
    else:
        status = request.form.get('status')
        cart.status = status
        db.session.commit()
        flash("Status is updated successfully")
        return redirect(url_for('admin.order', id=id))


@app.route('/admin/dashboard/products', methods=["GET", "POST"])
def products():
    if request.method == "GET":
        products = Product.query.all()
        return render_template("admin/products.html", products=products)
    else:
        name = request.form.get('name', None)
        description = request.form.get('description', None)
        price = request.form.get('price', None)
        active = request.form.get('active', None)
        file = request.files.get('cover', None)
        p = Product(name=name.title(), description=description.title(), price=price, active=active)
        if active == None:
            p.active = 0
        else:
            p.active = 1
        db.session.add(p)
        db.session.commit()
        file.save(f'static/cover/{p.id}.jpg')
        flash("New product is Added")
        return "Product Added. Done"


@app.route('/admin/dashboard/edit-product/<id>', methods=["GET", "POST"])
def edit_product(id):
    product = Product.query.filter(Product.id == id).first_or_404()
    if request.method == "GET":

        return render_template("admin/edit-product.html", product=product)
    else:
        name = request.form.get('name', None)
        description = request.form.get('description', None)
        price = request.form.get('price', None)
        active = request.form.get('active', None)
        file = request.files.get('cover', None)
        # p = Product(name=name.title(), description=description.title(), price=price, active=active)
        product.name = name
        product.description = description
        product.price = price

        if active == None:
            product.active = 0
        else:
            product.active = 1
        db.session.commit()
        if file.filename != "":
            file.save(f'static/cover/{product.id}.jpg')
        flash("Product is Edited")
        return redirect(url_for("admin.edit_product", id=id))
