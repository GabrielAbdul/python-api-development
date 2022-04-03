from fastapi import Response, Depends, status, HTTPException, APIRouter
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get('/', response_model=List[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get('/{id}', response_model=schemas.UserOut)
# validate id as int
def get_user(id: int, User: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} not found")
    return user


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # hash pawssword  
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    # ** unpacks dict
    created_user = models.User(**user.dict())
    # stage newly created user
    db.add(created_user)
    db.commit()
    # retrieve newly created user and store it in created_user
    db.refresh(created_user)
    return created_user


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    '''deletes a user from the database'''
    user = db.query(models.User).filter(models.User.id == id)
    if user.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.UserOut)
def update_user(id: int, updated_user: schemas.UserCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    '''updates a user'''
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    # Update the query object
    user_query.update(updated_user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()