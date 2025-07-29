# app.py
import streamlit as st
import pandas as pd
import ast
from collections import Counter
from itertools import combinations
import nltk
import ssl

st.set_page_config(layout = 'wide')

# This is a direct approach to ensure data is downloaded on deployment.
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# List of packages to ensure are downloaded
packages = ['punkt', 'wordnet', 'omw-1.4', 'punkt_tab']
for package in packages:
    # This will download the package if it's not already present
    # and do nothing if it is. The `quiet=True` flag supresses verbose output.
    nltk.download(package, quiet=True)

# --- Imports that depend on NLTK data ---
# This now happens AFTER the download is complete.
from src.data_cleaner import load_project_data
from src.map_visualizations import (
    create_layered_map,
    create_species_diversity_chart,
    create_goals_wordcloud,
    create_impact_category_chart 
)

st.markdown("""
<style>
/* Your full CSS here */
body {
    font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    color: #26272b;
}
h1 {
    color: #1a7342; 
    text-align: center;
    font-size: 2.8em;
    margin-bottom: 0.5em;
}
h2 {
    color: #1a7342;
    font-size: 2em;
    border-bottom: 2px solid #e6e6e6;
    padding-bottom: 5px;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
}
h3 {
    color: #388e3c;
    font-size: 1.5em;
    margin-top: 1em;
    margin-bottom: 0.5em;
}
p {
    font-size: 1.1em;
    line-height: 1.6;
    margin-bottom: 1em;
}
div.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    border: 1px solid #4CAF50;
    padding: 10px 20px;
    font-size: 16px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}
div.stButton > button:hover {
    background-color: #45a049;
    border-color: #45a049;
}
div[data-testid="stSidebarNav"] button {
    background-color: #2ca02c;
    color: white;
    border-radius: 8px;
    padding: 10px 15px;
    font-size: 15px;
    margin: 5px 0;
    width: 100%;
}
div[data-testid="stSidebarNav"] button:hover {
    background-color: #248c24;
}

</style>
""", unsafe_allow_html=True)

st.image("images/logowhite.png", use_column_width=True)
st.title("MCDC Faith in Place 2025")

if "page" not in st.session_state:
    st.session_state.page = "Project Overview"

st.sidebar.header("Navigation")
if st.sidebar.button("Project Overview"):
    st.session_state.page = "Project Overview"
if st.sidebar.button("Tree Planting Map"):
    st.session_state.page = "Tree Planting Map"
if st.sidebar.button("Environmental Impact"):
    st.session_state.page = "Environmental Impact"
if st.sidebar.button("Community & Workforce Impact"):
    st.session_state.page = "Community & Workforce Impact"

# --- DATA LOADING AND FILTERING ---
df = load_project_data({
    'original_data': "data/Geocoded_MCDC-Sample-Info.csv",
    'new_data': "data/usda_species_extracted_with_ollama_and_goals.csv"
})

filtered_df = df
if df is not None:
    st.sidebar.subheader("Global Filters")
    if 'Organization Name' in df.columns:
        organization_names = sorted(df['Organization Name'].unique().tolist())
        all_orgs_option = "All Organizations (Select All)"
        organization_names.insert(0, all_orgs_option)

        if "selected_organizations_filter" not in st.session_state:
            st.session_state.selected_organizations_filter = [all_orgs_option]

        selected_organizations = st.sidebar.multiselect(
            "Filter by Organization(s):",
            organization_names,
            default=st.session_state.selected_organizations_filter,
            key="org_multiselect_filter"
        )
        st.session_state.selected_organizations_filter = selected_organizations

        if all_orgs_option in selected_organizations or not selected_organizations:
            filtered_df = df
        else:
            filtered_df = df[df['Organization Name'].isin(selected_organizations)]

# --- PAGE RENDERING ---

