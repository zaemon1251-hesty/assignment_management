from domain import User, AuthedUser


class UserTest:
    def __init__(self):

        self.user = User(name="test", email="test@example.com", disabled=False)

    def test_vaildate_user(self):

        assert self.user.name == "test"
        assert self.user.email == "test@example.com"
