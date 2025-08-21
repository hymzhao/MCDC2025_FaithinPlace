import pandas as pd
import streamlit as st
import ast

def normalize_species_list(species_list):
    """
    Normalizes a list of species names using a comprehensive mapping dictionary.
    """
    # This map is now much more detailed to handle the variations from the data.
    species_normalization_map = {
        # --- Apple ---
        'apple': 'Apple', 'apple (malus domestica)': 'Apple', 'apples': 'Apple',
        'dwarf apple': 'Apple', 'granny smith': 'Apple', 'honeycrisp': 'Apple',
        'honeycrisp apple': 'Apple', 'red apple': 'Apple', 'malus domestica': 'Apple',
        'crabapple': 'Apple',
        # --- Ash ---
        'ash': 'Ash',
        # --- Beech ---
        'beech': 'Beech', 'american beech': 'Beech', 'fagus grandifolia': 'Beech',
        # --- Birch ---
        'birch': 'Birch', 'river birch': 'Birch', 'river birch (betula nigra)': 'Birch',
        # --- Buckeye ---
        'buckeye': 'Buckeye', 'aesculus glabra': 'Buckeye', 'ohio buckeye': 'Buckeye',
        'red buckeye': 'Buckeye',
        # --- Catalpa ---
        'catalpa': 'Catalpa', 'northern catalpa': 'Catalpa',
        # --- Cedar ---
        'cedar': 'Cedar', 'white cedar': 'Cedar', 'thuja occidentalis': 'Cedar',
        # --- Cherry ---
        'cherry': 'Cherry', 'lapins cherry': 'Cherry', 'rainier cherry': 'Cherry',
        'stella cherry': 'Cherry', 'sand cherry tree': 'Cherry',
        # --- Coffeetree ---
        'coffee': 'Kentucky Coffeetree', 'coffeetree': 'Kentucky Coffeetree',
        'kentucky coffee': 'Kentucky Coffeetree', 'kentucky coffee tree': 'Kentucky Coffeetree',
        'gymnocladus dioicus': 'Kentucky Coffeetree', 'gymnocladus dioicus-kentucky coffee tree': 'Kentucky Coffeetree',
        # --- Cypress ---
        'cypress': 'Cypress', 'bald cypress': 'Cypress',
        # --- Dogwood ---
        'dogwood': 'Dogwood', 'japanese dogwood': 'Dogwood', 'pagoda dogwood': 'Dogwood',
        'pagoda_dogwood': 'Dogwood',
        # --- Elm ---
        'elm': 'Elm', 'american elm': 'Elm', 'ulmus americana': 'Elm',
        'ulmus americana "princeton"': 'Elm', 'ulmus x "morton glossy"': 'Elm',
        # --- Ginkgo ---
        'ginkgo': 'Ginkgo',
        # --- Gum ---
        'gum': 'Gum', 'sweet gum': 'Gum',
        # --- Hackberry ---
        'hackberry': 'Hackberry', 'hack berry': 'Hackberry', 'celtis occidentalis': 'Hackberry',
        'celtis occidentalis-hackberry': 'Hackberry', 'common hackberry': 'Hackberry',
        'sugarberry': 'Hackberry',
        'Fringetree': 'Fringe Tree', 'Fringe Tree': 'Fringe Tree',
        # --- Hazelnut ---
        'hazelnut': 'Hazelnut', 'hedges of hazelnuts': 'Hazelnut', 'american hazelnut (corylus americana)': 'Hazelnut',
        'corylus americana': 'Hazelnut',
        # --- Hickory ---
        'butternut hickory': 'Hickory', 'shagbark hickory': 'Hickory', 'carya ovata': 'Hickory',
        'butternut': 'Hickory',
        # --- Honeylocust ---
        'honeylocust': 'Honeylocust', 'thornless honeylocust': 'Honeylocust',
        'gleditsia triacanthos': 'Honeylocust', 'gleditsia triacanthos inermis "shademaster"': 'Honeylocust',
        'locust': 'Honeylocust',
        # --- Hornbeam ---
        'hornbeam': 'Hornbeam', 'american hornbeam': 'Hornbeam', 'carpinus caroliniana': 'Hornbeam',
        'hophornbeam': 'Hornbeam', 'ostrya virginiana': 'Hornbeam',
        # --- Linden ---
        'linden': 'Linden', 'american linden': 'Linden', 'littleleaf linden': 'Linden', 'basswood': 'Linden',
        # --- Maple ---
        'maple': 'Maple', 'red maple': 'Maple', 'acer rubrum': 'Maple', 'sugar maple': 'Maple',
        'autumn blaze maple': 'Maple', 'red sunset maple': 'Maple', 'acer x freemanii `jeffsred`': 'Maple',
        'memorial tree (red maple)': 'Maple',
        # --- Oak ---
        'oak': 'Oak', 'bur oak': 'Oak', 'burr oak': 'Oak', 'northern red oak': 'Oak', 'quercus rubra': 'Oak',
        'red oak': 'Oak', 'white oak': 'Oak', 'chinkapin oak': 'Oak', 'chinquapin oak': 'Oak',
        'northern red oak (quercus rubra)': 'Oak', 'northern_red_oak': 'Oak', 'oak species': 'Oak',
        'quercus alba': 'Oak', 'quercus bicolor': 'Oak', 'swamp white oak': 'Oak', 'shingle oak': 'Oak',
        'shumard oak': 'Oak', 'quercus shumardii': 'Oak', 'quercus imbricaria': 'Oak',
        'quercus x schuetti': 'Oak', 'swamp white oak (quercus alba)': 'Oak', 'chinquapin': 'Oak',
        # --- Pawpaw ---
        'paw paw': 'Pawpaw', 'paw paw (asimina triloba)': 'Pawpaw', 'pawpaw': 'Pawpaw',
        'pennsylvania golden pawpaw': 'Pawpaw', 'sunflower pawpaw': 'Pawpaw', 'asimina triloba': 'Pawpaw',
        'sunflower': 'Pawpaw',
        # --- Peach ---
        'peach': 'Peach', 'elberta peach': 'Peach', 'harvester peach': 'Peach',
        'majestic peach': 'Peach', 'peach tree': 'Peach', 'peaches': 'Peach',
        # --- Pear ---
        'pear': 'Pear', 'pear (pyrus communis)': 'Pear', 'pear_tree': 'Pear', 'pears': 'Pear',
        'ornamental pear': 'Pear', 'pyrus communis': 'Pear',
        # --- Pecan ---
        'pecan': 'Pecan', 'northern pecan': 'Pecan', 'carya illinoinensis': 'Pecan', 'pecan tree': 'Pecan',
        # --- Pine ---
        'pine': 'Pine', 'eastern white pine': 'Pine', 'white pine': 'Pine',
        # --- Plum ---
        'plum': 'Plum', 'plums': 'Plum', 'american plum': 'Plum',
        # --- Redbud ---
        'redbud': 'Redbud', 'eastern redbud': 'Redbud', 'eastern red bud': 'Redbud',
        'cercis canadensis': 'Redbud', 'eastern redbud (cercis canadensis)': 'Redbud',
        'redbud eastern': 'Redbud',
        # --- Serviceberry ---
        'serviceberry': 'Serviceberry', 'allegheny serviceberry': 'Serviceberry',
        'amelanchier laevis': 'Serviceberry', 'service berry': 'Serviceberry',
        'service berry (amenlanchier)': 'Serviceberry', 'serviceberry (amelanchier arborea)': 'Serviceberry',
        # --- Spruce ---
        'spruce': 'Spruce', 'dwarf alberta spruce': 'Spruce',
        # --- Sycamore ---
        'sycamore': 'Sycamore', 'american sycamore': 'Sycamore', 'platanus occidentalis': 'Sycamore',
        'platanus occidentalis-sycamore': 'Sycamore',
        # --- Tulip Tree ---
        'tulip': 'Tulip Tree', 'tulip poplar': 'Tulip Tree', 'tulip tree': 'Tulip Tree',
        'tuliptree': 'Tulip Tree', 'liriodendron tulipifera': 'Tulip Tree',
        'liriodendron tulipifera-tulip poplar': 'Tulip Tree',
        # --- Walnut ---
        'walnut': 'Walnut',
        # --- Unspecified/Generic ---
        'count': 'Unspecified/Generic', 'species': 'Unspecified/Generic', 'tree': 'Unspecified/Generic',
        'others': 'Unspecified/Generic', 'unspecified': 'Unspecified/Generic',
        'threefold': 'Unspecified/Generic', 'street trees (not specified)': 'Unspecified/Generic',
        'shade trees': 'Unspecified/Generic', 'native trees': 'Unspecified/Generic',
        'indiana native (undetermined)': 'Unspecified/Generic', 'fruit bearing trees': 'Unspecified/Generic',
        'large fruit and nut trees': 'Unspecified/Generic', 'small fruit trees': 'Unspecified/Generic',
        'espaliered fruit trees': 'Unspecified/Generic',
    }

    cleaned_list = set()
    for species in species_list:
        standardized_name = species_normalization_map.get(species.lower(), species.title())
        cleaned_list.add(standardized_name)

    return sorted(list(cleaned_list))


