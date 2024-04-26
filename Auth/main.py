from starlette.responses import JSONResponse
from Auth.crud import *
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES
from user import schemas as Userschema
from fastapi import Depends,APIRouter,HTTPException,status
from Auth.schemas import Token,ResetPassword, Users
from database import get_db
import datetime
from sqlalchemy.orm import Session
import random
# from app.Users import crud
# from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
# from google.auth.transport import requests
# from google.oauth2 import id_token
from fastapi import HTTPException
from user import *
from user.crud import create_user_data
from user.models import UserMaster

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# router = APIRouter(tags=['Auth'])
router = APIRouter(
# router = APIRouter(tags=['Auth'])
    prefix="/Auth",
)

def generate_otp():
    return "".join([str(random.randint(0, 9)) for i in range(6)])

def failure_message(message):
    return JSONResponse({"status": "failed", "message": message},
                        status_code=401)
# Login



@router.post("/token", response_model=Token, tags=["Authentication"])
async def login_for_access_token(from_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    print(from_data,"<--------------------------- from_data")
    user = authendicate_user(db, from_data.username, from_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    db.query(UserMaster).filter(UserMaster.username == from_data.username).update(
        {
            UserMaster.access_token: access_token,
            UserMaster.token_type: "bearer",
            UserMaster.updated_at: datetime.datetime.now(),
            UserMaster.otp: generate_otp()
        }
    )
    
    try:
        db.commit()
    except:
        db.rollback()

    user_ = db.query(UserMaster).filter(UserMaster.id == user.id).first()

    response = Token(
        access_token=access_token,
        token_type="bearer",
        user_id=user_.username,
        user_name=str(user_.id),  # Convert user_.id to string
        # usertype_id=user_.usertype
    )

    return response

@router.post("/forgot_password/otp-gen",tags=["Authentication"])
async def forgot_password_otp_generation(mobile_no:str,db:Session=Depends(get_db)):
    if len(mobile_no)!=10 and not mobile_no.isdigit():
        return JSONResponse({"status":"failed","message":"Please enter a valid mobile number"},status_code=401)
    user = get_user(db,mobile_no=mobile_no)
    if user is None:
        return JSONResponse({"status": "failed", "message": "No user is registered with this mobile number"}, status_code=401)
    otp = generate_otp()
    db.query(UserMaster).filter(UserMaster.username==user.username).update({
        UserMaster.otp : otp
    })
    try:
        db.commit()
    except :
        db.rollback()
    return {"otp":otp,"status": "success", "message": "OTP has been sent to user's mobile number"}


@router.post("/forgot_password/otp-val",tags=["Authentication"])
async def forgot_password_otp_generation(otp:str,mobile_no:str,db:Session=Depends(get_db)):
    user = get_user(db,mobile_no=mobile_no)
    if user is None:
        return failure_message("No user is registered with this mobile number")
    if otp != user.otp:
        return failure_message("Incorrect OTP")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    db.query(UserMaster).filter(UserMaster.username==user.username).update(
        {
            UserMaster.access_token: access_token,
            UserMaster.token_type: "bearer",
        }
    )
    try:
        db.commit()
    except:
        db.rollback()
    return {"status": "success", "message": "OTP Validated Successfully","access_token": access_token, "token_type": "bearer"}


@router.post("/reset_password", tags=["Authentication"])
async def reset_password(request: ResetPassword,user = Depends(get_current_active_user), db: Session = Depends(get_db)):
    if request.password != request.confirm_password:
        return failure_message("Passwords do not match")
    if user is None:
        return failure_message("User authentication failed")
    db.query(UserMaster).filter(UserMaster.username == user.username).update({
        UserMaster.hashed_password: get_data_hash(request.password)
    })
    try:
        db.commit()
    except:
        db.rollback()
    return {"status": "success", "message": "Password changed successfully"}







