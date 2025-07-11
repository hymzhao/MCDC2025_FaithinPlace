# app.py
import streamlit as st
import pandas as pd 

# import functions from src modules
from src.data_cleaner import load_project_data
from src.map_visualizations import create_tree_location_map

st.set_page_config(layout = 'wide')

st.title("MCDC Faith in Place 2025")

if "page" not in st.session_state:
    st.session_state.page = "Project Overview"

st.sidebar.header("Navigation")
page = st.sidebar.markdown("### Go to")

# Navigation buttons
if st.sidebar.button("Project Overview"):
    st.session_state.page = "Project Overview"

if st.sidebar.button("Tree Planting Map"):
    st.session_state.page = "Tree Planting Map"

# Load data 
df = load_project_data("data/Geocoded_MCDC-Sample-Info.csv")

# Render pages
if st.session_state.page == "Project Overview":
    st.header("Project Overview and Motivation")
    st.write("Background Context")

    if df is not None:
        st.subheader("Raw Data Snippet")
        st.dataframe(df)

elif st.session_state.page == "Tree Planting Map":
    st.header("Tree Planting Map")

    if df is not None:
        create_tree_location_map(df)
        st.subheader("Species Diversity")
        st.info("Species diversity chart will be integrated here after parsing Project Description")

st.write("More dashboards and detailed metrics will be integrated here as our project progresses.")