from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, ValidationError
from typing import Optional
import bcrypt
import jwt

class JwtData(BaseModel):
    sub: str  # Typically the user ID
    iat: datetime  # Issued at time
    exp: datetime  # Expiration time
    # You can add additional fields here as needed
    # role: Optional[str] = None  # Example of an additional field

class AuthManager:
    def __init__(self, secret_key: str, algorithm: str = 'HS256', token_expiry_minutes: int = 120):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.token_expiry_minutes = token_expiry_minutes

    def create_jwt(self, user_id: str, extra_claims: Optional[dict] = None) -> str:
        """
        Creates a JWT for the given user_id.
        :param user_id: The ID of the user for whom the token is being created.
        :param extra_claims: Optional dictionary of additional claims to include in the token.
        :return: The JWT as a string.
        """
        payload = {
            'sub': user_id,
            'iat': datetime.now(timezone.utc),
            'exp': datetime.now(timezone.utc) + timedelta(minutes=self.token_expiry_minutes)
        }
        if extra_claims:
            payload.update(extra_claims)
        
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        return token

    def validate_jwt(self, token: str) -> JwtData:
        """
        Validates a JWT and returns the decoded payload as an instance of TokenData if valid.
        :param token: The JWT string to validate.
        :return: The decoded token as a TokenData instance.
        :raises: jwt.ExpiredSignatureError, jwt.InvalidTokenError, ValidationError
        """
        try:
            decoded_token = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            token_data = JwtData(**decoded_token)
            return token_data
        except jwt.ExpiredSignatureError:
            raise jwt.ExpiredSignatureError("Token has expired")
        except jwt.InvalidTokenError:
            raise jwt.InvalidTokenError("Invalid token")
        except ValidationError as e:
            raise ValueError(f"Token validation error: {e}")

    def hash_password(self, password: str) -> str:
        """
        Hashes a password using bcrypt.
        :param password: The password to hash.
        :return: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """
        Verifies a password against a given hashed password.
        :param password: The plain text password to verify.
        :param hashed_password: The hashed password to compare against.
        :return: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def generate_join_code(self) -> str:
        """
        Generates a random 6-character alphanumeric code.
        :return: The generated join code.
        """
        import random
        import string
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))