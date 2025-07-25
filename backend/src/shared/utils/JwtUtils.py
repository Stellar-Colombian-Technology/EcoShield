import jwt
import uuid
from datetime import datetime
import os
from typing import Dict, Any

# Configuración desde variables de entorno
ISSUER = os.getenv("JWT_ISSUER")
SECRET = os.getenv("JWT_SECRET" )  
EXPIRES_IN = os.getenv("JWT_EXPIRES_IN")

def generate_token(user: Dict[str, Any]) -> str:
   
    now = datetime.utcnow()
    
    payload = {
        "sub": user["username"],
        "userId": str(user["_id"]),
        "fullName": f"{user['firstName']} {user['lastName']}",
        "isVerified": user["isVerified"],
        "email": user["email"],
        "authorithies": user.role.name if user.role else "USER",
        "iat": int(now.timestamp()),
        "nbf": int(now.timestamp()),
        "iss": ISSUER
    }

    return jwt.encode(
        payload,
        SECRET,
        algorithm="HS256",
        headers={"exp": int((now + timedelta(hours=1)).timestamp())} if EXPIRES_IN == "1h" else None
    )

def verify_token(token: str) -> Dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            SECRET,
            algorithms=["HS256"],
            issuer=ISSUER,
            options={"require": ["iss", "exp", "iat", "nbf"]}
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Token inválido: {str(e)}")