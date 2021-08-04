import random
import string


class RandomData:
    @classmethod
    def uname(cls):
        return "".join([random.choice(string.ascii_lowercase) for _ in range(1, 8)])

    @classmethod
    def email(cls):
        return f'{RandomData.uname()}@example.com'

    @classmethod
    def pw(cls):
        pwchars = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        return "".join([random.choice(pwchars) for _ in range(1, 8)])
