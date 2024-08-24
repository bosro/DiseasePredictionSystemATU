import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate('/Users/user/documents/tutorials/machinelearning/multiple-disease-prediction-streamlit-app-main/multipleDiseaseProject/addfeatures/config/firebase_credentials.json')
        firebase_admin.initialize_app(cred)
    return firestore.client()

# Initialize Firebase and get Firestore client
db = initialize_firebase()