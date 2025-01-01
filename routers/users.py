from datetime import datetime, timedelta 
from fastapi import Depends, HTTPException, status, APIRouter, Body
from pydantic import BaseModel
from sqlalchemy.orm import Session
from google.cloud import bigquery
import os
from dotenv import load_dotenv
from fastapi.security import  OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from jose import jwt
from fastapi.responses import JSONResponse

# Load environment variables
load_dotenv()
class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter()

router = APIRouter(prefix="/users")

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
PROJECT_ID = os.getenv("PROJECT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM='HS256'

# Function to get BigQuery client
def get_bigquery_client():
    return bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

# Dependency to get database session
def get_db():
    client = get_bigquery_client()
    return client

# OAuth2PasswordBearer instance
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model 
class User:
    def __init__(self, id, username, first_name, last_name, email, phone_number, password):
        self.id = id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.password = password

# Authenticate user and return JWT
def authenticate_user(username: str, password: str, db: bigquery.Client):
    query = f"""
        SELECT * 
        FROM `{PROJECT_ID}.sales_data.users` 
        WHERE username = @username
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("username", "STRING", username)
        ]
    )
    result = db.query(query, job_config=job_config).result()
    user = [dict(row) for row in result]
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    return User(
        id=user[0].get("id"),
        username=user[0].get("username"),
        first_name=user[0].get("first_name"),
        last_name=user[0].get("last_name"),
        email=user[0].get("email"),
        phone_number=user[0].get("phone_number"),
        password=user[0].get("password")
    )


# Generate JWT token
from datetime import datetime, timedelta  # Ensure this is your import

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=15)  # Use datetime.utcnow
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Register route
@router.post("/register/")
def register_user(user_data: dict = Body(...), db: bigquery.Client = Depends(get_bigquery_client)):
    username = user_data.get("username")
    first_name = user_data.get("first_name")
    last_name = user_data.get("last_name")
    email = user_data.get("email")
    phone_number = user_data.get("phone_number")
    password = user_data.get("password")

    query = f"""
    INSERT INTO `{PROJECT_ID}.sales_data.users` 
    (username, first_name, last_name, email, phone_number, password) 
    VALUES ('{username}', '{first_name}', '{last_name}', '{email}', '{phone_number}', '{password}')
    """
    db.query(query).result()
    return {"msg": "User registered successfully"}



@router.post("/token/")
def login_for_access_token(
    form_data: LoginRequest, 
    db: bigquery.Client = Depends(get_bigquery_client)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Create the JWT token
    access_token = create_access_token(data={"sub": user.username})
    
    # Set the cookie in the response
    response = JSONResponse(
        content={"message": "Login successful","access_token":access_token, "token_type": "bearer"}
    )
    return response

@router.post("/logout/")
def logout_user():
    response = JSONResponse(
        content={"message": "Logged out successfully"}
    )
    response.set_cookie(
        key="access_token", 
        value="",          # Empty value to clear the cookie
        httponly=True, 
        secure=True, 
        samesite="Lax", 
        max_age=0,        
        expires="Thu, 01 Jan 1970 00:00:00 GMT" 
    )
    return response
