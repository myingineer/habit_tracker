from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..Utils import oauth2, database, utils, validators
from ..Schemas import users_schemas
from ..Models import users_model

router = APIRouter(
    tags=["Authentication"],
    prefix="/users"
)

@router.post("/login", response_model=users_schemas.Token)
async def loginUser(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # Find the user in the database
    user = db.query(users_model.User).filter(users_model.User.username == user_credentials.username.lower()).first()

    # If the user is not found, raise an exception
    if not user:
        validators.Validator_Functions.general_error("Invalid credentials", status.HTTP_403_FORBIDDEN)
    
    # Check if the password is correct
    if not utils.verify_password(user_credentials.password, user.password):
        validators.Validator_Functions.general_error("Invalid credentials", status.HTTP_403_FORBIDDEN)
    
    # Create an access token
    access_token = oauth2.create_access_token(
        data = {
            "user_id": user.user_id
        }
    )

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
