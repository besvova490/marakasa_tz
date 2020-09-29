from app import app, db, models


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Review': models.Review, 'Product': models.Product}


if __name__ == '__main__':
    app.run(debug=True)
