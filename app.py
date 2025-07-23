# app.py
import streamlit as st
import pandas as pd
import ast
from collections import Counter
from itertools import combinations
import nltk
import ssl

# --- THIS MUST BE THE FIRST STREAMLIT COMMAND ---
st.set_page_config(layout = 'wide')

# --- NLTK DOWNLOADER ---
@st.cache_resource
def download_nltk_data():
    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context
    
    nltk.download('punkt')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

download_nltk_data()

# --- IMPORT YOUR FUNCTIONS ---
from src.data_cleaner import load_project_data
from src.map_visualizations import (
    create_layered_map,
    create_species_diversity_chart,
    create_goals_wordcloud,
    create_impact_category_chart 
)

# --- CUSTOM CSS, HEADER, AND NAVIGATION (Unchanged) ---
st.markdown("""
<style>
/* Your CSS here */
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
    color: #1a7342; /* Darker green */
    font-size: 2em;
    border-bottom: 2px solid #e6e6e6; /* Subtle line below headers */
    padding-bottom: 5px;
    margin-top: 1.5em;
    margin-bottom: 0.8em;
}
/* ... rest of your CSS ... */
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

# --- DATA LOADING AND FILTERING (Unchanged) ---
df = load_project_data({
    'original_data': "data/Geocoded_MCDC-Sample-Info.csv",
    'new_data': "data/usda_species_extracted_with_ollama_and_goals.csv"
})

filtered_df = df
if df is not None:
    # Your filtering logic here...
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
    # ... (Your overview content)
    st.write("""
    The **Faith in Place Tree Equity and Forestry Workforce Initiative** is driven by a critical need to address
    **environmental justice** in historically underserved communities across Illinois, Indiana, and Wisconsin.
    """)

# --- RESTORED TREE PLANTING MAP PAGE ---
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
                st.image("images/Screenshot 2025-07-23 at 12.49.08 PM.png", caption="Components of the Tree Equity Score.")

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
    This section summarizes the primary goals of the grant projects. The chart shows the number of organizations
    tackling key impact areas, while the metrics provide deeper insights into the strategic focus of the portfolio.
    """)
    if filtered_df is not None and not filtered_df.empty and 'Goal Categories' in filtered_df.columns:
        col1, col2 = st.columns([0.6, 0.4])
        with col1:
            create_impact_category_chart(filtered_df)
        with col2:
            st.subheader("Deeper Insights")
            num_multi_goal_orgs = filtered_df['Goal Categories'].apply(lambda x: len(x) > 1).sum()
            total_orgs = len(filtered_df)
            percent_multi_goal = (num_multi_goal_orgs / total_orgs * 100) if total_orgs > 0 else 0
            st.metric(
                label="Multi-faceted Projects",
                value=f"{num_multi_goal_orgs}",
                help=f"{percent_multi_goal:.1f}% of organizations have goals in more than one impact category."
            )
            pairs = filtered_df['Goal Categories'].apply(lambda x: list(combinations(sorted(x), 2)))
            pair_counts = Counter(p for sublist in pairs for p in sublist)
            if pair_counts:
                most_common_pair, count = pair_counts.most_common(1)[0]
                st.markdown("##### Most Common Synergy")
                st.markdown(f"**{' & '.join(most_common_pair)}**")
                st.caption(f"This pair of goals appeared together in {count} projects.")
            st.write("##### Trees Planted per Impact Area")
            trees_per_cat = filtered_df.explode('Goal Categories').groupby('Goal Categories')['# Trees To Be Planted'].sum().sort_values(ascending=False)
            st.dataframe(trees_per_cat)
        with st.expander("See Goal Keywords in a Word Cloud"):
            create_goals_wordcloud(filtered_df)
    elif filtered_df.empty:
        st.warning("No data available for the selected organization(s).")
    else:
        st.warning("Data not loaded or no goal data available to display impact analysis.")