from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    is_admin: bool = False

class UserOut(BaseModel):
    id: int
    email: str
    is_admin: bool

class Token(BaseModel):
    access_token: str
    token_type: str