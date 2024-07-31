from pydantic import BaseModel


class SignUpSchema(BaseModel):
    email:str
    password:str
    first_name: str
    last_name: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "samplePassword123",
                "first_name": "john"
                "last_name" "Doe"
            }
        }

class LoginSchema(BaseModel):
    email:str
    password:str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "sample@gmail.com",
                "password": "samplePassword123"
            }
        }