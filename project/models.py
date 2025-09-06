from project import db
from project import bcrypt
from project import login_manager

from flask_login import UserMixin

# User-Loader callback - (used to reload the user object from the user ID stored in the session)
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=50), nullable=False, unique=True)
    email_address = db.Column(db.String(length=40), nullable=False, unique=True)    
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=100000)
    
    # Relationship : User -> Item : Item.owned_user = <owner user name>
    items = db.relationship('Item', backref='owned_user', lazy=True)
    
    # Dunder __repr__
    def __repr__(self):
        return f'User : {self.username}'
    
    # Getter - to get the password stored
    @property
    def password(self):
        raise AttributeError("Password is write-only.")
    
    # Setter - to store HASH password into DB from the plain text password (During Register)
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
        
    # To check whether entered password is correct or not (During Sign In)
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
    
    # Can Purchas the item if the item's price is lower than User's budget
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    # Can current logged-in user sell a given item
    def can_sell(self, item_obj):
        return item_obj in self.items
    
    # Getter - to display budget properly
    @property
    def display_budget(self):
       
        if len(str(self.budget)) <=3:
            # 999
            return f'₹ {self.budget}'
        elif len(str(self.budget)) <=5:
            # 99 999 to 1 000
            return f'₹ {str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        elif len(str(self.budget)) <=7:
            # 99 99 999 to 1 00 000
            return f'₹ {str(self.budget)[:-5]},{str(self.budget)[-5:-3]},{str(self.budget)[-3:]}'
        else :
            # 1 00 00 000 to 99 99 99 999
            return f'₹ {str(self.budget)[:-7]},{str(self.budget)[-7:-5]},{str(self.budget)[-5:-3]},{str(self.budget)[-3:]}'

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=True, unique=True)
    
    # Foreign Key Relationship
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    
    # Dunder __repr__
    def __repr__(self):
        return f'Item {self.name} : {self.barcode}'
    
    # Function when user buy a object from the market_place
    def buy(self, user):
        self.owner = user.id 
        user.budget -= self.price
        db.session.commit()
        
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
    
    @property
    def display_price(self):
       
        if len(str(self.price)) <=3:
            # 999
            return f'₹ {self.price}'
        elif len(str(self.price)) <=5:
            # 99 999 to 1 000
            return f'₹ {str(self.price)[:-3]},{str(self.price)[-3:]}'
        elif len(str(self.price)) <=7:
            # 99 99 999 to 1 00 000
            return f'₹ {str(self.price)[:-5]},{str(self.price)[-5:-3]},{str(self.price)[-3:]}'
        else :
            # 1 00 00 000 to 99 99 99 999
            return f'₹ {str(self.price)[:-7]},{str(self.price)[-7:-5]},{str(self.price)[-5:-3]},{str(self.price)[-3:]}'
    


# with app.app_context():
#     db.create_all()

#  with app.app_context():
#     User.__table__.drop(db.engine)

# with app.app_context():
#     User.__table__.create(db.engine)

