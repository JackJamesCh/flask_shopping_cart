class User:
    def __init__(self, email, password, is_admin):
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def __str__(self):
        return f"{self.email} - ${self.password} (Is Admin: {self.is_admin})"

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin
        }