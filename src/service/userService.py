from fastapi import Request,Response,Depends
from src.db.db_config import get_session
from src.repository.userRepository import UserRepository
from src.model.userModel import User
from src.schema.userSchema import UserRequest
from src.utils.password import hashedPassword , decryptPassword
from fastapi.exceptions import HTTPException
from fastapi import status
from src.exception.resourceNotFound import ResourceNotFoundException
from src.utils.tokenUtils import generateToken

class UserService:
    def __init__(self,user_repo:UserRepository):
        self.user_repo = user_repo

    async def createUser(self, req: UserRequest):
        
        user = User(email= req.email,password = hashedPassword(req.password) )
        return await self.user_repo.createUser(user)

    async def getUser(self,email:str):
        return await self.user_repo.getUser(email)
        # return {"message":"user not found"}

    async def signIn(self, email: str, password : str):
        dbUser = await self.user_repo.getUser(email)
        if not dbUser:
            raise ResourceNotFoundException("You email is incorrect or please register yourself first")
        isauth = decryptPassword(password , dbUser.password)
        if not isauth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="your password is incorrect")
        token = generateToken(dbUser.user_id, dbUser.email)
        data = {
            "user_id" : dbUser.user_id,
            "email" : dbUser.email,
            "token" : token
        }
        return data
