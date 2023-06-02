# Import the necessary libraries
import streamlit as st
import requests
from bs4 import BeautifulSoup
import openai
import re

# Set your OpenAI API key
openai.api_key = st.secrets['OPENAI_API_KEY']

st.session_state['model']='gpt-4-0314'

# Create a text area for input and a button
st.title('Web Text to GPT')
websites = st.text_area("Input website URL (one each line)", placeholder="https://example.com\nhttps://example.ai\n...")
input_prompt = st.text_area("Input prompt", 'What is the summary of the content from example.com?')
generate_button = st.button('Generate Response')

if generate_button:
    urls = websites.split('\n')[1:]
    print(urls)
    website_text=''
    
    for url in urls:
        # Download the webpage content
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

        page = requests.get(url, headers=headers)
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

