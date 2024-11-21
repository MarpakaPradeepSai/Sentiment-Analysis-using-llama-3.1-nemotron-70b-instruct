import streamlit as st
from openai import OpenAI

# Initialize the OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"
)

# Streamlit user interface
st.title("Sentiment Analysis App")
st.write("Enter a sentence, and the app will tell you if the sentiment is positive, negative, or neutral.")

# Text input from the user
user_input = st.text_area("Enter your text here:")

# Function to call the model for sentiment analysis
def get_sentiment(input_text):
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
    
    # Process and return the response
    for chunk in completion:
        if chunk.choices[0].delta.content is not None:
            return chunk.choices[0].delta.content.strip()

# Trigger sentiment analysis when the user presses the button
if st.button('Analyze Sentiment'):
    if user_input:
        sentiment = get_sentiment(user_input)
        st.write(f"Sentiment: {sentiment}")
    else:
        st.write("Please enter some text to analyze.")
