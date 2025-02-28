from fastapi import APIRouter


user_router = APIRouter()


@user_router.get("/me")
def get_user():
    return ""
