from fastapi import APIRouter, Path
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from bson.objectid import ObjectId
from src.databases.mongodb import MongoDB
from src.constants.collections import Collections
from src.utils.hasher import get_hash
from src.utils.logger import LOG

router = APIRouter()
mongo_db = MongoDB()

@router.get("/balance/{id}")
def get_balance(id=Path(...)):
    user = mongo_db.get_document(Collections.COLLECTION_USERS, {"_id": ObjectId(id)})
    if not user:
      return HTTPException(
          status_code=400,
          detail={"status": "failed", "message": f"No user with id {id} found"},
      )
    return JSONResponse(
                status_code=200,
                content={"status": "success", "message": f"Your balance is {user.get("balance")}"},
            )


    


# //TODO automatically guess who the user is using jwt token or something
