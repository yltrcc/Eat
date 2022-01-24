import datetime


class Member:
    def __init__(self, user_id: str = '', user_name: str = '', pwd: str = '',
                 create_datetime: datetime.datetime = None) -> None:
        self.id = user_id
        self.user_name = user_name
        self.password = pwd
        self.create_datetime = create_datetime

    def __repr__(self) -> str:
        return 'user_id = ' + self.id + ', user_name = ' + self.user_name + ', create_datetime = ' + str(
            self.create_datetime)