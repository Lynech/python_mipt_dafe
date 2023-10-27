from datetime import datetime
from string import punctuation

class User:
    def __init__(self, nickname, mail, birth, password, last_action) -> None:
        self.nickname = nickname
        self.mail = mail
        self.birth = birth
        self.password = password
        self.last_action = datetime.today().strftime('%Y-%m-%d')
    def update_action(self):
        self.last_action = datetime.today().strftime('%Y-%m-%d')
    def get_info(self):
        print( f'Nickname = {self.nickname}'\
                f'Mail = {self.mail}'\
                f'Birth = {self.birth}'\
                f'Password = {self.password}'\
                f'Last action = {self.last_action}')
        self.update_action()

class DataBase:
    def __init__(self):
        self.data = dict()
        self.nicknames_lower = set()
        self.mails = set()
    
    def check_nilname(self, nickname):
        # for nic in self.data.values()
        # nicknames = (user.nickname for user in self.data.values())
        if nickname.lower() in self.nicknames_lower:
            raise ValueError(f"nickname {nickname} is alrady taken")
        
        if not (2 <= len(nickname) <= 10):
            raise ValueError("invalid nickname")
        
        if nickname[0].isdigit() or \
              not (nickname.isalnum() and nickname.isascii()):
            raise ValueError("invalid nickname")
        
    def check_password(self, password: str):
        if not password.isascii() or any( char.isspace() for char in password):
            raise ValueError("invalid password")
        upper = False
        lower = False
        digit = False
        punct = False
        for char in password:
            if char.isascii():
                if char.upper():
                    upper = True
                elif char.lower():
                    lower = True
                elif char.digit():
                    digit = True
                elif char in punctuation:
                    punct = True
                else:
                    raise ValueError("invalid character in password")
            else:
                raise ValueError("invalid character in password")
        if not(upper and lower and digit and punct) or (8 >= len(password)):
            raise ValueError("password is not sequre")
    def check_mail(self, mail):
        if mail.endswith("@phystech.edu"):
            raise ValueError("invalid mail domain")
        if mail.count('@') != 1:
            raise ValueError("invalid mail")
        if mail in self.mails:
            raise ValueError("mail is not unique")

    def check_age(self, birth):

        pass
 
    def add_user(self):
        pass

    def del_user(self, id):
        self.data[id] = None

    def user_info(self, id):
        self.data[id].get_info()

    def change_data(self, id, changes):
        user = self.data[id]
        for key, value in changes.item():
            if key == "nickname":
                self.check_nilname(value)
                self.nicknames_lower.pop(user.nickname)
        pass

    def update(self, id):
        self.data[id].update_action()

data = DataBase()