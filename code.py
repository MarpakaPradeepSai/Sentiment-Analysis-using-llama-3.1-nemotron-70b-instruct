import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Streamlit UI - App Header
st.set_page_config(
    page_title="✨ Sentiment Analyzer ✨",
    page_icon="🧠",
    layout="centered"
)

# Add a custom style to improve the app's appearance
st.markdown(
    """
    <style>
        .main {
            background-color: #f7f9fc;
            padding: 20px;
            border-radius: 15px;
        }
        h1 {
            color: #4a4e69;
            text-align: center;
            font-size: 2.5em;
            margin-bottom: 20px;
        }
        .stButton>button {
            background-color: #4a90e2;
            color: white;
            border-radius: 10px;
            font-size: 1.2em;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #0066cc;
            color: #fff;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and Description
st.markdown("# 🌟 Sentiment Analyzer")
st.markdown(
    """
    Welcome to the **Sentiment Analyzer**! 🎉  
    Simply enter your text below, and we'll determine if it's **Positive** 😊, **Negative** 😔, or **Neutral** 😐.  
    """
)

# User Input
st.markdown("### 📋 Enter your text:")
input_text = st.text_area(
    "Type something interesting here!", 
    placeholder="e.g., I love learning about AI!", 
    height=150
)

# Sentiment Analysis Button
if st.button("🔍 Analyze Sentiment"):
    if input_text.strip():
        # Modify the prompt to ensure the model responds with just 'positive', 'negative', or 'neutral'
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
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
            if chunk.choices[0].delta.content:
                sentiment += chunk.choices[0].delta.content.strip()

        # Display Sentiment Result
        sentiment = sentiment.strip().lower()
        if sentiment == "positive":
            st.success(f"Sentiment: **{sentiment.capitalize()}** 😊")
        elif sentiment == "negative":
            st.error(f"Sentiment: **{sentiment.capitalize()}** 😔")
        elif sentiment == "neutral":
            st.info(f"Sentiment: **{sentiment.capitalize()}** 😐")
        else:
            st.warning("Could not determine sentiment. Please try again.")
    else:
        st.warning("⚠️ Please enter some text to analyze.")
