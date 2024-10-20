from fastapi import APIRouter, Depends
from models.users import User
from utils.auth_utils import get_current_user


router = APIRouter(
    prefix="/book",
    tags=["book"],
    responses={400: {"detail": "Error"}},
)


@router.get('/{book_id}')
async def get_book_by_id(book_id: int, user: User = Depends(get_current_user)):
    return {"message": "working"}
