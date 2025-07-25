from sqlalchemy import Column, Integer, Enum as SqlEnum
from sqlalchemy.orm import relationship
from infrastructure.model.enum.RolesEnum import RoleEnum
from infrastructure.config.Base import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(SqlEnum(RoleEnum), unique=True, nullable=False)

    users = relationship("User", back_populates="role")
