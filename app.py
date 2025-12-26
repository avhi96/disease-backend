from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pickle
import numpy as np
import random
import smtplib
import os
from email.message import EmailMessage
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

from data.hospitals import get_best_hospitals
from utils.location import detect_location
from services.hospital_service import resolve_hospitals

load_dotenv()

# ---------------- HOSPITAL DATA ----------------

def calculate_age_risk(age):
    if age is None:
        return "Unknown"
    if age < 30:
        return "Low"
    elif age < 50:
        return "Medium"
    else:
        return "High"


# ---------------- APP CONFIG ----------------

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODELS ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    age = db.Column(db.Integer)
    location = db.Column(db.String(100))

    is_verified = db.Column(db.Boolean, default=False)
    otp = db.Column(db.String(6))
    otp_expiry = db.Column(db.DateTime)


class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    disease = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(50), nullable=False)

# ---------------- LOAD MODELS ----------------

with open("models/diabetes_model.pkl", "rb") as f:
    diabetes_model = pickle.load(f)

with open("models/heart_model.pkl", "rb") as f:
    heart_model = pickle.load(f)

with open("models/kidney_model.pkl", "rb") as f:
    kidney_model = pickle.load(f)

with open("models/liver_model.pkl", "rb") as f:
    liver_model = pickle.load(f)

# ---------------- HELPERS ----------------

def age_risk(age):
    if age is None:
        return "Unknown"
    if age < 30:
        return "Low Risk"
    elif age < 45:
        return "Moderate Risk"
    elif age < 60:
        return "High Risk"
    return "Very High Risk"


def hospital_map_link(hospital, location):
    query = f"{hospital} {location}"
    return f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

# ---------------- AUTH ROUTES ----------------

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    if User.query.filter(
        (User.username == data["username"]) |
        (User.email == data["email"])
    ).first():
        return jsonify({"message": "User already exists"}), 400

    otp = str(random.randint(100000, 999999))

    user = User(
        username=data["username"],
        email=data["email"],
        password=generate_password_hash(data["password"]),
        age=data.get("age"),
        location=data.get("location"),
        otp=otp,
        otp_expiry=datetime.now() + timedelta(minutes=5),
        is_verified=False
    )

    db.session.add(user)
    db.session.commit()

    msg = EmailMessage()
    msg["Subject"] = "Verify Your Email"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = user.email
    msg.set_content(f"Your OTP is: {otp}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)

    return jsonify({"message": "Signup successful. OTP sent"})


@app.route("/verify-email", methods=["POST"])
def verify_email():
    data = request.get_json()
    user = User.query.filter_by(email=data["email"], otp=data["otp"]).first()

    if not user or user.otp_expiry < datetime.now():
        return jsonify({"message": "Invalid or expired OTP"}), 400

    user.is_verified = True
    user.otp = None
    user.otp_expiry = None
    db.session.commit()

    return jsonify({"message": "Email verified"})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter(
        (User.username == data["identifier"]) |
        (User.email == data["identifier"])
    ).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    if not user.is_verified:
        return jsonify({"message": "Verify email first"}), 403

    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "age": user.age,
        "location": user.location
    })

# ---------------- FORGOT PASSWORD ----------------

@app.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    if not user:
        return jsonify({"message": "Email not found"}), 404

    otp = str(random.randint(100000, 999999))
    user.otp = otp
    user.otp_expiry = datetime.now() + timedelta(minutes=5)
    db.session.commit()

    msg = EmailMessage()
    msg["Subject"] = "Password Reset OTP"
    msg["From"] = os.getenv("EMAIL_USER")
    msg["To"] = user.email
    msg.set_content(f"OTP: {otp}")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASS"))
        smtp.send_message(msg)

    return jsonify({"message": "OTP sent"})


@app.route("/reset-password", methods=["POST"])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(
        email=data["email"],
        otp=data["otp"]
    ).first()

    if not user or user.otp_expiry < datetime.now():
        return jsonify({"message": "Invalid or expired OTP"}), 400

    user.password = generate_password_hash(data["new_password"])
    user.otp = None
    user.otp_expiry = None
    db.session.commit()

    return jsonify({"message": "Password reset successful"})

# ---------------- PREDICTIONS ----------------

def prediction_response(user, disease, result):
    location = detect_location(request.remote_addr)

    hospitals = resolve_hospitals(
        disease=disease,
        lat=location["lat"],
        lng=location["lng"],
        fallback_location=location["city"] or user.location or "India"
    )

    return {
        "prediction": result,
        "age": user.age,
        "risk": age_risk(user.age),
        "city": location["city"],
        "state": location["state"],
        "hospitals": hospitals
    }

@app.route("/predict/diabetes", methods=["POST"])
def predict_diabetes():
    data = request.get_json()

    user = db.session.get(User, data.get("user_id"))
    if not user:
        return jsonify({"message": "User not found"}), 404

    try:
        features = np.array([
            data["Pregnancies"],
            data["Glucose"],
            data["BloodPressure"],
            data["SkinThickness"],
            data["Insulin"],
            data["BMI"],
            data["DiabetesPedigreeFunction"],
            data["Age"]
        ]).reshape(1, -1)
    except KeyError as e:
        return jsonify({"message": f"Missing field: {str(e)}"}), 400

    prediction = diabetes_model.predict(features)[0]
    result = "Diabetic" if prediction == 1 else "Not Diabetic"

    db.session.add(
        PredictionHistory(
            user_id=user.id,
            disease="Diabetes",
            result=result
        )
    )
    db.session.commit()

    return jsonify(
        prediction_response(user, "Diabetes", result)
    )

@app.route("/predict/heart", methods=["POST"])
def predict_heart():
    data = request.get_json()
    user = db.session.get(User, data["user_id"])

    features = np.array(list(data["features"])).reshape(1, -1)
    result = "Heart Disease Detected" if heart_model.predict(features)[0] == 1 else "No Heart Disease"

    db.session.add(PredictionHistory(user_id=user.id, disease="Heart", result=result))
    db.session.commit()

    return jsonify(prediction_response(user, "Heart", result))


@app.route("/predict/kidney", methods=["POST"])
def predict_kidney():
    data = request.get_json()
    user = db.session.get(User, data["user_id"])

    features = np.array(list(data["features"])).reshape(1, -1)
    result = "Kidney Disease Detected" if kidney_model.predict(features)[0] == 1 else "No Kidney Disease"

    db.session.add(PredictionHistory(user_id=user.id, disease="Kidney", result=result))
    db.session.commit()

    return jsonify(prediction_response(user, "Kidney", result))


@app.route("/predict/liver", methods=["POST"])
def predict_liver():
    data = request.get_json()
    user = db.session.get(User, data["user_id"])
    
    features = np.array(list(data["features"])).reshape(1, -1)
    result = "Liver Disease Detected" if liver_model.predict(features)[0] == 1 else "No Liver Disease"

    db.session.add(PredictionHistory(user_id=user.id, disease="Liver", result=result))
    db.session.commit()

    return jsonify(prediction_response(user, "Liver", result))

# ---------------- HISTORY ----------------

@app.route("/history/<int:user_id>")
def history(user_id):
    data = PredictionHistory.query.filter_by(user_id=user_id).all()
    return jsonify([
        {"disease": h.disease, "result": h.result}
        for h in data
    ])

# ---------------- RUN ----------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
