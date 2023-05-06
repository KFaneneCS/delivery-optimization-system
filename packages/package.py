class Package:
    def __init__(self, id_, destination, city, state, zip_code, deadline, kilos):
        self.id_ = id_
        self.destination = destination
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.kilos = kilos
        self.priority = None

    def __repr__(self):
        return f'Package(ID={self.id_} | destination={self.destination} | deadline={self.deadline} | ' \
               f'priority={self.priority}'

    def get_id(self):
        return self.id_

    def get_destination(self):
        return self.destination

    def get_deadline(self):
        return self.deadline

    def set_priority(self, priority_value: float):
        self.priority = priority_value
        return self.priority
