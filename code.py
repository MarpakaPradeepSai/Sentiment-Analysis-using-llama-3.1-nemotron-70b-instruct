import streamlit as st
from openai import OpenAI

# Replace with your actual API key
api_key = "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"  # Don't commit this line!
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=api_key,
)

# Streamlit UI with improved design
st.set_page_config(page_title="Sentiment Analysis with Llama ", layout="wide")

st.title("Sentiment Analysis ️‍♀️  Using Llama-3.1 Nemotron 70b instruct")

# Text input with emojis and better styling
text_area = st.empty()
with text_area:
    input_text = st.text_area(
        "Enter text for sentiment analysis:", "", placeholder="Write your text here..."
    )


if st.button("Analyze Sentiment"):
    if input_text:
        # Prompt modification for sentiment classification
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[
                {
                    "role": "user",
                    "content": f"Analyze the sentiment of the following text and respond with one word: 'positive' , 'negative' , or 'neutral' . Text: '{input_text}'",
                }
            ],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True,
        )

        sentiment = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                sentiment += chunk.choices[0].delta.content.strip()

        # Display results with emojis for sentiment
        if sentiment.strip():
            st.write(f"Sentiment: **{sentiment.strip()}** {get_emoji(sentiment)}")
        else:
            st.write("Could not determine sentiment. Please try again.")
    else:
        st.write("Please enter some text to analyze.")


def get_emoji(sentiment):
    if sentiment.lower() == "positive":
        return ""
    elif sentiment.lower() == "negative":
        return ""
    else:
        return ""
