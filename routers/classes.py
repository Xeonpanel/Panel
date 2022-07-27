from __main__ import sqlquery

class User():
    def __init__(self, id: int, name: str, email: str, token: str, user_type: str):
        self.id = id
        self.name = name
        self.email = email
        self.token = token
        self.type = user_type

    def get(self id: int):
        data = sqlquery("SELECT * FROM users WHHERE id = ?", id)
        if len(data):
            return User(data[0][0], data[0][1], data[0][2], data[0][4], data[0][5])

    