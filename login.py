import streamlit as st
from firebase_admin import auth
from firebase_config import db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def login():
    st.header('Login')
    
    with st.form("login_form"):
        email = st.text_input('Email', placeholder='Enter Your Email')
        password = st.text_input('Password', placeholder='Enter Your Password', type='password')
        
        submitted = st.form_submit_button("Login")
        
        if submitted:
            if not email or not password:
                st.error('Both email and password are required.')
            else:
                try:
                    user = auth.get_user_by_email(email)
                    logger.info(f"User found: {user.uid}")
                    
                    # Get user role from Firestore
                    user_doc = db.collection('users').document(user.uid).get()
                    if user_doc.exists:
                        user_data = user_doc.to_dict()
                        role = user_data.get('role', 'staff')  # Default to staff if role not found
                    else:
                        role = 'staff'  # Default role
                    
                    st.session_state['user'] = user
                    st.session_state['role'] = role
                    st.session_state['page'] = 'staff' if role == 'staff' else 'admin'
                    st.success('Logged in successfully')
                    st.rerun()
                except auth.UserNotFoundError:
                    logger.warning(f"User not found for email: {email}")
                    st.error('Invalid email or password')
                except Exception as e:
                    logger.error(f"Error during login: {str(e)}")
                    st.error(f'An error occurred: {str(e)}')