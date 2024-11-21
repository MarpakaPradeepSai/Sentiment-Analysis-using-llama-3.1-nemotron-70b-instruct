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
        
        sentiment = ""
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                sentiment = chunk.choices[0].delta.content.strip()

        # Show the result to the user
        st.write(f"Sentiment: **{sentiment}**")
    else:
        st.write("Please enter some text to analyze.")