def categorize_project_goals(goals_list):
    """
    Analyzes a list of goals and assigns them to predefined impact categories.
    """
    categories = set()
    goal_text = ' '.join(goals_list).lower()

    # Define keywords for each category
    category_keywords = {
        "Environmental & Climate": ['environment', 'sustainability', 'climate', 'canopy', 'green', 'beautification', 'ecosystem', 'air quality', 'stormwater', 'biodiversity'],
        "Youth & Education": ['education', 'youth', 'students', 'learning', 'school', 'educational', 'stem'],
        "Community Building": ['community', 'engagement', 'neighborhood', 'beautify', 'volunteer', 'public', 'space', 'gathering', 'social'],
        "Workforce & Economic": ['workforce', 'job', 'skills', 'economic', 'employment', 'career', 'development'],
        "Food & Agriculture": ['food', 'agriculture', 'orchard', 'fruit', 'harvest', 'garden']
    }

    for category, keywords in category_keywords.items():
        if any(keyword in goal_text for keyword in keywords):
            categories.add(category)

    if not categories:
        return ["General Improvement"]
    return sorted(list(categories))

@st.cache_data
def load_project_data(file_paths):
    """
    Loads, cleans, and categorizes project data.
    """
    try:
        df_original = pd.read_csv(file_paths['original_data'])
        df_new_nlp = pd.read_csv(file_paths['new_data'])

        # --- Merging and Basic Cleaning (unchanged) ---
        merge_on_candidate_cols = ['Organization Name', 'Project Description']
        actual_merge_on_cols = [col for col in merge_on_candidate_cols if col in df_original.columns and col in df_new_nlp.columns]
        if not actual_merge_on_cols:
            st.error("Error: No common identifying columns found.")
            return None
        cols_from_new_nlp = actual_merge_on_cols + ['USDA Matched Species', 'Species from Ollama', 'Goals from Ollama']
        cols_from_new_nlp_existing = [col for col in cols_from_new_nlp if col in df_new_nlp.columns]
        df_merged = pd.merge(
            df_original, df_new_nlp[cols_from_new_nlp_existing].drop_duplicates(),
            on=actual_merge_on_cols, how='left', suffixes=('_original', '_nlp')
        )
        df_cleaned = df_merged.copy()
        if 'Project Location State' in df_cleaned.columns:
            state_mapping = {'ILLINOIS': 'IL', 'INDIANA': 'IN', 'WISCONSIN': 'WI'}
            df_cleaned['Project Location State'] = df_cleaned['Project Location State'].astype(str).str.strip().str.upper().replace(state_mapping)
            valid_states = ['IL', 'IN', 'WI']
            df_cleaned['Project Location State'] = df_cleaned['Project Location State'].apply(lambda x: x if x in valid_states else 'Other/Invalid')
        for col in ['Latitude', 'Longitude', '# Trees To Be Planted']:
            if col in df_cleaned.columns:
                df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
        df_cleaned.dropna(subset=['Latitude', 'Longitude', '# Trees To Be Planted'], inplace=True)
        df_cleaned['# Trees To Be Planted'] = df_cleaned['# Trees To Be Planted'].astype(int)
        for col, start_char, empty_val in [
            ('Species from Ollama', '{', {}),
            ('USDA Matched Species', '[', []),
            ('Goals from Ollama', '[', [])
        ]:
            if col in df_cleaned.columns:
                df_cleaned[col] = df_cleaned[col].apply(
                    lambda x: ast.literal_eval(x) if pd.notna(x) and isinstance(x, str) and x.strip().startswith(start_char) else empty_val
                )

        # --- Species Cleaning (unchanged) ---
        def combine_species(row):
            ollama_species = list(row.get('Species from Ollama', {}).keys())
            usda_species = row.get('USDA Matched Species', [])
            return list(set(ollama_species + usda_species))
        df_cleaned['All Species'] = df_cleaned.apply(combine_species, axis=1)
        df_cleaned['Cleaned Species'] = df_cleaned['All Species'].apply(normalize_species_list)

        # --- ADD GOAL CATEGORIZATION ---
        if 'Goals from Ollama' in df_cleaned.columns:
            df_cleaned['Goal Categories'] = df_cleaned['Goals from Ollama'].apply(categorize_project_goals)

        return df_cleaned
    except FileNotFoundError as e:
        st.error(f"Error: A data file was not found. Please check '{e.filename}'.")
        return None
    except Exception as e:
        st.error(f"An error occurred while processing data: {e}.")
        return None