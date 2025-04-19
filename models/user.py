import boto3
import uuid
from uuid import UUID

from fastapi import HTTPException

from schemas.user import User
from dotenv import load_dotenv
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('ai_userData')

load_dotenv()


def userData():
    try:
        response = table.scan()
        # print(response)
        return response.get('Items', [])
    except Exception as e:
        print(f"❌ Error : {e}")
        return None


def register_user(user: User):
    try:
        user_id = uuid.uuid4()
        hashed_pw = pwd_context.hash(user.password)

        table.put_item(Item={
            "user_id": str(user_id),
            "name": user.name,
            "emailID": user.email,  # 👈 This must match your DynamoDB table key name
            "password": hashed_pw
        })

        return user_id  # uuid.UUID is fine, just convert it before response
    except Exception as e:
        print(f"❌ Error registering user: {e}")
        return None


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def update_user(emailID: str, update_fields: dict):
    try:
        # 🚫 Prevent partition key update
        if 'emailID' in update_fields:
            raise ValueError("Cannot update partition key (emailID).")

        # ✅ Hash the password if it's being updated
        if 'password' in update_fields:
            update_fields['password'] = hash_password(update_fields['password'])

        # Prepare the update expression
        expression_attr_names = {}
        expression_attr_values = {}
        update_expr = []

        for k, v in update_fields.items():
            attr_key = f"#attr_{k}" if k.lower() in ["name"] else k

            if attr_key != k:
                expression_attr_names[attr_key] = k

            expression_attr_values[f":{k}"] = v
            update_expr.append(f"{attr_key} = :{k}")

        update_expression = "SET " + ", ".join(update_expr)

        update_args = {
            "Key": {"emailID": emailID},
            "UpdateExpression": update_expression,
            "ExpressionAttributeValues": expression_attr_values,
            "ReturnValues": "ALL_NEW"
        }

        if expression_attr_names:
            update_args["ExpressionAttributeNames"] = expression_attr_names

        # Perform the update
        response = table.update_item(**update_args)

        return response.get("Attributes")

    except Exception as e:
        print(f"❌ Error updating user: {e}")
        return None


def get_user(emailID: str):
    try:
        # Query DynamoDB for user based on emailID (primary key)
        response = table.get_item(Key={"emailID": emailID})

        if 'Item' not in response:
            return None  # Return None if user not found

        # Rename emailID to email in the response before returning it
        user = response['Item']
        user['email'] = user.pop('emailID')  # Change key from emailID to email

        return user

    except Exception as e:
        print(f"Error fetching user: {str(e)}")
        raise HTTPException(status_code=500, detail="Error fetching user data")


def delete_user(emailID):
    # print(emailID)
    try:
        response = table.delete_item(
            Key={
                "email": emailID,  # Replace with actual key name and value
            }
        )
        return response

    except Exception as e:
        print(f"❌ Error Deleting user: {e}")
        return None

