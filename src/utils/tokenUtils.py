from jose import jwt,JWTError
from dotenv import load_dotenv
from fastapi.exceptions import HTTPException
from fastapi import status
import os 
from datetime import datetime ,timedelta,timezone

load_dotenv()

def generateToken(email:str,user_id :int)->str:
    secret_key = os.getenv("SECRET_KEY")
    payload = {
        user_id : user_id,
        email : email
    }
    token = jwt.encode(claims={**payload,"exp":datetime.now(timezone.utc) + timedelta(minutes=30)},key=secret_key,algorithm="HS256",)
    return token

def verifyToken(token:str)->dict:
    try:
        payload = jwt.decode(token = token,key=os.getenv("SECRET_KEY"), algorithms="HS256")
        return payload
    except JWTError as err: 
        print(err)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="provided token is wrong")

