from sqlalchemy.orm import Session
from infrastructure.model.Role import Role

class RoleRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> Role:
        role = Role(**data)
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)
        return role

    def find_by_id(self, role_id: int) -> Role | None:
        return self.db.query(Role).filter(Role.id == role_id).first()

    def find_by_name(self, name: str) -> Role | None:
        return self.db.query(Role).filter(Role.name == name).first()

    def find_all(self) -> list[Role]:
        return self.db.query(Role).all()

    def delete(self, role_id: int) -> bool:
        role = self.find_by_id(role_id)
        if not role:
            return False
        self.db.delete(role)
        self.db.commit()
        return True