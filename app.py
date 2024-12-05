from flask import Flask, render_template, jsonify, request
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
    try:
        # Load data from mycart.json
        with open('mycart.json', 'r') as file:
            mycart = json.load(file)  # Parse the JSON file into a Python object

        # Aggregate products by name and calculate quantities
        aggregated_cart = {}
        for product in mycart:
            product_name = product.get("name")

            # Use the product name as the key to aggregate quantities
            if product_name in aggregated_cart:
                aggregated_cart[product_name]["quantity"] += 1
            else:
                # Add the product to the aggregated cart with a quantity of 1
                aggregated_cart[product_name] = {
                    "name": product_name,
                    "price": product.get("price"),
                    "quantity": 1
                }

        # Convert aggregated data to a list
        aggregated_cart_list = list(aggregated_cart.values())

        return jsonify(aggregated_cart_list)  # Return the aggregated cart as a JSON response

    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Error decoding JSON"}), 500


@app.route('/api/add-to-cart', methods=['POST'])
def add_to_cart():
    try:
        # Load existing cart data
        try:
            with open('mycart.json', 'r') as file:
                mycart = json.load(file)  # Parse existing cart data
        except FileNotFoundError:
            mycart = []  # Initialize an empty cart if file doesn't exist

        # Get the product data from the request
        product = request.get_json()

        if not product:
            return jsonify({"error": "Invalid product data"}), 400

        # Add the new product to the cart
        mycart.append(product)

        # Save the updated cart back to the file
        with open('mycart.json', 'w') as file:
            json.dump(mycart, file, indent=4)  # Write the updated cart to file

        return jsonify({"message": "Product added to cart successfully", "product": product}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/clear-cart', methods=['DELETE'])
def clear_cart():
    try:
        mycart = []

        # Save the updated cart back to the file
        with open('mycart.json', 'w') as file:
            json.dump(mycart, file, indent=4)  # Write the updated cart to file

        return jsonify({"message": "Cart cleared successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)