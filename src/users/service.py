from users.repository import UserRepository
from service import BaseService

class UserService(BaseService):
    repository = UserRepository