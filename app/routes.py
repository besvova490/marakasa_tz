from . import app, cache, db
from app import models
from flask import jsonify, request


@app.route('/products', methods=['GET'])
def products():
    products_list = \
        [product.to_dict() for product in models.Product.query.all()]
    return jsonify({'msg': 'All products', 'items': products_list}), 200


@app.route('/products/<int:product_id>', methods=['GET'])
@cache.cached(timeout=10)
def product_get(product_id):
    product = models.Product.query.get(product_id)
    if not product:
        return jsonify({'mas': 'Bad request'}), 400
    query = request.args
    page = query.get('page', 1, type=int)
    product_reviews = product.reviews.paginate(page=page, per_page=1).items
    product_reviews = [review.review for review in product_reviews]
    return jsonify({
        'msg': 'Product page', 'item': product.to_dict(), 'current_page': page,
        'review_pages': product.reviews.count(),
        'review': product_reviews,
    }), 200


@app.route('/products/<int:product_id>', methods=['PUT'])
def product_put(product_id):
    product = models.Product.query.get(product_id)
    review = request.json.get('review')
    if not product or not review:
        return jsonify({'mas': 'Bad request'}), 400
    new_review = models.Review(
        asin=product.asin, title=product.title, review=review,
        product=product, product_id=product_id
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'msg': f'New review for {product.title} created'}), 200
