import server.app as mongo

class UserModel:

    @staticmethod
    def getUserByEmail(email):
        return mongo.db.user.find_one({'email': email})

    @staticmethod
    def createUser(user):
        return mongo.db.user.insert_one(user)

    @staticmethod
    def deleteUser(email):
        return mongo.db.user.delete_one({"email": email})

    @staticmethod
    def getAllUsers():
        return mongo.db.user.find()
