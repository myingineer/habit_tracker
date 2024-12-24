"""
    This file is used to validate requests and responses in the application.
"""

from datetime import datetime
from fastapi import HTTPException, status
from ..Schemas import habits_schemas, users_schemas


class Validator_Functions:
    # Check if the habit exists
    @staticmethod
    async def habit_exist(habit: habits_schemas.Habit, habit_id: int):
        if not habit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Habit not found with ID : {habit_id} not found"
            )
        
        return habit
    
    # Check if the user has permission to perform requested action
    @staticmethod
    async def confirm_permission(id: int, user_id: int):
        if id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={"status": "failure", "message": "You do not have permission to view this page"}
            )
        
        return True
        
    # Validating the email of the user by checking to see if there's a user object gotten from the database
    @staticmethod
    async def validate_user_by_email(user: users_schemas.User, update_info):
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status": "failure",
                    "message": f"User with email: {update_info.email} not found"
                }
            )
        
        return user
    
    # Validate code sent to the user
    @staticmethod
    async def validate_code(user, update_info):
        if int(user.token) != update_info.code:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": "failure",
                    "message": "Invalid reset code"
                }
            )
        
        return user
    
    # Check if the reset code has expired
    @staticmethod
    async def check_code_validity(user):
        if user.token_expiry < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "status": "failure",
                    "message": "Reset code has expired"
                }
            )
        
        return user
    
    # Check if the field is_token_verified is set to True
    @staticmethod
    async def is_token_verified(user):
        if user.is_token_verified == False:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "status": "failure",
                    "message": "Reset code is not verified"
                }
            )
        
        return True
    
    # General error message
    @staticmethod
    async def general_error(message, status_code):
        raise HTTPException(
            status_code=status_code,
            detail={
                "status": "failure",
                "message": message
            }
        )

