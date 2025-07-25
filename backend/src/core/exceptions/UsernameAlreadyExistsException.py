from shared.errors.ApiResponse import ApiResponse

class UsernameAlreadyExistsException(ApiResponse):
    def __init__(self, message: str = "Username already exists."):
        super().__init__(
            status_code=400,
            message=message
        )
        self.name = self.__class__.__name__