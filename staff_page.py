import streamlit as st
from prediction_functions import diabetes_prediction, heart_disease_prediction, parkinsons_prediction, anemia_prediction, hiv_prediction, typhoid_prediction, breast_cancer_prediction, generate_patient_diagnosis_report
from user_functions import view_prediction_history, generate_charts

def staff_page():
    st.title('Staff Dashboard')
    with st.sidebar:
        st.image("/Users/user/Documents/Tutorials/machineLearning/multiple-disease-prediction-streamlit-app-main/multipleDiseaseProject/addfeatures/atu.png", width=150, use_column_width=True)
        
        st.subheader(f'Welcome {st.session_state.user.display_name or st.session_state.user.email}')
        
        selected = st.selectbox('Select Function',
                                ['Diabetes Prediction',
                                 'Heart Disease Prediction',
                                 'Parkinsons Prediction',                             
                                 'HIV Prediction',
                                 'Anemia Prediction',
                                 'Typhoid Prediction',
                                 'Patient Diagnosis Report',
                                 #'Breast Cancer Prediction',
                                 'Prediction History',
                                 'Prediction Analytics'])
        
        if st.button('Logout'):
            st.session_state.clear()
            st.rerun()
    
    if selected == 'Diabetes Prediction':
        diabetes_prediction()
    elif selected == 'Heart Disease Prediction':
        heart_disease_prediction()
    elif selected == 'Parkinsons Prediction':
        parkinsons_prediction()
    elif selected == 'Anemia Prediction':
        anemia_prediction()
    elif selected == 'HIV Prediction':
        hiv_prediction()
    elif selected == 'Typhoid Prediction':
        typhoid_prediction()
    #elif selected == 'Breast Cancer Prediction':
        #breast_cancer_prediction()
    elif selected == 'Patient Diagnosis Report':
        generate_patient_diagnosis_report()
    elif selected == 'Prediction History':
        view_prediction_history()
    elif selected == 'Prediction Analytics':
        generate_charts(st.session_state.user.uid)