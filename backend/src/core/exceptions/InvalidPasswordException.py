from shared.errors.ApiResponse import ApiResponse

class InvalidPasswordException(ApiResponse):
    def __init__(self, message="Password inválida", missing_requirements=None):
        full_message = f"{message}"  # Ya lo armaste tú en el validador
        super().__init__(
            status_code=400,
            message=full_message
        )
        self.name = self.__class__.__name__
        self.missing_requirements = missing_requirements or []