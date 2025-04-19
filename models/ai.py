import boto3
import uuid
from uuid import UUID
from fastapi import HTTPException
from schemas.ai import CreateAiData
from dotenv import load_dotenv

dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('ai_Data')

def getAi():
    data=table.scan()
    return data

def createAi(aiData: CreateAiData):
    try:
        ai_id = uuid.uuid4()
        # print(aiData.ai_name)
        data = table.put_item(Item={
            "ai_id": str(ai_id),
            "ai_name": aiData.ai_name,
            "ai_description": aiData.ai_description,
            "ai_category": aiData.ai_category,
            "owner": aiData.owner,
            "company": aiData.company
        })
        return ai_id
    except Exception as e:
        print(f"❌ Error Creating AI: {e}")
    return None
