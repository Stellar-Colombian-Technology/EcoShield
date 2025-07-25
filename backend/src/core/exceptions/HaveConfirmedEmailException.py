from shared.errors.ApiResponse import ApiResponse

class HaveConfirmedEmailException(ApiResponse):
    def __init__(self, message: str = "The email is not confirmed yet. Please check your email inbox."):
        super().__init__(
            status_code=400,
            message=message
        )
        self.name = self.__class__.__name__