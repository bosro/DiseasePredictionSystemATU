import streamlit as st
from admin_functions import manage_database, view_overall_predictions, generate_admin_reports

def admin_page():
    st.title('Admin Dashboard')

    with st.sidebar:
        st.image("/Users/user/Documents/Tutorials/machineLearning/multiple-disease-prediction-streamlit-app-main/multipleDiseaseProject/addfeatures/atu.png", width=150, use_column_width=True)
        
        st.subheader(f'Welcome Admin {st.session_state.user.display_name or st.session_state.user.email}')
        
        selected = st.selectbox('Select Function',
                                ['Manage Database',
                                 'View Overall Predictions',
                                 'Generate Admin Reports'])
        
        if st.button('Logout'):
            st.session_state.clear()
            st.rerun()

    if selected == 'Manage Database':
        manage_database()
    elif selected == 'View Overall Predictions':
        view_overall_predictions()
    elif selected == 'Generate Admin Reports':
        generate_admin_reports()