if st.session_state.page == "Project Overview":
    st.header("Project Overview and Motivation")

    st.write("""
    The **Faith in Place Tree Equity and Forestry Workforce Initiative** is driven by a critical need to address
    **environmental justice** in historically underserved communities across Illinois, Indiana, and Wisconsin.
    In many of these areas, environmental inequities—such as lower tree canopy cover, higher pollution levels,
    and reduced access to green spaces—contribute to a range of adverse health, social, and economic outcomes.
    """)

    st.subheader("Our Vision: Data for Impact")
    st.write("""
    This dashboard aims to provide a **transparent, accessible, and data-driven view** of the project’s ecological and
    social benefits. By establishing and tracking key metrics, we seek to:
    * **Demonstrate the immediate impact** of tree planting efforts.
    * Highlight broader contributions to **climate resilience, economic development, and community empowerment**.
    * **Transform complex data into compelling narratives** that educate and inspire stakeholders.
    * Show **tangible results** to foster community engagement and build momentum for future initiatives.
    """)

    st.subheader("Navigating the Dashboard")
    st.write("""
    Use the **sidebar on the left** to explore different aspects of the Faith in Place Tree Grant projects:
    """)
    st.markdown("""
    * **Project Overview (You Are Here):** Understand the project's mission, goals, and how to use this dashboard.
    * **Tree Planting Map:** Visualize tree planting locations and quantities across the Midwest, with key metrics.
        Use the **"Filter by Organization(s)"** dropdown in the sidebar to narrow down the data displayed.
    * **Environmental Impact:** Explore estimated ecological benefits like carbon sequestration, stormwater management, and air quality improvements.
    * **Community & Workforce Impact:** Discover insights into jobs created, volunteer participation, and community engagement efforts.
    """)

    st.subheader("About the Data")
    st.write("""
    The data presented here is derived from **pre-project applications** submitted by community organizations and Houses of Worship
    receiving grants from the USDA Forest Service Tree Grant program. This dashboard provides a **real-time snapshot**
    of the planned tree planting and associated project goals.
    """)
    st.write("We anticipate integrating additional data as the project progresses to track growth, survival rates, and more precise environmental and social impacts over the four-year grant cycle.")

    if filtered_df is not None:
        st.caption("A snapshot of the data driving these insights:")
        st.dataframe(filtered_df.head(5))

    st.subheader("Our Team")
    st.write("""
    This initiative is a collaborative effort between **Faith in Place** and the **Metropolitan Chicago Data-Science Corps (MCDC)**.
    The project is funded by the **USDA Forest Service Tree Grant**.
    """)
    st.markdown("""
    MCDC Team:
    * **Ting Liu, Ph.D., Associate Professor & GIS Coordinator**
    * Leila Tanovic
    * Prach Thaewanarumitkul
    * Olivia Bobbie Carr
    * Hannah Zhao
            
    For inquiries, please contact:
    * **Liz Ferguson (Faith in Place):** Data and Operations Senior Coordinator | [Liz@faithinplace.org](mailto:Liz@faithinplace.org) | 484-560-7982
    * **Matthew Sperry (MCDC):** Business Liaison | [matt.sperry@northwestern.edu](mailto:matt.sperry@northwestern.edu)
    """)
    st.markdown("---")

elif st.session_state.page == "Tree Planting Map":
    st.header("Tree Planting Map")
    if filtered_df is not None and not filtered_df.empty:
        col1, col2 = st.columns([0.7, 0.3])
        with col1:
            create_layered_map(filtered_df)
        with col2:
            st.subheader("Key Metrics")
            total_trees = filtered_df['# Trees To Be Planted'].sum()
            st.metric(label="Total Trees To Be Planted", value=f"{total_trees:,.0f}")
            num_organizations = filtered_df['Organization Name'].nunique()
            st.metric(label="Participating Organizations", value=num_organizations)
            num_cities = filtered_df['Project Location City'].nunique()
            st.metric(label="Unique Project Cities", value=num_cities)
            num_states = filtered_df['Project Location State'].nunique()
            st.metric(label="Unique Project States", value=num_states)

            with st.expander("What is the Tree Equity Score?"):
                st.write("""
                Tree Equity Score is a nationwide, block group-level score ranging from 0-100 that highlights inequitable access to trees.
                The lower the score, the greater the priority for tree planting. A score of 100 means the block group has met a minimum standard
                for tree cover appropriate for the area's natural biome and built environment.
                """)
                st.image("images/treequity.png", caption="Components of the Tree Equity Score.")

        st.markdown("---")
        st.header("Species Diversity")
        create_species_diversity_chart(filtered_df)

    elif filtered_df.empty:
        st.warning("No data available for the selected organization(s). Please adjust your filter.")
    else:
        st.warning("Data not loaded. Cannot display map or metrics.")

elif st.session_state.page == "Community & Workforce Impact":
    st.header("Community and Workforce Impact Analysis")
    st.write("""
    This section summarizes the primary goals of the grant projects, showing key impact areas and strategic focus.
    """)
    if filtered_df is not None and not filtered_df.empty and 'Goal Categories' in filtered_df.columns:
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            create_impact_category_chart(filtered_df)
        with col2:
            st.subheader("Deeper Insights")
            
            # Reverted back to the original st.metric style
            num_multi_goal_orgs = filtered_df['Goal Categories'].apply(lambda x: len(x) > 1).sum()
            total_orgs = len(filtered_df)
            percent_multi_goal = (num_multi_goal_orgs / total_orgs * 100) if total_orgs > 0 else 0
            
            st.metric(
                label="Multi-faceted Projects",
                value=f"{num_multi_goal_orgs} Projects",
                help=f"{percent_multi_goal:.1f}% of organizations have goals in more than one impact category."
            )

            # --- Trees Planted per Impact Area ---
            st.write("##### Trees Planted per Impact Area")
            trees_per_cat = filtered_df.explode('Goal Categories').groupby('Goal Categories')['# Trees To Be Planted'].sum().sort_values(ascending=False)
            st.dataframe(trees_per_cat)
            
        with st.expander("See Goal Keywords in a Word Cloud"):
            create_goals_wordcloud(filtered_df)
    else:
        st.warning("No goal data available for the selected filters.")