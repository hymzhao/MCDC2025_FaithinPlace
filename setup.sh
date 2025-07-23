#!/bin/bash

mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

# This is the important part for NLTK
python -m nltk.downloader punkt
python -m nltk.downloader wordnet