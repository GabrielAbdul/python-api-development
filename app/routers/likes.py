from email.policy import HTTP
from fastapi import Response, Depends, status, HTTPException, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def like(like: schemas.Like, db: Session = Depends(database.get_db),
         current_user: int = Depends(oauth2.get_current_user)):

    post= db.query(models.Post).filter(models.Post.id == like.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with {like.post_id} does not exist')

    # to create a like, check if it exists first
    like_query = db.query(models.Like).filter(
        models.Like.post_id == like.post_id, models.Like.user_id == current_user.id)

    found_like = like_query.first()
    if (like.dir == 1):
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already liked {like.post_id}")
        new_like = models.Like(post_id = like.post_id, user_id = current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "successfully added like"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Like does not exist")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted like"}