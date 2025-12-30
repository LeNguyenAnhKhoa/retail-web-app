from fastapi import APIRouter, Request, Depends
from typing import Optional
from shared_config import StandardResponse, standard_response
from shared_utils import login_required
from controllers import *
from models import LoginModel, RegisterModel, TokensModel, UpdateUserModel, AdminUpdateUserModel, RefreshTokenModel

router = APIRouter()

@router.post("/login", response_model=StandardResponse)
@standard_response
def login(payload: LoginModel, request: Request):
    client_ip = request.client.host
    user_agent = request.headers.get("User-Agent")
    controller = LoginController()
    response = controller.execute(payload, client_ip, user_agent)
    return response

@router.get("/get-user-detail", response_model=StandardResponse)
@standard_response
def get_user_detail(user_info: dict = Depends(login_required)):
    controller = GetUserDetailController()
    response = controller.execute(user_info)
    return response


@router.post("/register", response_model=StandardResponse)
@standard_response
def register(payload: RegisterModel):
    controller = RegisterController()
    controller.execute(payload)
    return {}


@router.post("/update-user-info", response_model=StandardResponse)
@standard_response
def update_user_info(updated_user: UpdateUserModel, user_info: int = Depends(login_required)):
    controller = UpdateUserController()
    controller.execute(updated_user, user_info)
    return {}

@router.post("/update-user-by-admin", response_model=StandardResponse)
@standard_response
def update_user_by_admin(updated_user: AdminUpdateUserModel, user_info: dict = Depends(login_required)):
    controller = UpdateUserByAdminController()
    controller.execute(updated_user, user_info)
    return {}


@router.post("/logout", response_model=StandardResponse)
@standard_response
def logout(refresh_token: str, request: Request, user_info: dict = Depends(login_required)):
    access_token = request.headers.get("Authorization")
    controller = LogoutController()
    controller.execute(user_info, refresh_token, access_token)
    return {}


@router.post("/get-new-access-token", response_model=StandardResponse)
@standard_response
def get_new_access_token(payload: RefreshTokenModel):
    controller = GetNewAccessTokenController()
    response = controller.execute(payload.refresh_token)
    return response

@router.post("/activate-user", response_model=StandardResponse)
@standard_response
def activate_user(user_id: int, user_info: dict = Depends(login_required)):
    controller = ActivateUserController()
    controller.execute(user_id, user_info)
    return {}

@router.get("/get-all-users", response_model=StandardResponse)
@standard_response
def get_all_users(search: Optional[str] = None, user_info: dict = Depends(login_required)):
    controller = GetAllUsersController()
    response = controller.execute(user_info, search)
    return response

@router.post("/deactivate-user", response_model=StandardResponse)
@standard_response
def deactivate_user(user_id: int, user_info: dict = Depends(login_required)):
    controller = DeactivateUserController()
    controller.execute(user_id, user_info)
    return {}

@router.get("/dashboard-stats", response_model=StandardResponse)
@standard_response
def get_dashboard_stats(user_info: dict = Depends(login_required)):
    controller = DashboardStatsController()
    response = controller.execute(user_info)
    return response

@router.get("/monthly-sales", response_model=StandardResponse)
@standard_response
def get_monthly_sales(user_info: dict = Depends(login_required)):
    controller = MonthlySalesController()
    response = controller.execute(user_info)
    return response

@router.delete("/delete-user", response_model=StandardResponse)
@standard_response
def delete_user(user_id: int, user_info: dict = Depends(login_required)):
    controller = DeleteUserController()
    controller.execute(user_id, user_info)
    return {}