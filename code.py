import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Streamlit UI
st.title("Sentiment Analysis with OpenAI")

st.write("""
This app performs sentiment analysis on text input and classifies it as 'positive', 'negative', or 'neutral'.
""")

# Text input box for the user to enter text
input_text = st.text_area("Enter text for sentiment analysis:", "")

if st.button("Analyze Sentiment"):
    if input_text:
        # Modify the prompt to ensure the model responds with just 'positive', 'negative', or 'neutral'
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",  # Ensure this model supports sentiment analysis
            messages=[
                {
                    "role": "user",
                    "content": f"Please analyze the sentiment of the following text and respond with only one word: 'positive', 'negative', or 'neutral'. Text: '{input_text}'"
                }
            ],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )
        
        sentiment = ""  # Variable to accumulate the sentiment result
        for chunk in completion:
            # Ensure that content exists in the chunk and accumulate
            if chunk.choices[0].delta.content:
                sentiment += chunk.choices[0].delta.content.strip()
        
        # Check the accumulated sentiment and display
        if sentiment.strip():
            st.write(f"Sentiment: **{sentiment.strip()}**")
        else:
            st.write("Could not determine sentiment. Please try again.")
    else:
        st.write("Please enter some text to analyze.")
