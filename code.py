import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Set page config (optional)
st.set_page_config(page_title="Sentiment Analysis", page_icon="💬", layout="centered")

# Add a custom header and subheader with some color
st.markdown("""
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
    }
    .subheader {
        font-size: 20px;
        color: #555555;
        text-align: center;
    }
    .input-box {
        width: 100%;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #ccc;
    }
    .result-box {
        background-color: #f1f1f1;
        padding: 10px;
        border-radius: 5px;
        font-size: 20px;
        font-weight: bold;
        color: #333333;
    }
    .button-style {
        font-size: 18px;
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        cursor: pointer;
    }
    .button-style:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)

# Display the title and subheader
st.markdown('<p class="title">Sentiment Analysis Using Llama-3.1 Nemotron 70b Instruct</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Enter some text and click "Analyze" to see its sentiment</p>', unsafe_allow_html=True)

# Add a text area with custom styling for input text
input_text = st.text_area("Enter text for sentiment analysis:", "", height=150, key="input_text", max_chars=1000)

# Add a loading spinner while analyzing the sentiment
if st.button("Analyze Sentiment", key="analyze", help="Click to analyze sentiment"):
    with st.spinner("Analyzing sentiment... Please wait."):
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

            # Display the sentiment result in a styled result box
            if sentiment.strip():
                st.markdown(f'<div class="result-box">Sentiment: {sentiment.strip()}</div>', unsafe_allow_html=True)
            else:
                st.write("Could not determine sentiment. Please try again.")
        else:
            st.write("Please enter some text to analyze.")

