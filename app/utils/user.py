from pydantic import EmailStr
import app.models.user as models_user
import app.schemas.user as schemas_user
from app.utils.auth import verify_password


def get_user_by_email(email: EmailStr):
    user = models_user.User.objects(email=email).first()
    return schemas_user.UserInDB.from_orm(user)


def set_user_password(id: str, hashed_password: str):
    user = models_user.User.objects.get(id=id)
    user.hashed_password = hashed_password
    user.save()


def authenticate_user(email: EmailStr, password: str):
    user = get_user_by_email(email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
