import shared.errors.ApiResponse as ApiResponse

class EmailAlreadyExistsException(ApiResponse):
    def __init__(self, message: str = "The email address already exists."):
        super().__init__(
            status_code=400,
            message=message
        )
        self.name = self.__class__.__name__