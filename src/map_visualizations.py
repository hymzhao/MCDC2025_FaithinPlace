
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import geopandas as gpd
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

def create_layered_map(df):
    """
    Creates a map with a Tree Equity Score background layer and project locations on top.
    """
    if df is None:
        st.warning("No project data provided to create the map.")
        return

    try:
        # Make sure these filenames match what's in your 'data' folder
        state_files = [
            "data/il_tes.geojson",
            "data/in_tes.geojson",
            "data/wi_tes.geojson"
        ]
        list_of_gdfs = [gpd.read_file(file) for file in state_files]
        tes_data = pd.concat(list_of_gdfs, ignore_index=True)
    except Exception as e:
        st.error(f"Error loading GeoJSON files: {e}. Make sure the files are in the 'data' folder and filenames are correct.")
        return

    fig = go.Figure()

    # Add the Tree Equity Score background layer
    fig.add_trace(go.Choroplethmapbox(
        geojson=tes_data.__geo_interface__,
        locations=tes_data.index,
        z=tes_data['tes'],
        colorscale="RdYlGn",
        zmin=0,
        zmax=100,
        marker_opacity=0.6,
        marker_line_width=0,
        colorbar_title="Tree Equity Score"
    ))

    # Prepare data for the scatter plot
    map_df = df.dropna(subset=['Latitude', 'Longitude', '# Trees To Be Planted']).copy()
    map_df['Species List (for hover)'] = map_df['Cleaned Species'].apply(lambda x: ', '.join(x) if x else 'N/A')

    # Add your project locations on top
    fig.add_trace(go.Scattermapbox(
        lat=map_df["Latitude"],
        lon=map_df["Longitude"],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=map_df["# Trees To Be Planted"],
            color='#00008B',
            sizemin=4,
            # CORRECTED: Replaced 'sizemax' with 'sizeref' for proper scaling
            sizeref=max(map_df["# Trees To Be Planted"]) / 50, # Adjust divisor for best look
            opacity=0.8
        ),
        hoverinfo='text',
        text=[f"<b>{org}</b><br>Trees: {trees}<br>Species: {species}"
              for org, trees, species in zip(map_df['Organization Name'], map_df['# Trees To Be Planted'], map_df['Species List (for hover)'])],
    ))

    # Update the layout
    fig.update_layout(
        title="Project Locations Over Tree Equity Score",
        mapbox_style="carto-positron",
        mapbox_zoom=5,
        mapbox_center={"lat": 41.8, "lon": -88.0},
        margin={"r":0, "t":40, "l":0, "b":0},
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def create_species_diversity_chart(df):
    """
    Creates a filtered and styled bar chart of species diversity.
    """
    if df is None or 'Cleaned Species' not in df.columns:
        st.warning("Cleaned species data not available to create the diversity chart.")
        return

    all_species_list = [species for sublist in df['Cleaned Species'] for species in sublist]
    if not all_species_list:
        st.info("No species data to display in the chart for the selected filters.")
        return

    species_counts = Counter(all_species_list)
    species_df = pd.DataFrame(species_counts.items(), columns=['Species', 'Count'])

    # --- CHANGE 1: Filter the DataFrame ---
    # Keep only the species that appear in more than one project
    species_df = species_df[species_df['Count'] > 1].sort_values(by='Count', ascending=False)

    if species_df.empty:
        st.info("No species are planted in more than one project for the selected filters.")
        return

    fig = px.bar(
        species_df,
        x='Count',
        y='Species',
        orientation='h',
        title='Most Common Species Across Projects',
        labels={'Count': 'Number of Projects Planting This Species', 'Species': 'Tree Species'},
        # --- CHANGE 2: Update the color ---
        color_discrete_sequence=['#388e3c'] # A green from your website's theme
    )

    fig.update_layout(
        yaxis={'categoryorder':'total ascending'},
        height=max(400, len(species_df) * 25)
    )
    st.plotly_chart(fig, use_container_width=True)

def create_impact_category_chart(df):
    """
    Creates a bar chart showing the number of organizations in each goal category.
    """
    if df is None or 'Goal Categories' not in df.columns:
        st.warning("Goal category data not available.")
        return

    # Explode the lists of categories into separate rows and count them
    category_counts = df.explode('Goal Categories')['Goal Categories'].value_counts().reset_index()
    category_counts.columns = ['Category', 'Organization Count']

    fig = px.bar(
        category_counts,
        x='Organization Count',
        y='Category',
        orientation='h',
        title='Primary Project Impact Areas',
        labels={'Organization Count': 'Number of Organizations', 'Category': 'Impact Area'},
        color_discrete_sequence=['#1a7342'] # A darker green from your theme
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)


# --- UPDATED WORD CLOUD FUNCTION ---
def create_goals_wordcloud(df):
    """
    Generates a lemmatized and heavily cleaned word cloud from project goals.
    """
    if df is None or 'Goals from Ollama' not in df.columns:
        st.warning("Project goals data not available.")
        return

    all_goals_list = [goal for sublist in df['Goals from Ollama'] for goal in sublist]
    if not all_goals_list:
        st.info("No project goals to display in the word cloud.")
        return

    text = ' '.join(all_goals_list)

    lemmatizer = WordNetLemmatizer()
    tokens = word_tokenize(text)
    lemmatized_text = ' '.join([lemmatizer.lemmatize(word.lower()) for word in tokens])

    # --- EVEN MORE AGGRESSIVE STOPWORDS LIST ---
    stopwords = set([
        'of', 'the', 'for', 'a', 'in', 'with', 'project', 'tree', 'to', 'planting', 'through', 'provide', 'create', 'help', 'well',
        'also', 'area', 'will', 'plan', 'our', 'place', 'campus', 'effort',
        'surrounding', 'natural', 'goal', 'ha', 'student', 'program', 'new',
        'year', 'work', 'member', 'organization', 'group', 'city',
        'state', 'local', 'partner', 'people', 'site', 'ground', 'chicago',
        'illinois', 'indiana', 'wisconsin', 'hand', 'etc', 'use', 'need', 'enhance',
        'additional', 'make', 'ensure', 'within', 'around', 'including', 'and', 'to'
    ])

    wordcloud = WordCloud(
        width=800, height=400, background_color='white',
        colormap='Greens', max_words=100, stopwords=stopwords,
        collocations=False
    ).generate(lemmatized_text)

    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(plt.gcf())