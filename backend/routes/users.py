from fastapi import APIRouter, HTTPException
from backend.database import db
from backend.models import User

router = APIRouter()

@router.post("/users/")
async def create_user(user: User):
    result = await db.users.insert_one(user.dict())
    return {"id": str(result.inserted_id)}

@router.get("/users/{username}")
async def get_user(username: str):
    user = await db.users.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
