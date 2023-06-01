# Import the necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import re

def extract_urls(input_text):
    # Regex pattern to match URLs
    url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    
    # Find all URLs in the input text
    urls = re.findall(url_pattern, input_text)

    # Match any websites mentioned without http or https
    bare_url_pattern = re.compile(r'\bwww\.[a-zA-Z0-9-]+(\.[a-zA-Z0-9]+)+')

    # Find all bare URLs
    bare_urls = re.findall(bare_url_pattern, input_text)

    # Add 'https://' to the start of each bare URL
    full_bare_urls = ['https://' + url for url in bare_urls]

    # Combine both lists
    all_urls = urls + full_bare_urls

    return all_urls

# Set your OpenAI API key
openai.api_key = st.secrets['OPENAI_API_KEY']

st.session_state['model']='gpt-4-0314'

# Create a text area for input and a button
st.title('Web Text to GPT')
input_prompt = st.text_area("Input website URL and prompt", 'https://example.com\nWhat is the summary of the content?')
generate_button = st.button('Generate Response')

if generate_button:
    urls = extract_urls(input_prompt)
    
    website_text=''
    
    for url in urls:
        # Download the webpage content
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')

        # Get all text from the webpage
        website_text = website_text+ soup.get_text()

    # Concatenate website text with the rest of the prompt
    full_prompt = website_text + '\n' + input_prompt

    # Use the OpenAI API to generate a response
    response = openai.ChatCompletion.create(
            temperature = 0.7,
            model=st.session_state['model'],
            messages=[
                {
                    "role": "user",
                    "content": f"{full_prompt}"
                }
            ]
        )

    # Extract the assistant's reply
    assistant_reply = response['choices'][0]['message']['content']

    # Display the reply
    st.text_area("Output", assistant_reply, height = 400)

