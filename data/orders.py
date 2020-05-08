import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Order(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'orders'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    cart_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("carts.id"))
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    phone = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    delivery = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    delivery_price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    country = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    town = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    street = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    house = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    flat = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    promo = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    cart = orm.relation('Cart')
