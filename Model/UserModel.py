from Database.Connection import ConnectionModel


class User:
    def __init__(self, _id, name, username, email, password):
        self.id = _id
        self.name = name
        self.username = username
        self.email = email
        self.password = password
        self.user_collection = ConnectionModel.connect("user_info")

    def user_registration(self):
        result = self.user_collection.count({"username": self.username})
        if result:
            return "User already exists!"
        result = self.user_collection.insert_one({
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "password": self.password
        })
        if result.inserted_id:
            return "<p>User Added Successfully</p>"
        else:
            return "not successful"


class UserObject:
    def __init__(self, username, role):
        self.username = username
        self.blacklist = role
