from .db_session import create_session
from flask_restful import reqparse, abort, Api, Resource
from data.Musicians import Musician
from data.products import Product
from flask import jsonify

def abort_if_product_not_found(product_id):
    session = create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f"Product {product_id} not found")


class ProductResource(Resource):
    def get(self, product_id):
        abort_if_product_not_found(product_id)
        session = create_session()
        product = session.query(Product).get(product_id)
        return jsonify({'product': product.to_dict(
            only=('name', 'musician_id', 'description', 'price', 'year', 'is_lp', 'photo', 'views'))})

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('musician_id', required=True, type=int)
parser.add_argument('description', required=True)
parser.add_argument('price', required=True, type=int)
parser.add_argument('year', required=True, type=int)
parser.add_argument('is_lp', required=True, type=bool)
parser.add_argument('photo', required=True)
parser.add_argument('views', required=True, type=int)


class ProductListResource(Resource):
    def get(self):
        session = create_session()
        product = session.query(Product).all()
        return jsonify({'product': [item.to_dict(
            only=('name', 'musician.id', 'description', 'price', 'year', 'is_lp', 'photo', 'views')) for item in product]})
