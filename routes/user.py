from fastapi import APIRouter, HTTPException, Query
from schemas.user import User, UserOut, UserUpdate, UserUpdateOut
from models.user import register_user, userData, update_user, get_user ,delete_user
from uuid import UUID

router = APIRouter(prefix="/user", tags=["User"])


@router.get('/data', response_model=list[UserOut])
async def getUserData():
    user = userData()
    # print(user)
    if not user:
        raise HTTPException(status_code=404, detail="No users found")

    parsed_users = []
    for user in user:
        try:
            parsed_users.append(UserOut(
                user_id=UUID(user["user_id"]),
                name=user["name"],
                email=user["emailID"]
            ))
        except Exception as e:
            print(f"Skipping user: {e}")
    return parsed_users


@router.post('/register', response_model=UserOut)
async def registerUserData(user: User):
    user_id = register_user(user)
    if not user_id:
        raise HTTPException(status_code=500, detail="User registration failed.")

    return {
        "user_id": str(user_id),  # Convert UUID to str for response model
        "name": user.name,
        "email": user.email
    }


@router.put("/update", response_model=UserUpdateOut)
async def updateUserData(emailID: str = Query(...), user_data: UserUpdate = ...):
    update_fields = user_data.dict(exclude_unset=True)

    if not update_fields:
        raise HTTPException(status_code=400, detail="No data provided for update")

    # Simply update fields without hashing
    updated = update_user(emailID, update_fields)

    if not updated:
        raise HTTPException(status_code=404, detail="User not found or update failed")

    return updated  # This must match the UserUpdateOut schema


@router.get("/userDetails/{email}", response_model=UserOut)
def findUserData(emailID: str):
    user = get_user(emailID)  # Call the function to fetch user by emailID

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.delete("/deleteUser/{email}")
def deleteUserData(emailID: str):
    delete=delete_user(emailID)

    if not delete:
        raise HTTPException(status_code=404, detail="User not found")

    return delete

