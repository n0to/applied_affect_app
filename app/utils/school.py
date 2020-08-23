from mongoengine import DoesNotExist
import app.models.school as models_school
import app.schemas.school as schemas_school


def get_camera(id: str):
    camera = models_school.Camera.objects.get(id=id)
    return schemas_school.Camera.from_orm(camera)
