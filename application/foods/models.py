from application import db
from application.models import Base
from application.auth.models import User
from flask_login import current_user

from sqlalchemy.sql import text

ingredients = db.Table('ingredients',
    db.Column('food_id',  db.Integer, db.ForeignKey('food.id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.id'), primary_key=True)
)

class Food(Base):
    name = db.Column(db.String(144), nullable=False)
    preparing_time = db.Column(db.Integer, nullable=False)
    recipe = db.Column(db.String(5000), nullable=False)
    
    type_id = db.Column(db.Integer, db.ForeignKey('type.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    ingredients = db.relationship('Ingredient', secondary=ingredients, lazy='subquery',
        backref=db.backref('foods', lazy=True))

    def __init__(self, name, preparing_time, recipe, account_id, type_id):
        self.name = name
        self.preparing_time = preparing_time
        self.recipe = recipe
        self.account_id = account_id
        self.type_id = type_id
    
    def getId(self):
        return self.id

    def findIngredients(self):
        foodId = self.getId()
        stmt = text("SELECT Ingredient.id, Ingredient.name FROM Ingredient"
                    " JOIN Ingredients ON Ingredients.ingredient_id = Ingredient.id"
                    " WHERE Ingredients.food_id = :food_id" ).params(food_id=foodId)
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
                   " WHERE Ingredients.ingredient_id = :ingredient_id"
                   " AND Ingredients.food_id = :self_id").params(ingredient_id=ingredient_id, self_id=self.id)
        db.engine.execute(stmt)

    def addIngredient(self, ingredient_id):
        stmt = text("INSERT INTO Ingredients (food_id, ingredient_id)"
                    "VALUES (:food_id, :ingredient_id)").params(food_id=self.id, ingredient_id=ingredient_id)
        db.engine.execute(stmt)

    @staticmethod
    def delete_food(food_id):
        f = Food.query.get(food_id)
        i = f.findIngredients()
        for ingredient in i:
            f.deleteIngredient(ingredient['id'])
            
            amount = Ingredient.findIngredientCount(ingredient['id'])
            if amount == 0:
                Ingredient.query.filter_by(id=ingredient['id']).delete()
            
            db.session().commit()
    
        Like.query.filter_by(food_id=f.id).delete()

        Food.query.filter(Food.id == food_id).delete()

        db.session().commit()

    @staticmethod
    def getFoodCount():
        stmt = text("SELECT Food.account_id, COUNT(*) AS foods FROM Food"
                    " GROUP BY Food.account_id")
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"id":row[0], "foods":row[1]})
        
        return response

    @staticmethod
    def getUsersFoods(account_id):
        stmt = text("SELECT Food.id FROM Food"
                    " WHERE Food.account_id = :account_id").params(account_id = account_id)
        res = db.engine.execute(stmt)
        response = []
        for row in res:
            response.append({"food_id":row[0]})
        
        return response

    def countLikes(self):
        res = Like.query.filter_by(food_id=self.id).all()
        total = 0
        for like in res:
            total += like.value

        return total
    
    def users_like(self):
        l = Like.query.filter_by(account_id=current_user.id, food_id=self.id).first()
        value = ""
        if l:
            if l.value == 1:
                value = "Oma tykkäys: +1"
            elif l.value == -1:
                value = "Oma tykkäys: -1"
        return value

    def get_type_name(self):
        return Type.query.get(self.type_id).name
    
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

    def getId(self):
        return self.id

    @staticmethod
    def findIngredientCount(ingredient_id):
        if not ingredient_id:
            return
        
        stmt = text("SELECT COUNT(*) FROM Ingredients"
                    " WHERE ingredient_id = :ingredient_id").params(ingredient_id=ingredient_id)
        res = db.engine.execute(stmt)
        
        response = []
        for row in res:
            response.append({"amount":row[0]})
        return response[0].get('amount')

class Like(Base):
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    value = db.Column(db.Integer, nullable=False)

    def __init__(self, food_id, account_id, value):
        self.value = value
        self.food_id = food_id
        self.account_id = account_id

class Type(Base):
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, name):
        self.name = name

    @staticmethod
    def find_type(name):
        type_id = Type.query.filter_by(name=name).first()
        if not type_id:
            food_type = Type(name)
            db.session.add(food_type)
            db.session.commit()

            return food_type.id
        return type_id.id