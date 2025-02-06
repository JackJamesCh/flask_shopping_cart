
# E-commerce Web Application

This is an e-commerce web application with user and admin functionalities. The application allows users to view featured products, sort by price, and buy products. Admin users can manage products, edit product details, add new products, and delete existing ones.

## Features

### 1. **User Features**
- **No Login Required to Buy Products**: 
  - Users can browse products and make purchases without needing to log in.
  
- **Home Screen**:
  - The homepage displays featured products that can be viewed by any user.

- **Product Details Page**:
  - Users can view detailed product information.
  - Users can sort products by price.

### 2. **Admin Features**
- **Login**:
  - Admins can log in with the following credentials:
    - **Username**: `admin@email.com`
    - **Password**: `admin123`
  
  - The application can distinguish between normal users and admins.
  
- **Admin Dashboard**:
  - Admins can see a list of all products in the system, including product details like name, price, image, and featured status.

- **Product Management via Ag-Grid**:
  - Admins can **edit product details** directly through the Ag-Grid table.
  - To make changes:
    - Click into a field to edit.
    - Click outside the box or hit "Enter" to save the changes directly to the table.
    - Click Save Changes button.
  
- **Delete a Product**:
  - Admins can delete a product by clicking the **Delete** button next to the corresponding product row in the table.
  
- **Add a New Product**:
  - Admins can add a new product through the same page.

### 3. **Available User Accounts**

- **Admin**:
  - Username: `admin@email.com`
  - Password: `admin123`
  
- **Users**:
  - **Jack**:
    - Username: `jack@email.com`
    - Password: `jack123`
  
  - **Test**:
    - Username: `test@email.com`
    - Password: `test123`

---