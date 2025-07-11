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
        # Define the custom hover text as a single string
        # Plotly's hovertemplate uses specific syntax for custom data: %{customdata[index]}
        fig = px.scatter_mapbox(
            map_df,
            lat="Latitude",
            lon="Longitude",
            size="# Trees To Be Planted",
            hover_name="Organization Name", 
            custom_data=[map_df['Organization Name'],
                         map_df['Project Location City'],
                         map_df['Project Location State'],
                         map_df['# Trees To Be Planted']], # Pass the data you want in custom_data
            zoom=4,
            mapbox_style="carto-positron",
            size_max=30,
            color_discrete_sequence=["#2ca02c"]  # solid green color
        )

        # Customizing the hovertemplate
        # %{hover_name} refers to the column passed to hover_name (Organization Name in this case)
        # %{customdata[0]} refers to the first item in custom_data (Organization Name again, or you can skip it if hover_name is sufficient)
        # %{customdata[1]} refers to City
        # %{customdata[2]} refers to State
        # %{customdata[3]} refers to # Trees To Be Planted
        fig.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"  # Organization Name, bold
                "City, State: %{customdata[1]}, %{customdata[2]}<br>"
                "Number of Trees to be Planted: %{customdata[3]}"
                "<extra></extra>" # This removes the default "trace" info
            )
        )

        # Center the map over the Midwest
        fig.update_layout(
            mapbox_center={"lat": 41.8, "lon": -88.0},  # Illinois-ish
            margin={"r":0, "t":40, "l":0, "b":0},
            title="Tree Planting Locations in the Midwest"
        )


        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valid data to display on map.")


