from pydantic import BaseModel, Field
from typing import Optional

class UserModel(BaseModel):
    user_id: int = Field(..., title="User ID", description="Unique identifier for the user")
    username: str = Field(..., title="Username", description="Username of the user")
    full_name: str = Field(..., title="Full Name", description="Full name of the user")
    phone: str = Field(..., title="Phone", description="Phone number of the user")
    role: str = Field(..., title="Role", description="Role of the user (MANAGER, STAFF, STOCKKEEPER)")
    is_active: bool = Field(True, title="Is Active", description="Whether the user is active")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "username": "admin",
                "full_name": "Nguyễn Văn Admin",
                "phone": "0901234567",
                "role": "MANAGER",
                "is_active": True
            }
        }
        
        
class UpdateUserModel(BaseModel):
    username: Optional[str] = Field(None, title="Username", description="Username of the user")
    full_name: Optional[str] = Field(None, title="Full Name", description="Full name of the user")
    phone: Optional[str] = Field(None, title="Phone", description="Phone number of the user")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "admin",
                "full_name": "Nguyễn Văn Admin",
                "phone": "0901234567"
            }
        }

class CreateUserModel(BaseModel):
    username: str = Field(..., title="Username", description="Username of the user")
    password: str = Field(..., title="Password", description="Password of the user")
    full_name: str = Field(..., title="Full Name", description="Full name of the user")
    phone: str = Field(..., title="Phone", description="Phone number of the user")
    role: str = Field("STAFF", title="Role", description="Role of the user (MANAGER, STAFF, STOCKKEEPER)")
    is_active: bool = Field(True, title="Is Active", description="Whether the user is active")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "username": "staff1",
                "password": "123456",
                "full_name": "Trần Thị Nhân Viên",
                "phone": "0902345678",
                "role": "STAFF",
                "is_active": True
            }
        }
    