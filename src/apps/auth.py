from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from src.databases.mongodb import MongoDB
from src.constants.collections import Collections
from src.utils.hasher import get_hash
from src.utils.logger import LOG
from src.utils.jwt import construct_jwt


router = APIRouter()
mongo_db = MongoDB()

class upsertUser(BaseModel):
    access_token:str
    username:str
    balance:dict

class loginUser(BaseModel):
  access_token:str
  username :str



@router.post("/signup")
def upsert_user(body:upsertUser):
  try:
    data = body.model_dump()
    user_data = {"balance":data.get("balance"),"username":data.get("username")}
    user_id = mongo_db.upsert_document(Collections.COLLECTION_USERS,user_data)
    hashed_username = get_hash(data.get("username"))
    hashed_access_token = get_hash(data.get("access_token"))
    secret_data = {"user_id":user_id,"hashed_username":hashed_username,"hashed_access_token":hashed_access_token}
    mongo_db.upsert_document(Collections.COLLECTION_SECRETS,secret_data)
    #TODO: Currently multiple records for a single user can be formed(Bug)
    return JSONResponse(status_code=201,content={"status": "success", "message": f"User created with id:{user_id} and username:{data.get("username")}"})
  except Exception as e:
     LOG.error(f"Signup failed",e)
     return HTTPException(400,{"status":"failed"})

@router.post("/login")
def login_user(body:loginUser):
  try:
    data = body.model_dump()
    hashed_username = get_hash(data.get("username"))
    secrets = mongo_db.get_document(Collections.COLLECTION_SECRETS,{"hashed_username":hashed_username})
    if not secrets:
       raise HTTPException(400,{"status":"failed","details":"Username not found"})
    hashed_access_token = get_hash(data.get("access_token"))
    if hashed_access_token!=secrets.get("hashed_access_token"):
        raise HTTPException(400,{"status":"failed","details":"Wrong access token"})
    user_id = str(secrets.get("user_id"))
    payload = {"user_id":user_id}
    jwt_token = construct_jwt(payload)
    return JSONResponse(status_code=200,content={"status":"success","jwt_token":jwt_token})
  except Exception as e:
     print(e)
     LOG.error("Failed to login,error:",e)
     return HTTPException(status_code=400,detail={"status":"failed"})

