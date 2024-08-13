from fastapi import APIRouter
from app.api.routes import users, messages

router = APIRouter(prefix="/api")
router.include_router(router=users.router, prefix="/users", tags=["users"])
router.include_router(
    router=messages.router, prefix="/users/{user_id}/messages", tags=["messages"]
)


@router.get("/")
def read_root():
    return {"Hello": "World"}
