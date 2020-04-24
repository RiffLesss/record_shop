import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Cart_Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'cart_product'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"))
    cart_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("carts.id"))
    count = sqlalchemy.Column(sqlalchemy.Integer, default=1, nullable=True)
    cart = orm.relation('Cart')
    product = orm.relation('Product')
