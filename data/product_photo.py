import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Product_Photo(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'product_photo'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    product_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"))
    url = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    product_photo = orm.relation('Product')
