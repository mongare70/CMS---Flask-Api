import unittest
from app import app

class TestModels(unittest.TestCase):
    # def test_api(self):
    #     """
    #     Ensure that Flask was setup correctly
    #     """
    #     tester = app.test_client(self)
    #     response = tester.get('/api', content_type='html/text')
    #     self.assertEqual(response.status_code, 200)


    # def test_correct_login(self):
    #     """
    #     Ensure login behaves correctly given correct credentials
    #     """
    #     tester = app.test_client(self)
    #     response = tester.post('/api/login', data='{"username":"lionel", "password": "123456"}', follow_redirects=True)
    #     self.assertIn(b"true", response.data)


    # def test_wrong_login(self):
    #     """
    #     Ensure login behaves correctly given incorrect credentials
    #     """
    #     tester = app.test_client(self)
    #     response = tester.post('/api/login', data='{"username":"dsfd", "password": "efweffwe"}', follow_redirects=True)
    #     self.assertIn(b"false", response.data)



    # # def test_user_registration(self):
    # #     """
    # #     Ensure user can register
    # #     """
    # #     tester = app.test_client(self)
    # #     response = tester.post('/api/createUser', data='{"username":"lionel", "email":"lionel@example.com", "password": "123456"}', follow_redirects=True)
    # #     self.assertIn(b"true", response.data)


    # def test_edit_user(self):
    #     """
    #     Ensure user can edit his/her details
    #     """
    #     tester = app.test_client(self)
    #     response = tester.post('/api/editUser', data='{"firstname": "lionel", "lastname": "messi", "username":"lionel", "email":"lionel@gmail.com", "password": "123456"}', follow_redirects=True)
    #     self.assertIn(b"true", response.data)



    # def test_edit_user_using_wrong_password(self):
    #     """
    #     Ensure user cannot edit his/her details with wrong password
    #     """
    #     tester = app.test_client(self)
    #     response = tester.post('/api/editUser', data='{"firstname": "lionel", "lastname": "messi", "username":"lionel", "email":"lionel@gmail.com", "password": "jdhjfdh"}', follow_redirects=True)
    #     self.assertIn(b"false", response.data)


    def test_edit_user_password(self):
        """
        Ensure user can edit his/her password
        """
        tester = app.test_client(self)
        response = tester.post('/api/editUserPassword', data='{"username": "lionel", "oldPassword": "123456", "newPassword": "123456"}', follow_redirects=True)
        self.assertIn(b"true", response.data)



    def test_edit_user_password_using_wrong_old_password(self):
        """
        Ensure user cannot edit his/her password with wrong old password
        """
        tester = app.test_client(self)
        response = tester.post('/api/editUserPassword', data='{"username": "lionel", "oldPassword": "sdfsdfef", "newPassword": "123456"}', follow_redirects=True)
        self.assertIn(b"false", response.data)

    
    # def test_get_user_data(self):
    #     """
    #     Ensure user can see his data
    #     """
    #     tester = app.test_client(self)
    #     response = tester.post('/api/getUserData', data='"lionel"', follow_redirects=True)
    #     self.assertIn(b"lionel", response.data)


    # def test_delete_user(self):
    #     """
    #     Ensure user can delete his/her account information
    #     """
    #     tester = app.test_client(self)
    #     response = tester.post('/api/deleteUser', data='"lionel"')
    #     self.assertIn(b"true", response.data)


if __name__ == '__main__':
    unittest.main()
