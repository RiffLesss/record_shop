from flask import Flask, render_template, request, make_response, session, redirect, abort
from data import db_session
from data.users import User
from data.products import Product
from data.songs import Song
from data.carts import Cart
from data.cart_product import Cart_Product
from data.reviews import Review
from data.RegisterForm import RegisterForm
from data.LoginForm import LoginForm
from data.ReviewsForm import ReviewsForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import datetime


app = Flask(__name__)
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/shop.db")
    session = db_session.create_session()

    @app.route("/")
    def index():
        session = db_session.create_session()
        products = session.query(Product)
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
            session.add(user)
            session.commit()
            return redirect('/login')
        return render_template('register.html', title='Registration', form=form)

    @app.route("/cookie_test")
    def cookie_test():
        visits_count = int(request.cookies.get("visits_count", 0))
        if visits_count:
            res = make_response(f"Вы пришли на эту страницу {visits_count + 1} раз")
            res.set_cookie("visits_count", str(visits_count + 1),
                           max_age=60 * 60 * 24 * 365 * 2)
        else:
            res = make_response(
                "Вы пришли на эту страницу в первый раз за последние 2 года")
            res.set_cookie("visits_count", '1',
                           max_age=60 * 60 * 24 * 365 * 2)
        return res

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
            session.query(User).filter(User.id == current_user.id).update({User.dark_theme: 0},
                                                                          synchronize_session=False)
        else:
            session.query(User).filter(User.id == current_user.id).update({User.dark_theme: 1},
                                                                          synchronize_session=False)
        session.commit()
        return redirect("/")

    @app.route('/product/<int:id>', methods=['GET', 'POST'])
    def product_page(id):
        form = ReviewsForm()
        product = session.query(Product).filter(Product.id == id).first()
        if form.validate_on_submit():
            review_session = db_session.create_session()
            review = Review()
            review.content = form.content.data
            review.product_id = id
            current_user.review.append(review)
            review_session.merge(current_user)
            review_session.commit()
        reviews = session.query(Review).filter(Review.product_id == id)
        if product.is_lp == 0:
            return render_template("product.html", product=product, form=form, reviews=reviews)
        else:
            songs = session.query(Song).filter(Song.album_id == product.id)
            return render_template("product.html", product=product, form=form, reviews=reviews, songs=songs)

    app.run()


if __name__ == '__main__':
    main()
