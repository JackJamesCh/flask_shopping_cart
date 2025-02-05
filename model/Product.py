class Product:
    def __init__(self, name, price, image, featured):
        self.name = name
        self.price = price
        self.image = image
        self.featured = featured

    def __str__(self):
        return f"{self.name} - ${self.price} (Featured: {self.featured})"

    def to_dict(self):
        """Convert product instance to dictionary for JSON serialization."""
        return {
            "name": self.name,
            "price": self.price,
            "image": self.image,
            "featured": self.featured
        }