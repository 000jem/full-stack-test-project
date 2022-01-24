from ast import Pass
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user, logout_user

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'FIRSTDIGITALFINANCE'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class LoginForm(FlaskForm):
    form_username = StringField('username', validators=[InputRequired(), Length(min=4,max=32)])
    form_password = PasswordField('password', validators=[InputRequired(), Length(min=8,max=32)])

class RegisterForm(FlaskForm):
    form_username = StringField('username', validators=[InputRequired(), Length(min=4,max=32)])
    form_password = PasswordField('password', validators=[InputRequired(), Length(min=8,max=32)])



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(16), nullable=False)
    step1 = db.Column(db.String(50), default="")
    step2 = db.Column(db.String(50), default="")
    step3 = db.Column(db.String(50), default="")

    def __repr_(self):
        return f'User: {self.id} {self.username}'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.form_username.data).first()
        print(form.form_username.data)
        print(user)
        if user:
            if user.password == form.form_password.data:
                login_user(user)

                if user.step1 == "":
                    return redirect(url_for('step1'))
                elif user.step2 == "":
                    return redirect(url_for('step2'))
                elif user.step3 == "":
                    return redirect(url_for('step3'))
                else:
                    return redirect(url_for('index'))
                #return redirect(url_for('landing')) 
        return '<h1>Invalid username or password!</h1>'

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.form_username.data,password=form.form_password.data) 

        
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/login')
        except:
            return 'Error registering that user.'

    return render_template('register.html', form=form)

@app.route('/', methods=['POST','GET'])
@login_required
def index():
        return render_template('index.html', user=current_user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/age')
def step1():
    return render_template('step1.html', user=current_user)

@app.route('/pet')
def step2():
    return render_template('step2.html', user=current_user)

@app.route('/dream')
def step3():
    return render_template('step3.html', user=current_user)

@app.route('/edit/age', methods=['POST','GET'])
def edit1():
    if request.method == 'POST':    
        current_user.step1 = request.form['age']
    try: 
        db.session.commit()
        return redirect(url_for('step2'))
    except:
        return 'Error occured while updating age.'

@app.route('/edit/pet', methods=['POST','GET'])
def edit2():
    if request.method == 'POST':    
        current_user.step2 = request.form['pet']
    try: 
        db.session.commit()
        return redirect(url_for('step3'))
    except:
        return 'Error occured while updating pet.'

@app.route('/edit/dream', methods=['POST','GET'])
def edit3():
    if request.method == 'POST':    
        current_user.step3 = request.form['dream']
    try: 
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return 'Error occured while updating dream.'



if __name__ == "__main__":
    app.run(debug=True)
