from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str
    name: str
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True  # replaces orm_mode


class UserRead(BaseModel):
    id: str
    email: str
    username: str
    name: str

    class Config:
        from_attributes = True  # replaces orm_mode

class UserPreview(BaseModel):
    id: str
    name: str  # 👈 match actual field name in your User model

    class Config:
        from_attributes = True


class UserBasic(BaseModel):
    id: str
    name: str
    class Config:
        from_attributes = True


