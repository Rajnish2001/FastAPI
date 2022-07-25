from fastapi import APIRouter


router = APIRouter()
@router.get('/users',tags=['User'])
def user():
    return 'user section'