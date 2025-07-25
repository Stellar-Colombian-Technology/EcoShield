from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.config.Base import Base
from passlib.context import CryptContext
from EmailVerificationToken import EmailVerificationToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_enabled = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    

    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")
    verification_tokens = relationship(
        "EmailVerificationToken", 
        back_populates="user",
        cascade="all, delete-orphan"
    )
    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def hash_password(self):
        self.password = pwd_context.hash(self.password)

    def create_verification_token(self) -> EmailVerificationToken:
        return EmailVerificationToken.create_for_user(self.id)
        