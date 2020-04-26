import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase


class Song(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'sounds'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    album_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id"))
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    product = orm.relation('Product')
