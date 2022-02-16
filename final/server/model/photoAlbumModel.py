from server.s3 import s3
import server.app as mongo
import datetime
import os
import uuid


class PhotoAlbumModel:

    @staticmethod
    def newPicture(file, idUser):
        filename, pictureExtension = os.path.splitext(file.filename)
        filename = '%s%s' % (str(uuid.uuid4()), pictureExtension)
        picture = {
            "filename": filename,
            "approved": False,
            "creator": idUser,
            "authorizer": None,
            "dateAlteration": None,
            "datetime": datetime.datetime.utcnow()
        }
        s3.upload_fileobj(file, 'anchorphotoalbum', picture['filename'])

        return mongo.db.photo.insert_one(picture)

    @staticmethod
    def deleteImage(picture):
        s3.delete_object(Bucket='anchorphotoalbum', Key=picture['filename'])
        return mongo.db.photo.delete_one({"_id": picture["_id"]})

    @staticmethod
    def getPictureById(id):
        return mongo.db.photo.find_one({"_id": id})

    @staticmethod
    def getPicturesApproved():
        return mongo.db.photoAlbum.find({"approved": True})

    @staticmethod
    def getPictures():
        return mongo.db.photoAlbum.find()

    @staticmethod
    def approveImage(idUser, idPicture):
        picture = {
            "approved": True,
            "authorizer": idUser,
            "dateAlteration": datetime.datetime.utcnow()
        }
        return mongo.db.photo.update_one({"_id": idPicture}, {"$set": picture})

    @staticmethod
    def disapproveImage(idUser, idImage):
        picture = {
            "approved": False,
            "authorizer": idUser,
            "dateAlteration": datetime.datetime.utcnow()
        }
        return mongo.db.photo.update_one({"_id": idImage}, {"$set": picture})

    @staticmethod
    def like(idUser, idImage):
        if mongo.db.photo.find_one({"likes.user": idUser}) is None:
            return mongo.db.photo.update_one({"_id": idImage}, {"$push": {"likes": {"user": idUser}}})
        return mongo.db.photo.delete_one({"likes.user": idUser})
