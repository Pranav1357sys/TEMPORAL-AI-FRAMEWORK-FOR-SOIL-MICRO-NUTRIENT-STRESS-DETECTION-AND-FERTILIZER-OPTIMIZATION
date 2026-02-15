from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)
app.secret_key = 'secret123'

# -----------------------
# Database Config
# -----------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# -----------------------
# Database Models
# -----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(50))   # 'nutrition' or 'fertilizer'
    input_data = db.Column(db.String)
    result = db.Column(db.String)

with app.app_context():
    db.create_all()

# -----------------------
# Load Models & Encoders
# -----------------------
fertility_model = pickle.load(open('models/model.pkl', 'rb'))
fertilizer_model = pickle.load(open('models/model1.pkl', 'rb'))

le_Name = pickle.load(open('encoders/le_Name.pkl', 'rb'))
le_Fertility = pickle.load(open('encoders/le_Fertility.pkl', 'rb'))
le_Photoperiod = pickle.load(open('encoders/le_Photoperiod.pkl', 'rb'))
le_Category_pH = pickle.load(open('encoders/le_Category_pH.pkl', 'rb'))
le_Soil_Type = pickle.load(open('encoders/le_Soil_Type.pkl', 'rb'))
le_Season = pickle.load(open('encoders/le_Season.pkl', 'rb'))

le_soil = pickle.load(open('encoders/le_soil.pkl', 'rb'))
le_crop = pickle.load(open('encoders/le_crop.pkl', 'rb'))
le_fert = pickle.load(open('encoders/le_fert.pkl', 'rb'))

# -----------------------
# Routes
# -----------------------

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

# ---- Register ----
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        if User.query.filter_by(username=username).first():
            return "User already exists!"
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

# ---- Login ----
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid Credentials!"
    return render_template('login.html')

# ---- Logout ----
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# ---- Home ----
@app.route('/home')
def home():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

# ---- Nutrition Prediction ----
@app.route('/nutrition', methods=['GET','POST'])
def nutrition():
    if 'user' not in session:
        return redirect(url_for('login'))

    # Get dropdown options from LabelEncoders
    name_options = le_Name.classes_
    photoperiod_options = le_Photoperiod.classes_
    category_ph_options = le_Category_pH.classes_
    soil_type_options = le_Soil_Type.classes_
    season_options = le_Season.classes_

    result = None
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            input_features = [
                le_Name.transform([data['Name']])[0],
                le_Photoperiod.transform([data['Photoperiod']])[0],
                float(data['Temperature']),
                float(data['Rainfall']),
                float(data['pH']),
                float(data['Light_Hours']),
                float(data['Light_Intensity']),
                float(data['Rh']),
                float(data['Nitrogen']),
                float(data['Phosphorus']),
                float(data['Potassium']),
                float(data['Yield']),
                le_Category_pH.transform([data['Category_pH']])[0],
                le_Soil_Type.transform([data['Soil_Type']])[0],
                le_Season.transform([data['Season']])[0],
                float(data['N_Ratio']),
                float(data['P_Ratio']),
                float(data['K_Ratio'])
            ]
            pred = fertility_model.predict([input_features])[0]
            result = le_Fertility.inverse_transform([pred])[0]

            # Save to history
            history = PredictionHistory(
                username=session['user'],
                type='nutrition',
                input_data=str(data),
                result=result
            )
            db.session.add(history)
            db.session.commit()
        except Exception as e:
            return f"Error: {e}"

    return render_template('nutrition.html', 
                           result=result, 
                           name_options=name_options,
                           photoperiod_options=photoperiod_options,
                           category_ph_options=category_ph_options,
                           soil_type_options=soil_type_options,
                           season_options=season_options)

# ---- Fertilizer Prediction ----
@app.route('/fertilizer', methods=['GET','POST'])
def fertilizer():
    if 'user' not in session:
        return redirect(url_for('login'))

    soil_options = le_soil.classes_
    crop_options = le_crop.classes_

    result = None
    if request.method == 'POST':
        data = request.form.to_dict()
        try:
            input_features = [
                float(data['Temparature']),
                float(data['Humidity']),
                float(data['Moisture']),
                le_soil.transform([data['Soil_Type']])[0],
                le_crop.transform([data['Crop_Type']])[0],
                float(data['Nitrogen']),
                float(data['Potassium']),
                float(data['Phosphorous'])
            ]
            pred = fertilizer_model.predict([input_features])[0]
            result = le_fert.inverse_transform([pred])[0]

            # Save to history
            history = PredictionHistory(
                username=session['user'],
                type='fertilizer',
                input_data=str(data),
                result=result
            )
            db.session.add(history)
            db.session.commit()
        except Exception as e:
            return f"Error: {e}"

    return render_template('fertilizer.html', result=result,
                           soil_options=soil_options, crop_options=crop_options)

# ---- Prediction History ----
@app.route('/history')
def history():
    if 'user' not in session:
        return redirect(url_for('login'))
    user_history = PredictionHistory.query.filter_by(username=session['user']).all()
    return render_template('history.html', history=user_history)


if __name__ == '__main__':
    app.run(debug=True)
