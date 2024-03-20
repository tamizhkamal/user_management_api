from dependencies import get_data_hash
from requests import Session

from user.models import UserMaster
from user.schemas import UserCreate, UserUpdate


def create_user_data(db: Session, UserData: UserCreate):
    pincode = UserData.pincode
    print(UserData.username, "000000000000000000000000000000")
    user_db = UserMaster(
        username=UserData.username,
        hashed_password=get_data_hash(UserData.hashed_password),
        email=UserData.email,
        contact_number=UserData.contact_number,
        # pincode=UserData.pincode,
    )

    print("user_db", user_db)  # This will show the class name and memory location of the object
    print("user_db type", type(user_db))

    # if get_user_by_mobile(db, user_db.contact_number):
    #     exists_dict = {"message" : "User Already Exists", "code": "403"}
    #     return exists_dict
    try:
        db.add(user_db)
        db.commit()
        db.refresh(user_db)
        success_dict = {"message": "User added successfully", "code": "200", "result": user_db}
    except Exception as e:
        print(e)  # Print the exception for debugging purposes
        success_dict = {"message": "User Email or contact number Already Exists", "code": "200",}

    return success_dict

def update_user_data(id: int, user_update: UserUpdate, db: Session):
    user_details = db.query(UserMaster).filter(UserMaster.id == id).first()
    if user_details is None:
        return None
    user_details.username = user_update.username
    user_details.contact_number = user_update.contact_number
    db.commit()
    result = {
        "message": "Updated successfully",
        "UserID": user_details.id,
        "UserName": user_details.username,
        "ContactNumber": user_details.contact_number,
    }
    return result


def delete_user_data(id: int,db: Session):
    user_details = db.query(UserMaster).filter(UserMaster.id == id).first()
    user_details.delete = True
    db.commit()
    return {"message":'User Deleted succesfully'}