import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Product(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'products'
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    musician_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("musicians.id"))
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    is_lp = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    photo = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("product_photo.product_id"))
    musician = orm.relation('Musician')
    cart_product = orm.relation('Cart_Product', back_populates='product')
    product_photo = orm.relation('Product_Photo')
