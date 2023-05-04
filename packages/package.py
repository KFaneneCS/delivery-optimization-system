class Package:
    # TODO: cite the following: "https://stackoverflow.com/questions/77552/id-is-a-bad-variable-name-in-python"
    def __init__(self, id_, address, deadline, city, zip_code, mass):
        self.id_ = id_
        self.address = address
        self.deadline = deadline
        self.city = city
        self.zip_code = zip_code
        self.mass = mass
        self.status = "At hub"
