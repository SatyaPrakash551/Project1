from fastapi import APIRouter
from src.service.userService import UserService
from fastapi import status
from src.schema.userSchema import UserRequest, UserResponse
from fastapi import Depends,Request
from src.dependency.serviceDependency import getUserService
from src.redis_client import redis_client
import json
from fastapi.exceptions import HTTPException
from redis.exceptions import RedisError
router = APIRouter(prefix="/user",tags=["user"])

@router.post('/',status_code=status.HTTP_201_CREATED)
async def createUser(request:UserRequest,user_service: UserService= Depends(getUserService)):
    return await user_service.createUser(request)

@router.post('/sigin',status_code=status.HTTP_200_OK,response_model=UserResponse)
async def signIn(request : UserRequest,user_service : UserService = Depends(getUserService)):
    chache_key = f"myapp:user:{request.email}"
    try:
        chache_user = await redis_client.get(chache_key)

        if chache_user is not None:
            print(f"Chache hit : {chache_key}")
            return  json.loads(chache_user)
        
    except(RedisError,ValueError):
        print("chache read failed ; falling back to postgres")

    print(f"chache Miss : {chache_key}")
    user = await user_service.signIn(email=request.email,password =request.password)

    if user is None:
        raise HTTPException(status_code=404,detail="user not found")

    try:
        await redis_client.set(chache_key,json.dumps(user))#ex= 300
    except RedisError:
        print("chache write failed ; returning to databse result")
    return user