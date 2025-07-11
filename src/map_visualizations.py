import streamlit as st
import pandas as pd
import plotly.express as px

def create_tree_location_map(df):
    """
    Goal is to create an interactive map that shows tree planting locations with hover details. 
    This function will assume that df has 'Latitude', 'Longitude', '# Trees To Be Planted', 'Organization Name' columns.
    """
    if df is None: 
        st.warning("No data provided to create the map.")
        return
    # will need to make sure that Trees To Be Planted is Numeric 
    # creating the df with just the relevant columns

    map_df = df.dropna(subset = ['Latitude', 'Longitude', '# Trees To Be Planted', 'Organization Name']).copy()
    # to ensure '# Trees To Be Planted' is numeric, coercing errors to NaN and filling with 0
    map_df['# Trees To Be Planted'] = pd.to_numeric(map_df['# Trees To Be Planted'], errors='coerce').fillna(0)

    if not map_df.empty:
        fig = px.scatter_mapbox(map_df,
                                lat = "Latitude", 
                                lon = "Longitude",
                                color = "# Trees To Be Planted",
                                size = "# Trees To Be Planted", 
                                hover_name = "Organization Name", # this will show the org name on hover
                                hover_data = {'# Trees To Be Planted': True,
                                              'Project Address': True,
                                              'Latitude': False, # hiding the lat/lon
                                              'Longitude': False},
                                zoom = 3,
                                mapbox_style = "carto-positron", 
                                title = "Tree Planting Locations & Quantities"
                                )
        fig.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
        fig.update_coloraxes(colorbar_title = "Trees Planted")

        st.plotly_chart(fig, use_container_width = True)
    else:
        st.warning("No valid lat/lon, organization name, or tree count to disply on map.")

