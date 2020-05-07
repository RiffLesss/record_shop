from flask import Flask, render_template, request, make_response, session, redirect, abort
from sqlalchemy import func
from data import db_session
from data.users import User
from data.RegisterForm import RegisterForm
from data.LoginForm import LoginForm
from data.products import Product
from data.carts import Cart
from data.Musicians import Musician
from data.cart_product import Cart_Product
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/shop.db")
    #app.run()
    session = db_session.create_session()

    @app.route("/")
    def index():
        session = db_session.create_session()
        products = session.query(Product).order_by(Product.views.desc())
        return render_template("index.html", products=products)

    @app.route("/TopSingles")
    def singles():
        session = db_session.create_session()
        products = session.query(Product).filter(Product.is_lp == False).order_by(Product.views.desc())
        return render_template("index.html", products=products)

    @app.route("/TopAlbums")
    def albums():
        session = db_session.create_session()
        products = session.query(Product).filter(Product.is_lp == True).order_by(Product.views.desc())
        return render_template("index.html", products=products)

    @app.route("/year/<int:year>")
    def year(year):
        session = db_session.create_session()
        products = session.query(Product).filter(Product.year == year).order_by(Product.views.desc())
        return render_template("index.html", products=products)

    @app.route("/musician/<name>")
    def musician(name):
        name = name.replace('%20', ' ')
        session = db_session.create_session()
        musician = session.query(Musician).filter(Musician.name == name).first()
        products = session.query(Product).filter(Product.musician_id == musician.id).order_by(Product.views.desc())
        return render_template("index.html", products=products)

    @app.route('/register', methods=['GET', 'POST'])
    def reqister():
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Registration',
                                       form=form,
                                       message="Passwords don't match")
            session = db_session.create_session()
            if session.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Registration',
                                       form=form,
                                       message="This user already exists")
            user = User(
                name=form.name.data,
                surname=form.surname.data,
                email=form.email.data,
            )
            user.set_password(form.password.data)
            user_cart = Cart(user_id=user.id)
            session.add(user)
            session.add(user_cart)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Registration', form=form)

    @app.route('/add_to_cart/<int:id>')
    @login_required
    def add_to_cart(id):
        product = session.query(Product).get(id)
        cart = session.query(Cart).filter(Cart.user_id == current_user.id).first()
        cart_product = Cart_Product(
            product_id=product.id,
            cart_id=cart.id,
            count=1,
            one_price=product.price,
            full_price=product.price
        )
        session.add(cart_product)
        session.commit()
        address = '/product/' + str(id)
        return redirect(address)

    @app.route('/delete/<int:id>', methods=['GET', 'POST'])
    @login_required
    def delete(id):
        session = db_session.create_session()
        cart_products = session.query(Cart_Product).filter(Cart_Product.id == id).first()
        if cart_products:
            session.delete(cart_products)
            session.commit()
        else:
            abort(404)
        return redirect('/cart')

    @app.route('/cart')
    def cart():
        empty_cart = False
        cart = session.query(Cart).get(current_user.id)
        cart_products = session.query(Cart_Product).filter(Cart_Product.cart_id == cart.id)
        product_count = session.query(func.sum(Cart_Product.count)).filter_by(cart_id=cart.id).scalar()
        full_price = session.query(func.sum(Cart_Product.full_price)).filter_by(cart_id=cart.id).scalar()
        if cart_products:
            empty_cart = True
        return render_template('cart.html', title='Cart', cart_products=cart_products,
                               product_count=product_count, full_price=full_price, empty_cart=empty_cart)

    @login_manager.user_loader
    def load_user(user_id):
        session = db_session.create_session()
        return session.query(User).get(user_id)

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            session = db_session.create_session()
            user = session.query(User).filter(User.email == form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect("/")
            return render_template('login.html',
                                   message="Wrong email or password",
                                   form=form)
        return render_template('login.html', title='Authorization', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect("/")

    @app.route('/changetheme')
    @login_required
    def change_theme():
        session = db_session.create_session()
        if current_user.dark_theme:
            session.query(User).filter(User.id == current_user. id).update({User.dark_theme: 0},
                                                                          synchronize_session=False)
        else:
            session.query(User).filter(User.id == current_user.id).update({User.dark_theme: 1},
                                                                          synchronize_session=False)
        session.commit()
        return redirect("/")

    @app.route('/changeform')
    @login_required
    def change_form():
        session = db_session.create_session()
        if current_user.circle_theme:
            session.query(User).filter(User.id == current_user.id).update({User.circle_theme: 0},
                                                                          synchronize_session=False)
        else:
            session.query(User).filter(User.id == current_user.id).update({User.circle_theme: 1},
                                                                          synchronize_session=False)
        session.commit()
        return redirect("/")

    @app.route("/count+/<int:id>")
    def plus_count(id):
        session.query(Cart_Product).filter(Cart_Product.id == id).\
            update({Cart_Product.count: Cart_Product.count + 1,
                    Cart_Product.full_price: Cart_Product.one_price * (Cart_Product.count + 1)})
        c_p = session.query(Cart_Product).filter(Cart_Product.id == id).first()
        full_price = round(c_p.full_price, 2)
        session.query(Cart_Product).filter(Cart_Product.id == id). \
            update({Cart_Product.full_price: full_price})
        session.commit()
        return redirect("/cart")

    @app.route("/count-/<int:id>")
    def minus_count(id):
        count = session.query(Cart_Product).get(id)
        if count.count > 1:
            session.query(Cart_Product).filter(Cart_Product.id == id). \
                update({Cart_Product.count: Cart_Product.count - 1,
                        Cart_Product.full_price: Cart_Product.one_price * (Cart_Product.count - 1)})
            c_p = session.query(Cart_Product).filter(Cart_Product.id == id).first()
            full_price = round(c_p.full_price, 2)
            session.query(Cart_Product).filter(Cart_Product.id == id). \
                update({Cart_Product.full_price: full_price})
            session.commit()
        return redirect("/cart")


    app.run()


if __name__ == '__main__':
    main()