#ApiResponse.py
class ApiResponse(Exception):
    def __init__(self, status_code, message=None):
        super().__init__(message or self.get_default_message(status_code))
        self.status_code = status_code
        self.message = message or self.get_default_message(status_code)
    
    @staticmethod
    def get_default_message(status_code):
        messages = {
            400: 'A bad request, you have made.',
            401: 'Unauthorized, you are not allowed to do this.',
            404: 'Resource not found, it was.',
            500: ('Errors are the path to the dark side. Errors lead to anger. '
                  'Anger leads to hate. Hate leads to career change.'),
        }
        return messages.get(status_code, 'An unexpected error has occurred.')