from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/login')
def login(email, password):
    return {
        "response": "Success/Fail"
    }
