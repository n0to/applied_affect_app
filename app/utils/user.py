import app.models.user as models_user
import app.schemas.user as schemas_user


def get_user(email: str):
    user = models_user.User.objects(email=email)
    return schemas_user.UserInDB.from_orm(user)
