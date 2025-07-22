import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_tree_location_map(df):
    """
    Creates an interactive map using the cleaned species data for the hover-over.
    """
    if df is None:
        st.warning("No data provided to create the map.")
        return

    map_df = df.dropna(subset=['Latitude', 'Longitude', '# Trees To Be Planted', 'Organization Name']).copy()
    map_df['# Trees To Be Planted'] = pd.to_numeric(map_df['# Trees To Be Planted'], errors='coerce').fillna(0)

    # Use the 'Cleaned Species' column for the hover-over text
    map_df['Species List (for hover)'] = map_df['Cleaned Species'].apply(lambda x: ', '.join(x) if x else 'N/A')

    if not map_df.empty:
        fig = px.scatter_mapbox(
            map_df,
            lat="Latitude",
            lon="Longitude",
            size="# Trees To Be Planted",
            hover_name="Organization Name",
            # Update custom_data to use the cleaned species list
            custom_data=[map_df['Organization Name'],
                         map_df['Project Location City'],
                         map_df['Project Location State'],
                         map_df['# Trees To Be Planted'],
                         map_df['Species List (for hover)']],
            zoom=4,
            mapbox_style="carto-positron",
            size_max=30,
            color_discrete_sequence=["#2ca02c"]
        )

        fig.update_traces(
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "City, State: %{customdata[1]}, %{customdata[2]}<br>"
                "Number of Trees to be Planted: %{customdata[3]}<br>"
                "<b>Species:</b> %{customdata[4]}" # Make 'Species' label bold
                "<extra></extra>"
            )
        )

        fig.update_layout(
            mapbox_center={"lat": 41.8, "lon": -88.0},
            margin={"r":0, "t":40, "l":0, "b":0},
            title="Tree Planting Locations"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valid data to display on map.")

def create_species_diversity_chart(df):
    """
    Creates a bar chart using the cleaned and normalized species data.
    """
    # Use the 'Cleaned Species' column
    if df is None or 'Cleaned Species' not in df.columns:
        st.warning("Cleaned species data not available to create the diversity chart.")
        return

    # Create a flat list of all cleaned species from all projects
    all_species_list = [species for sublist in df['Cleaned Species'] for species in sublist]

    if not all_species_list:
        st.info("No species data to display in the chart for the selected filters.")
        return

    species_counts = Counter(all_species_list)
    species_df = pd.DataFrame(species_counts.items(), columns=['Species', 'Count']).sort_values(by='Count', ascending=False)

    fig = px.bar(
        species_df,
        x='Count',
        y='Species',
        orientation='h',
        title='Species Diversity Across Projects',
        labels={'Count': 'Number of Projects Planting This Species', 'Species': 'Tree Species'},
        color_discrete_sequence=px.colors.qualitative.Pastel # Using a different color scheme
    )
    fig.update_layout(
        yaxis={'categoryorder':'total ascending'}, # Show most frequent at the top
        height=max(400, len(species_df) * 25) # Dynamically adjust height
    )
    st.plotly_chart(fig, use_container_width=True)

def create_goals_wordcloud(df):
    """
    Generates and saves a word cloud from the 'Goals from Ollama' column.
    """
    if df is None or 'Goals from Ollama' not in df.columns:
        st.warning("Project goals data not available to create a word cloud.")
        return

    # Combine all goals into a single string of text
    all_goals_list = [goal for sublist in df['Goals from Ollama'] for goal in sublist]

    if not all_goals_list:
        st.info("No project goals to display in the word cloud for the selected filters.")
        return

    text = ' '.join(all_goals_list)

    # Generate the word cloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='viridis', # A nice green-blue color map
        max_words=100,
        contour_width=3,
        contour_color='steelblue',
        collocations=False # Avoids pairing words together
    ).generate(text)

    # Save the generated image
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    
    # Display the word cloud in Streamlit using st.pyplot()
    st.pyplot(plt.gcf())