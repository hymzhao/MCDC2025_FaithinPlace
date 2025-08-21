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
    create_impact_category_chart,
    create_tree_type_chart
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
st.title("Growing Justice: The Faith in Place Tree Equity Dashboard")

if "page" not in st.session_state:
    st.session_state.page = "Project Overview"

st.sidebar.header("Navigation")
if st.sidebar.button("Project Overview"):
    st.session_state.page = "Project Overview"
if st.sidebar.button("Tree Planting Map"):
    st.session_state.page = "Tree Planting Map"
if st.sidebar.button("Community & Workforce Impact"):
    st.session_state.page = "Community & Workforce Impact"

# --- DATA LOADING AND FILTERING ---
df = load_project_data({
    'original_data': "data/Geocoded_MCDC-Sample-Info.csv",
    'new_data': "data/usda_species_extracted_with_ollama_and_goals.csv"
})

# Initialize filtered_df in case the data fails to load
filtered_df = None

if df is not None:
    # Start with a copy that we will progressively filter
    filtered_df = df.copy()
    
    st.sidebar.subheader("Global Filters")

    # --- NEW: STATE FILTER ---
    if 'Project Location State' in df.columns:
        states = sorted(df['Project Location State'].unique().tolist())
        selected_states = st.sidebar.multiselect(
            "Filter by State(s):",
            states,
            default=states, # Default to all states selected
            key="state_multiselect_filter"
        )
        # Apply the state filter first
        if selected_states:
            filtered_df = filtered_df[filtered_df['Project Location State'].isin(selected_states)]

    # --- EXISTING: ORGANIZATION NAME FILTER ---
    # This filter now works on the dataframe that may have already been filtered by state
    if 'Organization Name' in filtered_df.columns:
        # Get organization names from the *already filtered* df
        organization_names = sorted(filtered_df['Organization Name'].unique().tolist())
        all_orgs_option = "All Organizations"
        organization_names.insert(0, all_orgs_option)

        selected_organizations = st.sidebar.multiselect(
            "Filter by Organization(s):",
            organization_names,
            default=all_orgs_option,
            key="org_multiselect_filter"
        )

        # Only apply this filter if a specific organization is chosen
        if all_orgs_option not in selected_organizations and selected_organizations:
            filtered_df = filtered_df[filtered_df['Organization Name'].isin(selected_organizations)]

# --- PAGE RENDERING ---

if st.session_state.page == "Project Overview":
    st.markdown("""
    ## Our Mission: Growing a Just and Sustainable Future

    The **Faith in Place Tree Equity and Forestry Workforce Initiative** is a direct response to environmental injustice in historically underserved communities across Illinois, Indiana, and Wisconsin. For too long, these communities have faced inequities like lower tree canopy cover, higher pollution, and reduced access to green spaces, leading to adverse health, social, and economic outcomes.

    In partnership with the USDA Forest Service, Faith in Place is empowering local leaders by distributing 65 to 85 grants to community organizations and Houses of Worship. This initiative is about more than just planting trees; it's a four-year commitment to fostering workforce development, stimulating local economies, and empowering communities to become active stewards of their environment.

    ## The Power of Data: Making Our Impact Visible

    This dashboard was created to provide a transparent, data-driven view of the project’s profound ecological and social benefits. Our goal is to transform complex data into a compelling narrative that educates, inspires, and demonstrates tangible results.

    By tracking key metrics from the very beginning of the grant cycle, we aim to:
    * **Visualize** the geographic scope and diversity of tree planting efforts.
    * **Measure** the initiative's contribution to climate resilience, community well-being, and economic growth.
    * **Ensure** that the benefits of this work are visible, measurable, and accessible to all stakeholders, from community members to funders.

    This tool serves as a living foundation for understanding and amplifying the impact of the USDA Forest Service Tree Grant, telling the story of environmental justice and community resilience in a way that resonates with everyone.
    """)
    st.markdown("---")
    if filtered_df is not None:
        st.caption("A snapshot of the data driving these insights:")
        st.dataframe(filtered_df.head(5))

    st.subheader("Navigating the Dashboard")
    st.write("""
    Use the **sidebar on the left** to explore different aspects of the Faith in Place Tree Grant projects:
    """)
    st.markdown("""
    * **Project Overview (You Are Here):** Understand the project's mission, goals, and how to use this dashboard.
    * **Tree Planting Map:** Visualize tree planting locations and quantities across the Midwest, with key metrics.
        Use the **"Filter by Organization(s)"** dropdown in the sidebar to narrow down the data displayed.
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
        st.header("Species Diversity Analysis")
        # Add a subheader for the new chart
        st.subheader("Projects by Tree Category")
        create_tree_type_chart(filtered_df) # Call the new function

        with st.expander("See Detailed Species Breakdown"):
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
            st.caption("Note: A single project's trees may be counted in multiple categories.")
            
            trees_per_cat = filtered_df.explode('Goal Categories').groupby('Goal Categories')['# Trees To Be Planted'].sum().sort_values(ascending=False)
            st.dataframe(trees_per_cat)
            
        with st.expander("See Goal Keywords in a Word Cloud"):
            create_goals_wordcloud(filtered_df)
    else:
        st.warning("No goal data available for the selected filters.")