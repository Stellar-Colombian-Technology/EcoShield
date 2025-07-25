import re
from core.exceptions.InvalidPasswordException import InvalidPasswordException

def validate_password_strength(password: str) -> None:
    """Versión con validación detallada por componentes"""
    missing_requirements = []
    
    if len(password) < 8:
        missing_requirements.append("at least 8 characters")
    
    if not any(c.isupper() for c in password):
        missing_requirements.append("at least one uppercase letter")
    
    if sum(c.isdigit() for c in password) < 2:
        missing_requirements.append("at least two digits")
    
    special_chars = set("!@#$%^&*(),.?\":{}|<>")
    if not any(c in special_chars for c in password):
        missing_requirements.append("at least one special character")
    
    if missing_requirements:
        raise InvalidPasswordException(
            missing_requirements=missing_requirements,
            message=f"Password missing: {', '.join(missing_requirements)}"
        )