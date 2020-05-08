from flask import Flask, Blueprint, jsonify, make_response, request
from data import db_session
from data.Musicians import Musician
from data.products import Product

app = Flask(__name__)
blueprint = Blueprint('product_api', __name__,
                            template_folder='templates')

@blueprint.route('/api/products')
def get_products():
    session = db_session.create_session()
    products = session.query(Product).all()
    return jsonify(
        {
            'products':
                [item.to_dict(only=('name', 'musician.id', 'description', 'price', 'year', 'is_lp', 'photo', 'views'))
                 for item in products]
        }
    )


@blueprint.route('/api/product/<int:product_id>',  methods=['GET'])
def get_one_product(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if not product:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'products': product.to_dict(only=('name', 'musician.id', 'description', 'price', 'year', 'is_lp', 'photo', 'views'))
        }
    )


# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)