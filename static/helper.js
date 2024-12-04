// Function to call the "Add to Cart" API
async function addToCart(product) {
    const apiUrl = "http://127.0.0.1:5000/api/add-to-cart"; // Replace with your add-to-cart API endpoint

    try {
        const response = await fetch(apiUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(product),
        });

        if (!response.ok) {
            throw new Error(`Error: ${response.status} - ${response.statusText}`);
        }

        alert(`${product.name} has been added to your cart!`);
    } catch (error) {
        console.error("Failed to add product to cart:", error);
        alert("Failed to add product to cart. Please try again.");
    }
}