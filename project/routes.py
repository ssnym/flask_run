from project import app, db
from flask import render_template, redirect, url_for, flash, request
from project.models import Item, User
from project.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user , login_required, current_user

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/profile/')
def profile_page():
    username = current_user
    return render_template('file_3_profile.html', username = username)

@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    
    sell_form = SellItemForm()
    
    if request.method == "POST":
        # Purchase item logic
        purchased_item = request.form.get('purchased_item')
        p_item_obj = Item.query.filter_by(name=purchased_item).first()
        if p_item_obj:
            if current_user.can_purchase(p_item_obj):
                p_item_obj.buy(current_user)
                flash(f'Item Purchased : {p_item_obj.name} for {p_item_obj.display_price}', category='success')
            else:
                flash(f"Can't purchase {p_item_obj.name}", category='danger')
                
        # Sell item logic
        sell_item = request.form.get('sell_item')
        s_item_obj = Item.query.filter_by(name=sell_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f'Congrats, {s_item_obj.name} sold!', category='success')                
            else:
                flash(f"Can't sell {s_item_obj.name}", category='danger')
        

        return redirect(url_for('market_page'))
    
    # GET request
    items = Item.query.filter_by(owner=None)
    owned_items = Item.query.filter_by(owner = current_user.id)
    return render_template('market.html', items=items, purchase_form=purchase_form, owned_items = owned_items, sell_form = sell_form)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        
        print("Form validated successfully!")  # Debug line   
        
        user_to_create = User(username=form.username.data, 
                              email_address = form.email_address.data,
                              password = form.password_1.data)
        db.session.add(user_to_create)
        db.session.commit()
        
        login_user(user_to_create)    
        flash(f'Account created successfully! You are logged in as {user_to_create.username}', category='success')
        return redirect( url_for('market_page'))
        
        
    else:
        print("Form validation failed:")  # Debug line
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
        
    return render_template('register.html', form = form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    
    form = LoginForm()
    
    if form.validate_on_submit():
        
        attempted_user = User.query.filter_by(username = form.username.data).first()
        
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password_entered.data):
            
            login_user(attempted_user)    
              
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            
            return redirect(url_for('market_page'))
        
        else:
            flash('Wrong Username - Password', category='danger')
            
    else:
        for err_msg in form.errors.values():
            flash(err_msg, category='danger')
        
    return render_template('login.html', form=form)


@app.route('/logout')
# @login_required
def logout_page():
    logout_user()
    flash('Your are logged out!', category='info')
    return redirect( url_for('home_page') )
    