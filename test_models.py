import unittest
from app import User, bcrypt

class TestModels(unittest.TestCase):
    def test_new_user(self):
        """
        Given a User model
        When a new User is created
        then check the username, email, and hashed_password are defined correctly
        """
        hashed_password = bcrypt.generate_password_hash("123456")
        user = User(username="mama", email="mama@example.com", password=hashed_password)
        self.assertEqual(user.firstname, None)
        self.assertEqual(user.lastname, None)
        self.assertEqual(user.username, "mama")
        self.assertEqual(user.email, "mama@example.com")
        self.assertNotEqual(user.password, "123456")

if __name__ == '__main__':
    unittest.main()
