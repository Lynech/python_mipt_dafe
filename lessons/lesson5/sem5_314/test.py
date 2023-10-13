class employer:
    id = 0
    name = ''
    hours = 0
    kosyak = 0
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.hours = 0
    def addHours(self, hours):
        self.hours += hours
    def addKosyak(self):
        self.kosyak += 1
    def status(self) -> str:
        string = str(self.id) + ' ' + self.name + ' ' + str(self.hours)
        return string

class Data_base_my:
    main_data = dict()
    def add_employee(self, id, name):
        temp = employer(id, name)
        self.main_data.update({id: temp})
    def fire_employee(self, id):
        if id in self.main_data:
            self.main_data.pop(id)
    def add_hours(self, id, name, hours):
        if id in self.main_data:
            self.main_data[id].addHours(hours)
            if self.main_data[id].name != name:
                self.main_data[id].addKosyak()
    def get_status(self):
        print(60*'v')
        for id in self.main_data:
            print(self.main_data[id].status())
        print(60*'^')
    def fire_kosyachnikov(self):
        for id in self.main_data:
            if self.main_data[id].kosyak >= 3:
                self.main_data.pop(id)
                break
    def __init__(self):
        self.main_data = dict()
        
db = Data_base_my()
while True:
    string = input()
    if(string == 'status'):
        db.get_status()
        continue
    string = string.split()
    if(len(string) == 3):
        id = string[0]
        name = string[1]
        operation = string[2]
        if operation == '+':
            db.add_employee(id, name)
        elif operation == '-':
            db.fire_employee(id)
        elif operation.isdigit():
            hour = int(operation)
            db.add_hours(id, name, hour)
        else:
            print("mrG wtf?")
    else:
        print("mrG wtf?")
    db.fire_kosyachnikov()
