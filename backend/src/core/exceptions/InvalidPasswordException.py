from shared.errors.ApiResponse import ApiResponse

class InvalidPasswordException(ApiResponse):
    def __init__(self, message: str = "Password must contain"):
        super().__init__(
            status_code=400,
            message=message
        )
        self.name = self.__class__.__name__