from __main__ import sqlquery

class User():
    def __init__(
        self,
        id: int,
        name: str,
        email: str,
        token: str,
        user_type: str
    ):
        self.id = id
        self.name = name
        self.email = email
        self.token = token
        self.type = user_type