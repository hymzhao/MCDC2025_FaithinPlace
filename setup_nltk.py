import nltk
import ssl

# This is a workaround for a common certificate verification issue
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download the necessary NLTK data packages
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4') # Open Multilingual Wordnet, for better compatibility