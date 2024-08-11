import random
import string
import uuid


def generate_random_email(domain: str = "test.com") -> str:
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"{username}@{domain}"


def generate_random_name() -> str:
    first_name = "".join(
        random.choices(string.ascii_lowercase, k=random.randint(3, 8))
    ).capitalize()
    last_name = "".join(
        random.choices(string.ascii_lowercase, k=random.randint(3, 10))
    ).capitalize()

    return f"{first_name} {last_name}"


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()
