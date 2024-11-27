from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.params import Body
from ..Utils import database, utils, oauth2, mailing, validators
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..Schemas import users_schemas
from ..Models import users_model

# Create the router
router = APIRouter(
    tags=["Users"],
    prefix="/users"
)

# To create a new user
@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=users_schemas.User)
async def createUser(user: users_schemas.UserCreate = Body(...), db: Session = Depends(database.get_db)):

    # Lowercase the email and username
    user.email = user.email.lower()
    user.username = user.username.lower()

    # Hash the password
    user.password = utils.hash_password(user.password)

    # To take the user from the schema, turn it to a dictionary and pass it to the User model
    new_user = users_model.User(**user.model_dump())

    try: 
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "status": "failure",
                "message": "User with email or username already exists"
            }
        )
    
    # Contents of the email
    email_string = f"Welcome OnBoard to our Application. We hope you keep to your habits. Cheersssss!!!!"
    html = utils.emailTemplate(new_user.username, email_string)
    
    try:
        await mailing.send_email(user.email, "Welcome OnBoard", html)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sending failed"
        )
    
    return new_user

# To get the user profile
@router.get("/profile", status_code=status.HTTP_200_OK, response_model=users_schemas.User)
async def getUserProfile(db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):

    user = db.query(users_model.User).filter(users_model.User.user_id == current_user.user_id).first()

    return user

# To confirm the email of the user who wants to reset their password
@router.post("/reset/confirm/email", status_code=status.HTTP_200_OK)
async def confirmResetEmail(update_info: users_schemas.EmailVerify = Body(...), db: Session = Depends(database.get_db)):

    user = db.query(users_model.User).filter(users_model.User.email == update_info.email.lower()).first()
    
    # Validate the user by email and check if it exists in the database
    await validators.Validator_Functions.validate_user_by_email(user, update_info)
    
    # Generate a random code
    random_code = utils.generate_reset_token()

    # Send Code to User Email and update the code in the database with the expiry time
    user.token = random_code
    user.token_expiry = datetime.now() + timedelta(minutes=10)

    # Contents of the email
    email_string = f"Use this code {random_code} to reset your password. Code expires in 10 minutes."
    html = utils.emailTemplate(user.username, email_string)

    # Try to save the code in the database
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database update failed"
        )

    # Try to send the email
    try:
        await mailing.send_email(user.email, "Password Reset Code", html)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sending failed"
        )

    return {
        "status": "success",
        "message": f"Code sucessfully sent to {update_info.email}"
    }


# To confirm the reset code and check if it is valid
@router.post("/reset/confirm/code", status_code=status.HTTP_200_OK)
async def confirmResetCode(
    update_info: users_schemas.CodeVerify = Body(...), 
    db: Session = Depends(database.get_db)
):
    user = db.query(users_model.User).filter(users_model.User.email == update_info.email.lower()).first()

    await validators.Validator_Functions.validate_user_by_email(user, update_info)
    await validators.Validator_Functions.validate_code(user, update_info)
    await validators.Validator_Functions.check_code_validity(user)

    # Update the user token to verified
    try:
        user.is_token_verified = True
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database update failed"
        )

    return {
        "status": "success",
        "message": "Reset code is valid"
    }


# To reset the password of the user
@router.post("/reset/password", status_code=status.HTTP_200_OK, response_model=users_schemas.User)
async def resetPassword(
    update_info: users_schemas.PasswordReset = Body(...), 
    db: Session = Depends(database.get_db),
):
    user = db.query(users_model.User).filter(users_model.User.email == update_info.email.lower()).first()

    await validators.Validator_Functions.validate_user_by_email(user, update_info)
    await validators.Validator_Functions.is_token_verified(user)

    # Confirm the time for the token expiry is still valid
    try: 
        user = await validators.Validator_Functions.check_code_validity(user)
    except Exception:
        user.token = None
        user.token_expiry = None
        user.is_token_verified = False
        db.commit()
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Reset code has expired. Please request a new one"
        )


    user.password = utils.hash_password(update_info.new_password)
    user.token = None
    user.token_expiry = None
    user.is_token_verified = False

    # Try to update the password in the database
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Database update failed"
        )
    
    email_string = f"Your password was successfully changed. If you didn't do this, Please contact support immediately. Else, Ignore this email. Cheersss!!!"
    html = utils.emailTemplate(user.username, email_string)
    
    try:
        await mailing.send_email(user.email, "Password Reset Successful", html)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sending failed"
        )

    return user