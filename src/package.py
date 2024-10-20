class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At Hub"
        self.delivery_time = None
        self.truck = None

    def __str__(self):
        return f"Package {self.package_id}: {self.address}, {self.city}, {self.state} {self.zip_code}, Due: {self.deadline}, Weight: {self.weight}kg, Status: {self.status}"

    def update_status(self, status, time=None):
        self.status = status
        if status == "Delivered":
            self.delivery_time = time