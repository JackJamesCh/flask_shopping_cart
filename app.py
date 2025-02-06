from flask import Flask, render_template, jsonify, request
from dao.ProductDao import ProductDao
from dao.UserDao import UserDao
from model.Product import Product
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

productDao = ProductDao()
userDao = UserDao()

# Ensure this folder exists
UPLOAD_FOLDER = os.path.join('static', 'images')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route('/')
def home():
    # Render an HTML template called 'index.html'
    return render_template('index.html')

@app.route('/admin_portal')
def admin_portal():
    return render_template('admin_portal.html')

@app.route('/shop')
def shop():
    # Render an HTML template called 'shop'
    return render_template('shop.html')

@app.route('/about')
def about():
    # Render an HTML template called 'about'
    return render_template('about.html')

@app.route('/mycart')
def mycart():
    # Render an HTML template called 'my cart'
    return render_template('mycart.html')

@app.route('/signin')
def signin():
    # Render an HTML template called 'signin.html'
    return render_template('signin.html')


@app.route('/api/get-products')
def get_products():

    return jsonify(productDao.get_all_products())
    # Load data from products.json
    #try:
        #with open('products.json', 'r') as file:
           # products = json.load(file)  # Parse the JSON file into a Python object
       # return jsonify(products)  # Return the data as a JSON response
    #except FileNotFoundError:
       # return jsonify({"error": "File not found"}), 404
  #  except json.JSONDecodeError:
        #return jsonify({"error": "Error decoding JSON"}), 500

@app.route('/api/get-featured-products')
def get_featured_products():
    return jsonify(productDao.get_all_featured_products())
    # # Load data from products.json
    # try:
    #     with open('products.json', 'r') as file:
    #         products = json.load(file)  # Parse the JSON file into a Python object
    #
    #     # Filter products to get only featured products
    #     featured_products = [product for product in products if product.get('featured')]
    #
    #     return jsonify(featured_products)  # Return the featured products as a JSON response
    #
    # except FileNotFoundError:
    #     return jsonify({"error": "File not found"}), 404
    # except json.JSONDecodeError:
    #     return jsonify({"error": "Error decoding JSON"}), 500


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

@app.route('/api/signin', methods=['POST'])
def api_signin():
    # Get the email and password from the request
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = (userDao.get_user_by_email_password(email, password))
    print(user)
    if user is not None:
        if user['is_admin']:
            return jsonify({"message": "Login successful"}), 200  # Successful login
        else:
            return jsonify({"error": "User is not an Admin!"}), 401
    else:
        return jsonify({"error": "Invalid credentials"}), 404  # Invalid login credentials

    # # Load the users from the users.json file
    # try:
    #     with open('users.json', 'r') as file:
    #         users = json.load(file)  # Parse the JSON file into a Python object
    #
    #     user = None  # Initialize the user variable as None
    #
    #     # Loop through all users in the list
    #     for u in users:
    #         # Check if both the email and password match
    #         if u['email'] == email and u['password'] == password:
    #             user = u  # Assign the matching user to the user variable
    #             break  # Exit the loop as we've found the matching user
    #
    #     if user is not None:
    #         return jsonify({"message": "Login successful"}), 200  # Successful login
    #     else:
    #         return jsonify({"error": "Invalid credentials"}), 404  # Invalid login credentials
    #
    # except FileNotFoundError:
    #     return jsonify({"error": "Users file not found"}), 404
    # except json.JSONDecodeError:
    #     return jsonify({"error": "Error decoding JSON"}), 500

@app.route('/api/update-products', methods=['POST'])
def update_products():
    """API endpoint to update multiple products."""
    data = request.get_json()
    products = data.get("products", [])

    updated_count = 0

    for product_data in products:
        product = Product(
            name=product_data["name"],
            price=product_data["price"],
            image=product_data.get("image", ""),  # Ensure image is handled if needed
            featured=bool(product_data["featured"])
        )

        productDao.update_product(product)
        updated_count += 1

    return jsonify({"message": f"Updated {updated_count} products successfully!"}), 200


@app.route('/api/delete-product', methods=['POST'])
def delete_product():
    """API endpoint to update multiple products."""
    data = request.get_json()
    productName = data.get("productName", "")

    # Fetch the product from the database to get the image path
    product = productDao.get_product_by_name(productName)

    if not product:
        return jsonify({"message": f"Product {productName} not found!"}), 404

    # Delete the image file from static/images if it exists
    image_path = product.image
    if os.path.exists(image_path):
        os.remove(image_path)

    productDao.delete_product(productName)

    return jsonify({"message": f"Deleted {productName} successfully!"}), 200


@app.route('/api/add-product', methods=['POST'])
def add_product():
    """API endpoint to add a single product with an image."""
    # Check if the request contains the necessary parts (form data and files)
    if 'image' not in request.files:
        return jsonify({"message": "No image file part"}), 400

    # Get form data
    name = request.form.get('name')
    price = request.form.get('price')
    featured = request.form.get('featured', False)  # Default to False if not provided
    image = request.files['image']

    if not name or not price:
        return jsonify({"message": "Name and price are required"}), 400

    # Handle image upload (save to static/images)
    filename = secure_filename(image.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)

    # Save the image to the static/images folder
    image.save(image_path)

    # Create a product object
    product = Product(
        name=name,
        price=float(price),  # Assuming price is a number and needs conversion
        image=image_path,  # Store the path to the image
        featured=bool(featured)
    )

    # Add the product using your DAO
    productDao.add_product(product)

    return jsonify({"message": "Product added successfully!"}), 201


if __name__ == '__main__':
    app.run(debug=True)