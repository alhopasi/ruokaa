from application import db

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(144), nullable=False)
    preparing_time = db.Column(db.Integer, nullable=False)
    recipe = db.Column(db.String(5000), nullable=False)

    def __init__(self, name, preparingTime, recipe):
        self.name = name
        self.preparingTime = preparingTime
        self.recipe = recipe
