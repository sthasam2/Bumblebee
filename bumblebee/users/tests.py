import random
import string


from django.test import TestCase
from users.models import CustomUser


class UserProfileTest(TestCase):
    def random_string(self):
        return "".join(random.choice(string.ascii_lowercase) for i in range(10))

    def test_user_has_profile(self):
        user = CustomUser(
            email=f"{self.random_string()}@{self.random_string()}.com",
            username=self.random_string(),
            password="123ajkdsa34fana",
        )
        user.save()

        self.assertTrue(hasattr(user, "profile"))
