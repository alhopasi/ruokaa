from application import db
from application.models import Base
from application.auth.models import User

from sqlalchemy.sql import text

ingredients = db.Table('ingredients',
    db.Column('food_id',  db.Integer, db.ForeignKey('food.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

class Food(Base):
    name = db.Column(db.String(144), nullable=False)
    preparing_time = db.Column(db.Integer, nullable=False)
    recipe = db.Column(db.String(5000), nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    ingredients = db.relationship('Ingredient', secondary=ingredients, lazy='subquery',
        backref=db.backref('foods', lazy=True))

    def __init__(self, name, preparing_time, recipe, account_id):
        self.name = name
        self.preparing_time = preparing_time
        self.recipe = recipe
        self.account_id = account_id
    
    def getId(self):
        return self.id

    def findIngredients(self):
        foodId = self.getId()
        stmt = text("SELECT Ingredient.id, Ingredient.name FROM Ingredient"
                    " JOIN Ingredients ON Ingredients.ingredient_id = Ingredient.id"
                    " WHERE Ingredients.food_id = " + str(foodId) )
        res = db.engine.execute(stmt)

        response = []
        for row in res:
            response.append({"id":row[0], "name":row[1]})

        return response
    
    def getUser(self):
        u = User.query.get(self.account_id)
        return u

    def deleteIngredient(self, ingredient_id):
        stmt = text("DELETE FROM Ingredients"
                   " WHERE Ingredients.ingredient_id = " + str(ingredient_id) + ""
                   " AND Ingredients.food_id = " + str(self.id) )

        db.engine.execute(stmt)
    

class Ingredient(Base):
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def findIngredient(name):
        if not name:
            return
        name = name.lower().strip()
        i = Ingredient.query.filter_by(name=name).first()

        if not i:
            i = Ingredient(name)
            db.session().add(i)
            db.session().commit()
            return Ingredient.findIngredient(name)
            
        return i

    