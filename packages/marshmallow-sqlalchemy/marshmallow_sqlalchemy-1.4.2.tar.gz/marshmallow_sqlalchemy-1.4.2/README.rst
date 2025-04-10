**********************
marshmallow-sqlalchemy
**********************

|pypi-package| |build-status| |docs| |marshmallow-support|

Homepage: https://marshmallow-sqlalchemy.readthedocs.io/

`SQLAlchemy <http://www.sqlalchemy.org/>`_ integration with the  `marshmallow <https://marshmallow.readthedocs.io/en/latest/>`_ (de)serialization library.


Declare your models
===================

.. code-block:: python

    import sqlalchemy as sa
    from sqlalchemy.orm import (
        DeclarativeBase,
        backref,
        relationship,
        sessionmaker,
    )

    from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

    engine = sa.create_engine("sqlite:///:memory:")
    Session = sessionmaker(engine)


    class Base(DeclarativeBase):
        pass


    class Author(Base):
        __tablename__ = "authors"
        id = sa.Column(sa.Integer, primary_key=True)
        name = sa.Column(sa.String, nullable=False)

        def __repr__(self):
            return f"<Author(name={self.name!r})>"


    class Book(Base):
        __tablename__ = "books"
        id = sa.Column(sa.Integer, primary_key=True)
        title = sa.Column(sa.String)
        author_id = sa.Column(sa.Integer, sa.ForeignKey("authors.id"))
        author = relationship("Author", backref=backref("books"))


    Base.metadata.create_all(engine)

.. start elevator-pitch

Generate marshmallow schemas
============================

.. code-block:: python

    from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field


    class AuthorSchema(SQLAlchemySchema):
        class Meta:
            model = Author
            load_instance = True  # Optional: deserialize to model instances

        id = auto_field()
        name = auto_field()
        books = auto_field()


    class BookSchema(SQLAlchemySchema):
        class Meta:
            model = Book
            load_instance = True

        id = auto_field()
        title = auto_field()
        author_id = auto_field()

You can automatically generate fields for a model's columns using `SQLAlchemyAutoSchema`.
The following schema classes are equivalent to the above.

.. code-block:: python

    from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


    class AuthorSchema(SQLAlchemyAutoSchema):
        class Meta:
            model = Author
            include_relationships = True
            load_instance = True


    class BookSchema(SQLAlchemyAutoSchema):
        class Meta:
            model = Book
            include_fk = True
            load_instance = True


Make sure to declare `Models` before instantiating `Schemas`. Otherwise `sqlalchemy.orm.configure_mappers() <https://docs.sqlalchemy.org/en/latest/orm/mapping_api.html>`_ will run too soon and fail.

(De)serialize your data
=======================

.. code-block:: python

    author = Author(name="Chuck Paluhniuk")
    author_schema = AuthorSchema()
    book = Book(title="Fight Club", author=author)

    with Session() as session:
        session.add(author)
        session.add(book)
        session.commit()

        dump_data = author_schema.dump(author)
        print(dump_data)
        # {'id': 1, 'name': 'Chuck Paluhniuk', 'books': [1]}

    with Session() as session:
        load_data = author_schema.load(dump_data, session=session)
        print(load_data)
        # <Author(name='Chuck Paluhniuk')>

Get it now
==========

.. code-block:: shell-session

   $ pip install -U marshmallow-sqlalchemy


Requires Python >= 3.9, marshmallow >= 3.18.0, and SQLAlchemy >= 1.4.40.

.. end elevator-pitch

Documentation
=============

Documentation is available at https://marshmallow-sqlalchemy.readthedocs.io/ .

Project links
=============

- Docs: https://marshmallow-sqlalchemy.readthedocs.io/
- Changelog: https://marshmallow-sqlalchemy.readthedocs.io/en/latest/changelog.html
- Contributing Guidelines: https://marshmallow-sqlalchemy.readthedocs.io/en/latest/contributing.html
- PyPI: https://pypi.python.org/pypi/marshmallow-sqlalchemy
- Issues: https://github.com/marshmallow-code/marshmallow-sqlalchemy/issues

License
=======

MIT licensed. See the bundled `LICENSE <https://github.com/marshmallow-code/marshmallow-sqlalchemy/blob/dev/LICENSE>`_ file for more details.


.. |pypi-package| image:: https://badgen.net/pypi/v/marshmallow-sqlalchemy
    :target: https://pypi.org/project/marshmallow-sqlalchemy/
    :alt: Latest version
.. |build-status| image:: https://github.com/marshmallow-code/marshmallow-sqlalchemy/actions/workflows/build-release.yml/badge.svg
    :target: https://github.com/marshmallow-code/marshmallow-sqlalchemy/actions/workflows/build-release.yml
    :alt: Build status
.. |docs| image:: https://readthedocs.org/projects/marshmallow-sqlalchemy/badge/
   :target: http://marshmallow-sqlalchemy.readthedocs.io/
   :alt: Documentation
.. |marshmallow-support| image:: https://badgen.net/badge/marshmallow/3,4?list=1
    :target: https://marshmallow.readthedocs.io/en/latest/upgrading.html
    :alt: marshmallow 3|4 compatible
