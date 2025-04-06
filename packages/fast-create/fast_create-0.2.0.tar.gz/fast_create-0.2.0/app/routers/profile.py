from fastapi import APIRouter, Depends
from securities.oauth2 import get_current_user
router = APIRouter()
from schemas.userSchema import Profile

@router.get('/users/me', response_model=Profile)
def myProfile(current_user: Profile = Depends(get_current_user)):
    return current_user