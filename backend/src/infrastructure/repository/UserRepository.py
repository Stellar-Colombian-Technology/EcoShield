from sqlalchemy.orm import Session
from infrastructure.model.User import User

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: dict) -> User:
        user = User(**data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def find_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def find_all(self, filters: dict = {}) -> list[User]:
        query = self.db.query(User)
        for attr, value in filters.items():
            query = query.filter(getattr(User, attr) == value)
        return query.all()

    def find_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def find_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def update(self, user_id: int, update_data: dict) -> User | None:
        user = self.find_by_id(user_id)
        if not user:
            return None
        for key, value in update_data.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.find_by_id(user_id)
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True