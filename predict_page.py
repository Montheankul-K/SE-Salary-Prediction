import streamlit as st
import pickle
import numpy as np


def load_model():
    with open("./model/saved_steps.pkl", "rb") as file:
        data = pickle.load(file)
    return data


data = load_model()

dt_regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]


def show_predict_page():
    st.title("Software Engineer Salary Prediction")
    st.write("Need some information to predict salary")

    countries_list = ('United States of America',
                      'United Kingdom of Great Britain and Northern Ireland',
                      'Australia', 'Netherlands', 'Germany', 'Sweden', 'France', 'Spain',
                      'Brazil', 'Italy', 'Canada', 'Switzerland', 'India', 'Norway',
                      'Denmark', 'Israel', 'Poland')

    education_list = ("Less than a Bachelor's degree", 'Bachelor’s degree',
                      'Master’s degree', "More than a Master's degree")

    country = st.selectbox("Country", countries_list)
    education = st.selectbox("Education", education_list)
    experience = st.slider("Years of Experience", 0, 50, 1)

    calculate = st.button("Calculate Salary")
    if calculate:
        x = np.array([[country, education, experience]])
        x[:, 0] = le_country.transform(x[:, 0])
        x[:, 1] = le_education.transform(x[:, 1])
        x = x.astype(float)

        salary = dt_regressor.predict(x)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
