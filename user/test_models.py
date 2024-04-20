# import unittest
# from models import UserMaster as User
# from pydantic import ValidationError

# class TestUserModel(unittest.TestCase):
#     def test_valid_user(self):
#         # Test valid user data
#         user_data = {
#             "id": 1,
#             "username": "john_doe",
#             "email": "john@example.com",
#             "contact_number": "1234567890",
#             "hashed_password": "hashed_password",
#             "access_token": "access_token",
#             "token_type": "Bearer",
#             "otp": "1234",
#             "image": "image.jpg",
#             "is_admin": False,
#             "delete": False,
#             "created_by": 1,
#             "updated_by": 1,
#         }
#         user = User(**user_data)
#         self.assertEqual(user.id, 1)
#         self.assertEqual(user.username, "john_doe")
#         self.assertEqual(user.email, "john@example.com")
#         # Add more assertions for other fields as needed

#     def test_invalid_user(self):
#         # Test invalid user data
#         invalid_user_data = {
#             "id": "invalid_id",  # Invalid data type for id
#             "username": "john_doe",
#             "email": "john@example.com",
#             "contact_number": "1234567890",
#             "hashed_password": "hashed_password",
#             "access_token": "access_token",
#             "token_type": "Bearer",
#             "otp": "1234",
#             "image": "test.jpg",
#             "is_admin": False,
#             "delete": False,
#             "created_by": 1,
#             "updated_by": 1,
#         }
#         try:
#             User(**invalid_user_data)
#         except ValidationError as e:
#             # Verify the fields causing the validation error
#             self.assertIn("id", e.errors())  # Check if 'id' is in the list of errors
#             print("ValidationError raised as expected:", e)
#         else:
#             self.fail("ValidationError not raised")

# if __name__ == "__main__":
#     unittest.main()
