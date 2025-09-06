from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateTimeField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from project.models import User


class RegisterForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist! Please try a different username')
        
    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address = email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email Address already exists! Please try a different email address')
        

    username = StringField(label='User Name:', validators=[Length(min=3, max=25), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password_1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password_2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password_1'), DataRequired()])
    
    submit = SubmitField(label='Create Account')
    
    
class LoginForm(FlaskForm):
    
    username = StringField(label = 'User Name:', validators = [DataRequired()])
    password_entered = PasswordField(label='Password:', validators=[DataRequired()])
    
    login_btn = SubmitField(label='Sign In')
    
    
class PurchaseItemForm(FlaskForm):
    
    submit = SubmitField(label='Purchase Item')
    

class SellItemForm(FlaskForm):
    
    submit = SubmitField(label='Sell Item')
    