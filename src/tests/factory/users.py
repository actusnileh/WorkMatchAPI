from faker import Faker


fake = Faker()


def create_fake_user():
    username = fake.user_name()
    password = fake.password(length=12)
    email = fake.email()
    full_name = fake.name()
    return {
        "email": email,
        "password": password,
        "username": username,
        "full_name": full_name,
        "role": "user",
    }


def create_fake_hr():
    username = fake.user_name()
    password = fake.password(length=12)
    email = fake.email()
    full_name = fake.name()
    return {
        "email": email,
        "password": password,
        "username": username,
        "full_name": full_name,
        "role": "hr",
    }
