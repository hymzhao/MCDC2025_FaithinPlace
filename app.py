# app.py
import streamlit as st
import pandas as pd 

st.set_page_config(layout="wide")

st.title("My Faith in Place Dashboard")
st.write("Welcome to the dashboard!")

# Load data (ensure Geocoded_MCDC-Sample-Info.csv is in the same directory)
try:
    df = pd.read_csv('Geocoded_MCDC-Sample-Info.csv')
    st.dataframe(df)
except FileNotFoundError:
    st.error("Please place 'Geocoded_MCDC-Sample-Info.csv' in the same folder as app.py")