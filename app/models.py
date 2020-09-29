from app import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String, unique=True)
    title = db.Column(db.String)
    reviews = db.relationship(
        "Review", backref="product",
        lazy='dynamic', cascade="all, delete"
    )

    def __init__(self, asin, title):
        self.asin = asin
        self.title = title

    def __repr__(self):
        return f'<Product: {self.asin}>'

    def to_dict(self):
        return {'id': self.id, 'asin': self.asin, 'title': self.title}


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String)
    title = db.Column(db.String)
    review = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    def __init__(self, asin, title, review, product, product_id):
        self.asin = asin
        self.title = title
        self.review = review
        self.product = product
        self.product_id = product_id

    def __repr__(self):
        return f'<Review: {self.asin}>'

    def to_dict(self):
        return {
            'id': self.id, 'asin': self.asin, 'title': self.title,
            'review': self.review
        }
