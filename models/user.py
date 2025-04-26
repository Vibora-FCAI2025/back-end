from .document import Document

class User(Document):
    REQUIRED_FIELDS = ['name', 'email', 'age', 'created_at']

    def __init__(self, data=None):
        super().__init__('users', data, required_fields=self.REQUIRED_FIELDS)

    @property
    def name(self):
        return self.data.get('name')

    @property
    def email(self):
        return self.data.get('email')

    @property
    def age(self):
        return self.data.get('age')

    @property
    def created_at(self):
        return self.data.get('created_at')

    def __str__(self):
        return f"User(name={self.name}, email={self.email}, age={self.age})"
