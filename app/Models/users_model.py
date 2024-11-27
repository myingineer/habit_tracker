from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from ..Models import Base

class User(Base):
    __tablename__ = "user_table"
    
    user_id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    token = Column(String, nullable=True) # To store the token for verification any purpose requiring a token
    token_expiry = Column(TIMESTAMP, nullable=True) # To store the expiry of the token
    is_token_verified = Column(Boolean, nullable=False, default=False) # To check if the token has been verified
    # is_user_verified = Column(Boolean, nullable=False, default=False) # To check if the user has verified their email