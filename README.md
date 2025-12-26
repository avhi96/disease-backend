# Disease Prediction System (ML + Flask + React)

A **college-level full‑stack project** that predicts diseases based on user symptoms and medical parameters using **Machine Learning**, with secure authentication, email verification, and prediction history.

---

## Project Overview

This project helps users:

* Create an account with **email verification (OTP)**
* Log in securely
* Predict diseases using ML models
* Get **hospital recommendations** based on disease
* View **prediction history**
* Reset password using **email OTP**

It is designed for **academic purposes** and backend code review by professors.

---

## Diseases Covered

1. **Diabetes**
2. **Heart Disease**
3. **Kidney Disease**
4. **Liver Disease**

Each disease uses a separate ML model trained on standard datasets.

---

## Tech Stack

### Backend

* Python
* Flask
* Flask‑SQLAlchemy
* SQLite (database)
* scikit‑learn (ML models)
* SMTP (Gmail) for OTP emails

### Frontend (planned)

* React.js

### ML Algorithms

* Logistic Regression

---

## Authentication Features

* Signup with **email + username**
* **Email verification using OTP**
* Secure password hashing
* Login blocked until email is verified
* Forgot password with **email OTP reset**

---

## Hospital Recommendation

After prediction, the system suggests **relevant hospitals** based on disease type using a predefined list (college‑level implementation).

---

## Prediction History

* Each prediction is saved with:

  * User ID
  * Disease name
  * Prediction result
* Users can fetch their full prediction history

---

## API Endpoints

### 🔹 Basic

* `GET /` → Server status

### 🔹 Authentication

* `POST /signup`
* `POST /verify-email`
* `POST /login`

### 🔹 Forgot Password

* `POST /forgot-password`
* `POST /verify-otp`
* `POST /reset-password`

### 🔹 Disease Prediction

* `POST /predict/diabetes`
* `POST /predict/heart`
* `POST /predict/kidney`
* `POST /predict/liver`

### 🔹 History

* `GET /history/<user_id>`

---

## Datasets Used

* **Diabetes:** Pima Indians Diabetes Dataset
* **Heart Disease:** UCI Heart Disease Dataset
* **Kidney Disease:** Chronic Kidney Disease Dataset
* **Liver Disease:** Indian Liver Patient Dataset

(All datasets are commonly used for academic projects.)

---

## How to Run the Project (Backend)

1. Install dependencies:

```bash
pip install flask flask-sqlalchemy scikit-learn python-dotenv werkzeug
```

2. Create `.env` file:

```env
EMAIL_USER=yourgmail@gmail.com
EMAIL_PASS=your_gmail_app_password
```

3. Run server:

```bash
python app.py
```

---

## Viva / Professor Explanation (Short)

> “This project uses machine learning models to predict diseases based on user input. Flask APIs handle authentication, prediction, and history management. Email OTP is used for verification and password recovery. SQLite is used as the database, and models are trained using Logistic Regression.”

---

## Notes

* Free hosting platforms can be used (Render / Vercel)
* Free hosting may have limitations (sleep time, limited requests)
* This project is intended for **academic demonstration**, not medical diagnosis

---

##  Developer

* **Project Type:** College / Academic Project
* **Backend:** Fully manual & professor‑review ready

---

 **All backend APIs tested and working successfully**

---

### If you are reviewing this project:

This system demonstrates practical use of **ML + backend development + security concepts** in a real‑world style application.

```
disease_prediction_backend
├─ .env
├─ app.py
├─ data
│  ├─ hospitals.py
│  └─ __pycache__
│     └─ hospitals.cpython-313.pyc
├─ instance
│  └─ users.db
├─ models
│  ├─ diabetes_model.pkl
│  ├─ heart_model.pkl
│  ├─ kidney_model.pkl
│  └─ liver_model.pkl
├─ README.md
├─ services
│  ├─ google_places.py
│  ├─ hospital_service.py
│  └─ __pycache__
│     ├─ google_places.cpython-313.pyc
│     └─ hospital_service.cpython-313.pyc
├─ training
│  ├─ model_train_diabetes.py
│  ├─ model_train_heart.py
│  ├─ model_train_kidney.py
│  └─ model_train_liver.py
└─ utils
   ├─ location.py
   ├─ maps.py
   └─ __pycache__
      ├─ location.cpython-313.pyc
      └─ maps.cpython-313.pyc

```