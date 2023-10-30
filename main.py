# TEST FOR ARTICLE READER APP THAT CAN BYPASS PAYWALLS
# conda env is ChatGPT
# launch app locally with: streamlit run C:\Users\marco\PycharmProjects\Reportailor\test_read_all.py

import streamlit as st
from PIL import Image
from trafilatura import fetch_url, bare_extraction
import spacy

# Load the multilingual model
spacy.cli.download("xx_sent_ud_sm")
nlp = spacy.load("xx_sent_ud_sm")


# Insert spacing to create paragraphs
def insert_elements_after_nth(input_list, n, elements_to_insert):
    index = n  # Start inserting elements after the nth index
    while index < len(input_list):
        for element in elements_to_insert:
            input_list.insert(index, element)
            index += 1 + n  # Move the index after the recently inserted element
    return input_list


# Extract text article
def article_reader(article_url):
    """Pass article links to Trafilatura library to extract full-text"""
    # Download HTML article web page
    downloaded = fetch_url(article_url)

    # Extract information from HTML
    result = bare_extraction(downloaded, favor_precision=True)

    # Get title
    title = result['text'].split('\n', 1)[0]

    # Get body article
    full_text = result['text'].split('\n', 1)[1:]
    full_text = " ".join(full_text)

    # Process text (split in sentences & paragraphs)
    doc = nlp(full_text)
    sentences = [sent.text.strip() for sent in doc.sents]

    # Create a list to store the paragraphs
    paragraphs = []

    # Iterate over the sentences and group them into paragraphs
    current_paragraph = []
    for sentence in sentences:
        current_paragraph.append(sentence)
        if len(current_paragraph) == 4:
            paragraphs.append(' '.join(current_paragraph))
            current_paragraph = []

    # If there are remaining sentences, create a paragraph with them
    if current_paragraph:
        paragraphs.append(' '.join(current_paragraph))

    # Join the paragraphs with line breaks
    output = '\n\n '.join(paragraphs)

    # add_spacing = insert_elements_after_nth(sentences, 3, "\n  \n")
    # body = "  ".join(add_spacing)

    return title, output


# START APP

# Dark background
dark = '''
<style>
    .stApp {
    background-color: black;
    }
</style>
'''

st.markdown(dark, unsafe_allow_html=True)

# Initialize app
image_title = Image.open('Paywall_killer_banner.png')

col1, col2, col3 = st.columns([0.5, 6, 0.5])
with col1:
    st.write("")

with col2:
    # st.markdown("<h1 style='text-align: center; color: black;'>Paywall Killer</h1>", unsafe_allow_html=True)
    st.image(image_title, width=300)

with col3:
    st.write("")

# Get link article
link_input = st.text_input('', placeholder="Paste article link")

# Process article
if st.button('Read', key='submit_article') or link_input:
    title, body = article_reader(link_input)
    st.title(title)
    st.markdown(''':white[''' + body + ''']''')
    # " ".join(body)
