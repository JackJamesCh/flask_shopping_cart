from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def home():
    # Render an HTML template called 'index.html'
    return render_template('index.html')

@app.route('/shop')
def shop():
    # Render an HTML template called 'shop'
    return render_template('shop.html')

@app.route('/about')
def about():
    # Render an HTML template called 'shop'
    return render_template('about.html')

@app.route('/mycart')
def mycart():
    # Render an HTML template called 'shop'
    return render_template('mycart.html')

@app.route('/api/get-products')
def get_products():
    # Load data from products.json
    try:
        with open('products.json', 'r') as file:
            products = json.load(file)  # Parse the JSON file into a Python object
        return jsonify(products)  # Return the data as a JSON response
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500

@app.route('/api/get-featured-products')
def get_featured_products():
    # Load data from products.json
    try:
        with open('products.json', 'r') as file:
            products = json.load(file)  # Parse the JSON file into a Python object

        # Filter products to get only featured products
        featured_products = [product for product in products if product.get('featured')]

        return jsonify(featured_products)  # Return the featured products as a JSON response

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500


@app.route('/api/get-mycart')
def get_mycart():
    # Load data from products.json
    try:
        with open('mycart.json', 'r') as file:
            mycart = json.load(file)  # Parse the JSON file into a Python object
        return jsonify(mycart)  # Return the data as a JSON response
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500


if __name__ == '__main__':
    app.run(debug=True)