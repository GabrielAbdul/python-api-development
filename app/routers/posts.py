from fastapi import Response, Depends, status, HTTPException, APIRouter
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import List
from typing import Optional
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):

    # convert to dict, then ** unpacks dict
    created_post = models.Post(owner_id=current_user.id, **post.dict())
    # stage newly created post
    db.add(created_post)
    db.commit()
    # retrieve newly created post and store it in created_post
    db.refresh(created_post)
    return created_post


@router.get('/', response_model=List[schemas.PostOut])
#@router.get('/', response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    # pre join posts query
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # joins the posts table and likes table requiring the post.id to = the like.post_id
    # filters results by search, limit, or skipping
    posts = db.query(
        models.Post, func.count(models.Like.post_id).label("likes")).join(
            models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    post = db.query(
        models.Post, func.count(models.Like.post_id).label("likes")).join(
            models.Like, models.Like.post_id == models.Post.id, isouter=True).group_by(
                models.Post.id).filter(models.Post.id == id).first()
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    '''deletes a post from the database'''
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized')

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    '''updates a post'''
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Not authorized')
    # Update the query object
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post