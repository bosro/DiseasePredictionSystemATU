import streamlit as st
from firebase_admin import auth, credentials
from firebase_config import db
import logging
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# You'll need to set this to your Firebase project's web API key
FIREBASE_WEB_API_KEY = "AIzaSyDMv4uvjb9Igjl-m8q54H7Xmvz8PExs6xE"

def verify_password(email, password):
    request_data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_WEB_API_KEY}"
    
    try:
        response = requests.post(rest_api_url, data=json.dumps(request_data))
        if response.ok:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error verifying password: {str(e)}")
        return False

def send_password_reset_email(email):
    request_data = {
        "requestType": "PASSWORD_RESET",
        "email": email
    }
    rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key={FIREBASE_WEB_API_KEY}"
    
    try:
        response = requests.post(rest_api_url, data=json.dumps(request_data))
        if response.ok:
            return True
        else:
            return False
    except Exception as e:
        logger.error(f"Error sending password reset email: {str(e)}")
        return False

def login():
    st.header('Login')
    
    with st.form("login_form"):
        email = st.text_input('Email', placeholder='Enter Your Email')
        password = st.text_input('Password', placeholder='Enter Your Password', type='password')
        
        col1, col2 = st.columns([1,1])
        with col1:
            submitted = st.form_submit_button("Login")
        with col2:
            forgot_password = st.form_submit_button("Forgot Password")
        
        if submitted:
            if not email or not password:
                st.error('Both email and password are required.')
            else:
                try:
                    # Verify password using Firebase Authentication REST API
                    if verify_password(email, password):
                        # If password is correct, get user data
                        user = auth.get_user_by_email(email)
                        logger.info(f"User authenticated: {user.uid}")
                        
                        # Get user role from Firestore
                        user_doc = db.collection('users').document(user.uid).get()
                        if user_doc.exists:
                            user_data = user_doc.to_dict()
                            role = user_data.get('role')
                            
                            if role not in ['admin', 'staff']:
                                logger.warning(f"Invalid role for user {user.uid}: {role}")
                                st.error('Invalid user role. Please contact an administrator.')
                                return
                            
                            # Set session state
                            st.session_state['user'] = user
                            st.session_state['role'] = role
                            st.session_state['page'] = 'admin' if role == 'admin' else 'staff'
                            
                            st.success(f'Logged in successfully as {role}')
                            st.rerun()
                        else:
                            logger.warning(f"User document not found for {user.uid}")
                            st.error('User data not found. Please contact an administrator.')
                    else:
                        st.error('Invalid email or password')
                
                except auth.UserNotFoundError:
                    logger.warning(f"User not found for email: {email}")
                    st.error('Invalid email or password')
                except Exception as e:
                    logger.error(f"Error during login: {str(e)}")
                    st.error('An error occurred during login. Please try again later.')
        
        elif forgot_password:
            if not email:
                st.error('Please enter your email address to reset your password.')
            else:
                if send_password_reset_email(email):
                    st.success('Password reset email sent. Please check your inbox.')
                else:
                    st.error('An error occurred while sending the password reset email. Please try again later.')