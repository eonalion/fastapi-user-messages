import uuid


def generate_uuid():
    return str(uuid.uuid4())


print(generate_uuid())
