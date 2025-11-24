"""
Role-based Access Control (RBAC) Middleware
Phân quyền theo vai trò: MANAGER, STAFF, STOCKKEEPER
"""

from functools import wraps
from fastapi import HTTPException, status
from typing import List

# Role definitions
class Roles:
    MANAGER = "MANAGER"
    STAFF = "STAFF"
    STOCKKEEPER = "STOCKKEEPER"

# Permission mapping theo yêu cầu
PERMISSIONS = {
    # Module: Quản lý người dùng và phân quyền
    "user:login": [Roles.MANAGER, Roles.STAFF, Roles.STOCKKEEPER],
    "user:manage": [Roles.MANAGER],
    "user:assign_roles": [Roles.MANAGER],
    "user:view": [Roles.MANAGER],
    
    # Module: Quản lý sản phẩm
    "product:manage": [Roles.MANAGER, Roles.STOCKKEEPER],
    "product:view": [Roles.MANAGER, Roles.STAFF, Roles.STOCKKEEPER],
    "product:view_import_price": [Roles.MANAGER, Roles.STOCKKEEPER],
    "product:edit_import_price": [Roles.MANAGER, Roles.STOCKKEEPER],
    
    # Module: Quản lý danh mục
    "category:manage": [Roles.MANAGER, Roles.STOCKKEEPER],
    "category:view": [Roles.MANAGER, Roles.STOCKKEEPER],
    
    # Module: Quản lý nhà cung cấp
    "supplier:manage": [Roles.MANAGER, Roles.STOCKKEEPER],
    "supplier:view": [Roles.MANAGER, Roles.STOCKKEEPER],
    
    # Module: Quản lý khách hàng
    "customer:manage": [Roles.MANAGER, Roles.STAFF],
    "customer:view": [Roles.MANAGER, Roles.STAFF],
    
    # Module: Quản lý kho hàng
    "inventory:import": [Roles.MANAGER, Roles.STOCKKEEPER],
    "inventory:export": [Roles.MANAGER, Roles.STOCKKEEPER],
    "inventory:stock_check": [Roles.MANAGER, Roles.STOCKKEEPER],
    "inventory:view": [Roles.MANAGER, Roles.STOCKKEEPER],
    
    # Module: Quản lý bán hàng
    "order:create": [Roles.MANAGER, Roles.STAFF],
    "order:view": [Roles.MANAGER, Roles.STAFF],
    
    # Module: Báo cáo và thống kê
    "report:revenue": [Roles.MANAGER],
    "report:profit": [Roles.MANAGER],
    "report:stock": [Roles.MANAGER, Roles.STOCKKEEPER],
    "report:best_selling": [Roles.MANAGER, Roles.STOCKKEEPER],
}

def check_permission(user_role: str, permission: str) -> bool:
    """
    Kiểm tra xem user có quyền thực hiện action không
    
    Args:
        user_role: Role của user (MANAGER, STAFF, STOCKKEEPER)
        permission: Permission cần check (vd: "product:manage")
    
    Returns:
        True nếu có quyền, False nếu không
    """
    allowed_roles = PERMISSIONS.get(permission, [])
    return user_role in allowed_roles

def require_permission(permission: str):
    """
    Decorator để check permission cho route
    
    Usage:
        @require_permission("product:manage")
        async def create_product(user_role: str = Depends(get_current_user_role)):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract user_role from kwargs (passed by dependency injection)
            user_role = kwargs.get('user_role') or kwargs.get('current_user', {}).get('role')
            
            if not user_role:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            if not check_permission(user_role, permission):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Permission denied. Required permission: {permission}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def require_roles(allowed_roles: List[str]):
    """
    Decorator đơn giản hơn - chỉ check role
    
    Usage:
        @require_roles([Roles.MANAGER, Roles.STOCKKEEPER])
        async def create_product(current_user: dict = Depends(get_current_user)):
            ...
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            user_role = current_user.get('role')
            if user_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Allowed roles: {', '.join(allowed_roles)}"
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
