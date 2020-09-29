import argparse
import csv
import sys
from app import db
from app.models import Product, Review
from sqlalchemy.exc import IntegrityError


def open_products(file_name):
    with open(file_name, 'r') as f:
        csv_reader = csv.DictReader(f)
        csv_products_list = [product_data for product_data in csv_reader]
    return csv_products_list


def open_reviews(file_name):
    with open(file_name, 'r') as f:
        csv_reader = csv.DictReader(f)
        csv_reviews_list = [reviews_data for reviews_data in csv_reader]
    return csv_reviews_list


def add_product_to_db(products_list):
    try:
        product_obj_list = []
        for product in products_list:
            product_obj_list.append(
                Product(asin=product['Asin'], title=product['Title']))
        db.session.bulk_save_objects(product_obj_list)
        db.session.commit()
        return {'msg': 'All products added'}
    except IntegrityError:
        return {'msg': 'some product from file already in db'}


def add_reviews_to_db(reviews_list):
    try:
        reviews_obj_list = []
        for review in reviews_list:
            product_review = Product.query.filter_by(
                asin=review['Asin']).first()
            reviews_obj_list.append(
                Review(asin=review['Asin'], title=review['Title'],
                       review=review['Review'], product=product_review,
                       product_id=product_review.id)
            )
        db.session.bulk_save_objects(reviews_obj_list)
        db.session.commit()
        return {'msg': 'All reviews added'}
    except IntegrityError:
        return {'msg': 'some review for file already in db'}


# 'products_data/Products - Лист1.csv'
# 'products_data/Reviews - Лист1.csv'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--products_file', '-p',
                        help='product file name for parse and save to db')
    parser.add_argument('--reviews_file', '-r',
                        help='reviews file name for parse and save to db')
    args = parser.parse_args()

    if args.products_file:
        products = open_products(args.products_file)
        add_product_to_db(products)
        sys.exit()
    elif args.reviews_file:
        reviews = open_reviews(args.reviews_file)
        add_reviews_to_db(reviews)
        sys.exit()
    else:
        print('Unknown command use help')
        sys.exit()
