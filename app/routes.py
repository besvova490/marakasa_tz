from . import app, cache, db
from app import models
from flask import jsonify, request


@app.route('/products', methods=['GET'])
def products():
    products_list = \
        [product.to_dict() for product in models.Product.query.all()]
    return jsonify({'msg': 'All products', 'items': products_list}), 200


@app.route('/products/<int:product_id>', methods=['GET'])
@cache.cached(timeout=15, query_string=True)
def product_get(product_id):
    product = models.Product.query.get(product_id)
    if not product:
        return jsonify({'mas': 'Bad request'}), 400
    query = request.args
    page = query.get('page', 1, type=int)
    per_page = query.get('per_page', 2, type=int)
    product_reviews_pages = product.reviews.paginate(page=page,
                                                     per_page=per_page)
    product_reviews = [{'title': review.title, 'review': review.review}
                       for review in product_reviews_pages.items]
    return jsonify({
        'msg': 'Product page', 'item': product.to_dict(),
        'current_page': product_reviews_pages.page,
        'pages': product_reviews_pages.pages,
        'review': product_reviews,
    }), 200


@app.route('/products/<int:product_id>', methods=['PUT'])
def product_put(product_id):
    product = models.Product.query.get(product_id)
    review = request.json.get('data')
    if not product or not review:
        return jsonify({'mas': 'Bad request'}), 400
    new_review = models.Review(
        asin=product.asin, title=review['title'], review=review['review'],
        product=product, product_id=product_id
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify({'msg': f'New review for {product.title} created'}), 200
