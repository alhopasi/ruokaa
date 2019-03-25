from application import db

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    
    name = db.Column(db.String(144), nullable=False)
    preparing_time = db.Column(db.Integer, nullable=False)
    recipe = db.Column(db.String(5000), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)

    def __init__(self, name, preparing_time, recipe, account_id):
        self.name = name
        self.preparing_time = preparing_time
        self.recipe = recipe
        self.account_id = account_id
