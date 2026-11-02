from src.repository.userRepository import UserRepository
from fastapi import Depends
from src.dependency.repositoryDependency import getUserRepository
from src.service.userService import User
from src.service.userService import UserService
def getUserService(user_repo : UserRepository = Depends(getUserRepository)):
    return UserService(user_repo)