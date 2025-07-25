from core.service.UserService import UserService
from core.service.EmailService import EmailService
from api.dto.Auth.AuthResponse import AuthResponse
from api.dto.Auth.AuthLoginRequest import AuthLoginRequest
from core.interceptors.RunInterceptors import run_interceptors
from core.interceptors.User.ConfirmedMailInterceptor import validate_confirmed_mail
from api.dto.User.UserDto import AuthRegisterRequest
from infrastructure.model.User import User
from shared.utils.JwtUtils import generate_token
from infrastructure.model.EmailVerificationToken import EmailVerificationToken
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self):
        self.user_service = UserService()
        self.email_service = EmailService()

    async def login(self, request_data: dict, db: Session) -> AuthResponse:
        login_request = AuthLoginRequest(**request_data)
        username = login_request.username
        password = login_request.password

        user = self.user_service.find_by_username(db, username)
        if not user:
            return AuthResponse(
                username=None,
                message="Usuario no encontrado",
                jwt=None,
                status=False
            )

        await run_interceptors([lambda: validate_confirmed_mail(user)])

        if not pwd_context.verify(password, user.password):
            return AuthResponse(
                username=None,
                message="Contraseña incorrecta",
                jwt=None,
                status=False
            )

        token = generate_token(user)

        return AuthResponse(
            username=user.username,
            message="Inicio de sesión exitoso",
            jwt=token,
            status=True
        )
    
    
    async def register(self, request_data: dict, db: Session) -> AuthResponse:
        register_request = AuthRegisterRequest(**request_data)
        user_data = register_request()

        user_service = UserService(db)

        try:
            created_user = await user_service.create(user_data)

            token_model = EmailVerificationToken.create_for_user(created_user.id)
            db.add(token_model)
            db.commit()
            db.refresh(token_model)

            await self.email_service.send_verification_email(
                to_email=created_user.email,
                username=created_user.username,
                token=token_model.token
            )

            token = generate_token(created_user)

            return AuthResponse(
                username=created_user.username,
                message="Usuario registrado exitosamente",
                jwt=token,
                status=True
            )

        except Exception as e:
            return AuthResponse(
                username=user_data.get("username"),
                message=str(e),
                jwt=None,
                status=False
            )

    def verify_email(self, token: str, db: Session) -> dict:
        record = db.query(EmailVerificationToken).filter_by(token=token).first()

        if not record:
            raise Exception("Token inválido o ya utilizado")

        if record.is_expired():
            raise Exception("El token ha expirado")

        user = db.query(User).filter_by(id=record.user_id).first()
        if not user:
            raise Exception("Usuario no encontrado")

        user.is_verified = True
        db.add(user)
        db.delete(record)
        db.commit()

        return {
            "message": "Correo verificado correctamente. Ya puedes iniciar sesión."
        }
