import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def shorted_categories(categories, cutoff_value):
    categorical = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff_value:
            categorical[categories.index[i]] = categories.index[i]
        else:
            categorical[categories.index[i]] = "Other"
    return categorical


def clean_year_code(year_code):
    if year_code == "Less than 1 year":
        return 0.5
    if year_code == "More than 50 years":
        return 50
    return float(year_code)


def clean_education(edu):
    if "Bachelor’s degree" in edu:
        return "Bachelor’s degree"
    if "Master’s degree" in edu:
        return "Master’s degree"
    if "Professional degree" in edu:
        return "More than a Master's degree"
    return "Less than a Bachelor's degree"


@st.cache_data
def load_data():
    df = pd.read_csv("./data/survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCode",
             "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorted_categories(
        df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)

    upper_limit = df["Salary"].quantile(0.99)
    lower_limit = df["Salary"].quantile(0.01)
    df = df[df["Salary"].between(lower_limit, upper_limit)]
    df = df[df["Country"] != "Other"]

    df["YearsCode"] = df["YearsCode"].apply(clean_year_code)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)

    df["Country"] = df["Country"].replace(
        {"United States of America": "United States", "United Kingdom of Great Britain and Northern Ireland": "United Kingdom"})
    return df


df = load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salary")
    st.write("Stack Overflow Software Engineer Survey 2022")

    st.write("#### Fulltime Software Engineer by Country")
    data = df.groupby(["Country"])[
        "Salary"].count().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("#### Mean Salary base on Country")
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write("#### Mean Salary base on Experience")
    data = df.groupby(["YearsCode"])[
        "Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)
