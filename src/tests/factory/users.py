import random

from faker import Faker


fake = Faker()


def create_fake_user():
    username = fake.user_name()
    password = fake.password(length=12)
    email = fake.email()
    full_name = fake.name()
    role = random.choice(["hr", "user"])
    return {
        "email": email,
        "password": password,
        "username": username,
        "full_name": full_name,
        "role": role,
    }
