# Growing Justice: The Faith in Place Tree Equity Dashboard

This repository contains the source code for an interactive data dashboard built for **Faith in Place**. The dashboard visualizes the impact of the USDA Forest Service Tree Grant initiative, which aims to promote environmental justice by funding tree planting projects in underserved communities across Illinois, Indiana, and Wisconsin.

The live application is deployed on Streamlit Cloud and can be viewed here: `[https://hymzhao-mcdc2025-faithinplace-app-mgscys.streamlit.app/]`

---

## How to Run Locally

To run this application on your own machine, follow these steps.

1.  **Clone the Repository:**
    Open your terminal and run the following command to clone the project files.
    ```
    git clone https://github.com/hymzhao/MCDC2025_FaithinPlace.git
    ```
2.  **Navigate to the Directory:**
    ```
    cd MCDC2025_FaithinPlace
    ```
3.  **Install Dependencies:**
    Make sure you have Python installed. Then, install the required packages using pip.
    ```
    pip install -r requirements.txt
    ```
4.  **Run the Streamlit App:**
    Once the dependencies are installed, run the following command in the terminal to launch the dashboard.
    ```
    streamlit run app.py
    ```
    Your web browser should open with the application running.

---

## File Structure

Here is a brief overview of the key files and folders in this project:

- **`/` (Root Directory)**

  - `app.py`: The main script that runs the Streamlit application, handles page navigation, and defines the overall layout.
  - `requirements.txt`: A list of the Python packages required to run the project.
  - `packages.txt`: A list of system-level dependencies required for deployment on Streamlit Cloud.
  - `.gitignore`: Specifies files and folders that Git should ignore (e.g., `__pycache__`).

- **`/src`**

  - `data_cleaner.py`: Contains all the functions for loading, cleaning, merging, and transforming the raw project data.
  - `map_visualizations.py`: Contains all the functions that generate the Plotly charts and Matplotlib word cloud used in the dashboard.

- **`/data`**

  - This folder holds all the raw data used by the application, including CSV files with project information and GeoJSON files for the map's base layer.

- **`/images`**
  - Contains static image assets used in the dashboard, such as the organization logo.
