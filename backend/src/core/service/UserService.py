from infrastructure.repository.UserRepository import UserRepository
from core.interceptors.RunInterceptors import run_interceptors
from core.interceptors.User.UniqueUsernameInterceptor import validate_unique_username
from core.interceptors.User.UniqueEmailInterceptor import validate_unique_email
from core.interceptors.User.PasswordStrengthInterceptor import validate_password_strength
from core.helpers.Pager import create_pager
from core.helpers.Params import create_params
from sqlalchemy.orm import Session
from infrastructure.model.User import User


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def find_by_email(self, email: str) -> User | None:
        return self.repo.find_by_email(email)

    def find_by_username(self, username: str) -> User | None:
        return self.repo.find_by_username(username)

    def find_by_id(self, user_id: int) -> User | None:
        return self.repo.find_by_id(user_id)

    async def create(self, user_data: dict) -> User:
        await run_interceptors([
        self._check_username_unique,
        self._check_email_unique,
        # self._check_password_strength,
    ], user_data)

        user = User(**user_data)
        user.hash_password()

        return self.repo.create(user)

# Métodos privados
    async def _check_username_unique(self, data: dict):
        await validate_unique_username(data["username"], self.db)

    async def _check_email_unique(self, data: dict):
        await validate_unique_email(data["email"], self.db)

    # def _check_password_strength(self, data: dict):
    #     return validate_password_strength(data["password"])
    #     async def update(self, user_id: int, update_data: dict) -> User | None:
    #         update_data["exclude_id"] = user_id

    #         await run_interceptors([
    #             lambda data: validate_unique_username(data, self.db),
    #             lambda data: validate_unique_email(data, self.db),
    #             lambda data: validate_password_strength(data),
    #         ], update_data)

    #         if "password" in update_data:
    #             temp_user = User(password=update_data["password"])
    #             temp_user.hash_password()
    #             update_data["password"] = temp_user.password

    #         return self.repo.update(user_id, update_data)

    #     def delete(self, user_id: int) -> bool:
    #         return self.repo.delete(user_id)

    #     def find_all(self, page_index=1, page_size=10, search='') -> dict:
    #         params = create_params(page_index=page_index, page_size=page_size, search=search)

    #         query = self.db.query(User)
    #         if params["search"]:
    #             search_filter = f"%{params['search']}%"
    #             query = query.filter(
    #                 (User.username.ilike(search_filter)) |
    #                 (User.first_name.ilike(search_filter)) |
    #                 (User.last_name.ilike(search_filter))
    #             )

    #         total = query.count()
    #         users = query.offset((params["page_index"] - 1) * params["page_size"]).limit(params["page_size"]).all()

    #         return create_pager(
    #             registers=users,
    #             total=total,
    #             page_index=params["page_index"],
    #             page_size=params["page_size"],
    #             search=params["search"]
    #         )