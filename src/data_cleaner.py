import pandas as pd
import streamlit as st
import ast

@st.cache_data
def load_project_data(file_paths):
    """
    Goal is to load the project data from a csv file and perform initial cleaning.
    """
    try:
        # Load the original data (with geocoding)
        df_original = pd.read_csv(file_paths['original_data'])

        # Load the new data (with NLP-extracted columns)
        df_new_nlp = pd.read_csv(file_paths['new_data'])


        # --- Perform the merge ---
        # Using a more robust, minimal set of common columns for merging.
        # Ensure these columns actually exist in both DataFrames.
        # 'Project Description' is a strong identifier to ensure unique project matching.
        merge_on_candidate_cols = [
            'Organization Name',
            'Project Description'
        ]

        # Filter for only columns that actually exist in BOTH DFs from the chosen list
        actual_merge_on_cols = [
            col for col in merge_on_candidate_cols
            if col in df_original.columns and col in df_new_nlp.columns
        ]

        if not actual_merge_on_cols:
            st.error("Error: No common identifying columns found between the datasets for merging. Cannot proceed with merge.")
            return None

        # Ensure that only the NLP-related columns plus the merge keys are taken from df_new_nlp
        # to avoid duplicating other columns that are already in df_original.
        cols_from_new_nlp = actual_merge_on_cols + ['USDA Matched Species', 'Species from Ollama', 'Goals from Ollama']
        # Filter this list to only include columns that actually exist in df_new_nlp
        cols_from_new_nlp_existing = [col for col in cols_from_new_nlp if col in df_new_nlp.columns]


        # Merge the two DataFrames
        df_merged = pd.merge(
            df_original,
            df_new_nlp[cols_from_new_nlp_existing].drop_duplicates(),
            on=actual_merge_on_cols,
            how='left',
            suffixes=('_original', '_nlp') # Distinguishes any overlapping column names if they occur
        )

        # --- Continue with cleaning and type conversions on the merged DataFrame ---
        df_cleaned = df_merged.copy()

        if 'Project Location State' in df_cleaned.columns:
            # Create a mapping dictionary for standardization
            state_mapping = {
                'ILLINOIS': 'IL',
                'INDIANA': 'IN',
                'WISCONSIN': 'WI',
                # You can keep other variations here if needed
            }
            # Apply cleaning: strip whitespace, convert to upper, then replace
            # This ensures ' IL ' -> 'IL' and 'Illinois' -> 'IL'
            df_cleaned['Project Location State'] = df_cleaned['Project Location State'].astype(str).str.strip().str.upper().replace(state_mapping)

            # Define the valid states
            valid_states = ['IL', 'IN', 'WI']

            # Now, categorize any state not in the valid list
            df_cleaned['Project Location State'] = df_cleaned['Project Location State'].apply(
                 lambda x: x if x in valid_states else 'Other/Invalid'
            )
        
        # Ensure Latitude, Longitude, and '# Trees To Be Planted' are numeric
        if 'Latitude' in df_cleaned.columns:
            df_cleaned['Latitude'] = pd.to_numeric(df_cleaned['Latitude'], errors='coerce')
        if 'Longitude' in df_cleaned.columns:
            df_cleaned['Longitude'] = pd.to_numeric(df_cleaned['Longitude'], errors='coerce')

        # Drop rows where essential coordinates or tree count are missing AFTER numerical conversions
        # This handles cases where conversion to numeric resulted in NaNs
        df_cleaned.dropna(subset=['Latitude', 'Longitude', '# Trees To Be Planted'], inplace=True)


        if '# Trees To Be Planted' in df_cleaned.columns:
            df_cleaned['# Trees To Be Planted'] = pd.to_numeric(df_cleaned['# Trees To Be Planted'], errors='coerce').fillna(0).astype(int)


        # --- Parse the new stringified columns on the merged DataFrame ---
        # 'Species from Ollama' is a stringified dictionary
        if 'Species from Ollama' in df_cleaned.columns:
            df_cleaned['Species from Ollama'] = df_cleaned['Species from Ollama'].apply(
                lambda x: ast.literal_eval(x) if pd.notna(x) and isinstance(x, str) and x.strip().startswith('{') else {}
            )

        # 'USDA Matched Species' and 'Goals from Ollama' are stringified lists
        if 'USDA Matched Species' in df_cleaned.columns:
            df_cleaned['USDA Matched Species'] = df_cleaned['USDA Matched Species'].apply(
                lambda x: ast.literal_eval(x) if pd.notna(x) and isinstance(x, str) and x.strip().startswith('[') else []
            )
        if 'Goals from Ollama' in df_cleaned.columns:
            df_cleaned['Goals from Ollama'] = df_cleaned['Goals from Ollama'].apply(
                lambda x: ast.literal_eval(x) if pd.notna(x) and isinstance(x, str) and x.strip().startswith('[') else []
            )
        # --- End of NEW parsing ---

        return df_cleaned
    except FileNotFoundError as e:
        st.error(f"Error: One of the data files was not found. Please ensure '{e.filename}' is in the correct path.")
        return None
    except Exception as e:
        st.error(f"An error occurred while loading, merging, or processing data: {e}. Please check the sidebar for debugging information if available.")
        return None
