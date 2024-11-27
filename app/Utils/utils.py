from passlib.context import CryptContext
import random

# This just tells passlib to use the bcrypt hashing algorithm 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# This function will hash a password
def hash_password(password: str):
    return pwd_context.hash(password)

# This function will verify a password
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# This function will generate a random token
def generate_reset_token():
    return str(random.randint(100000, 999999))

def emailTemplate(username, body):
    # Create the HTML content of the email
    html = f"""
        <html>
            <div class="content">
                <p>Hello <span>{username.capitalize()}</span>,</p>
                <p>{body}</p>
            </div>
        </html>
    """

    return html