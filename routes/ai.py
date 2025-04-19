from fastapi import APIRouter, HTTPException
from schemas.ai import CreateAiData, GetAiData
from models.ai import createAi, getAi
from typing import List
router = APIRouter(prefix='/Ai', tags=["Ai"])

@router.get('/data',response_model=List[GetAiData])
def getAiData():
    response = getAi()
    items = response["Items"]
    return items


@router.post("/createAi")
def createAiData(aiData: CreateAiData):
    response = createAi(aiData)
    # print(response)
    if not response:
        raise HTTPException(status_code=500, detail="User registration failed.")

    return {f"Data Created With id :{response}"}
