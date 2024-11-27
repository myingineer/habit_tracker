from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
from ..Schemas import users_schemas
from .database import get_db
from ..Models import users_model

'''
This is a file that contains the functions and classes that are used to handle the authentication and authorization of the API
It contains the following:

- The create_access_token function 
This function is used to create an access token for a user
It takes in a dictionary containing the data to be encoded into the token
It adds an expiration time to the token and encodes the data into a JWT using the SECRET_KEY and ALGORITHM from the settings

- The verify_access_token function
This function is used to verify the access token sent in the request
It decodes the token using the SECRET_KEY and ALGORITHM from the settings
It checks if the token is valid and has not expired
It then returns the data encoded in the token

- The oauth2_scheme object
To extract the token from the request
This looks for the Authorization header in the request and extracts the BEARER token from it
The tokenUrl indicates the endpoint where the token can be requested/refreshed
It then passes the token to the get_current_user function to verify the token and look up the user in the database

- The get_current_user function
This function is used to get the current user from the database
It takes in the token extracted from the request and the database session
It verifies the token using the verify_access_token function
It then looks up the user in the database using the user_id from the token
'''

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def create_access_token(data: dict):
    to_encode = data.copy() # Copy the data to avoid modifying the original data
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # Set the expiration time for the token
    to_encode.update({"exp": expire}) # Add the expiration time to the data
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM) # Encode the data into a JWT
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try: 
        # Decode the token using the SECRET_KEY and ALGORITHM
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Get the user_id from the token
        user_id: int = payload.get("user_id")

        # If the user_id is not present, raise an exception
        if user_id is None:
            raise credentials_exception
        
        # Validate the User ID
        token_data = users_schemas.TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "status": "failure", 
            "message" :"Could not validate credentials or token is invalid or expired"
        },
        headers={"WWW-Authenticate": "Bearer"}
    ) # Create an exception to be raised if the credentials are invalid

    token = verify_access_token(token, credentials_exception) # Verify the token
    user = db.query(users_model.User).filter(users_model.User.user_id == token.user_id).first() # Look up the user in the database

    return user

    