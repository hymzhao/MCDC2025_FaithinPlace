import pandas as pd
import streamlit as st

@st.cache_data
def load_project_data(file_path):
    """
    Goal is to load the project data from a csv file and perform initial cleaning.
    """
    try:
        df = pd.read_csv(file_path)
        # Convert columns to numeric, coercing errors to NaN and filling with 0 for tree count
        if 'Latitude' in df.columns:
            df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
        if 'Longitude' in df.columns:
            df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
        if '# Trees To Be Planted' in df.columns:
            df['# Trees To Be Planted'] = pd.to_numeric(df['# Trees To Be Planted'], errors='coerce').fillna(0).astype(int)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{file_path}' was not found. Please ensure it's in the correct path (e.g., 'data/Geocoded_MCDC-Sample-Info.csv').")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading or processing data: {e}")
        return None