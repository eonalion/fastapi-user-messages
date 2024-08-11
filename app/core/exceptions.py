class NotFoundError(Exception):
    def __init__(self, message="Entity not found"):
        self.message = message
        super().__init__(self.message)


class AlreadyExistsError(Exception):
    def __init__(self, message="Entity already exists"):
        self.message = message
        super().__init__(self.message)
