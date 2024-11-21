import streamlit as st
from openai import OpenAI
import time

# Set page configuration
st.set_page_config(
    page_title="Sentiment Analyzer 🧠",
    page_icon="📊",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stTextArea textarea {
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 10px;
    }
    .stButton>button {
        background-color: #2ecc71;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #27ae60;
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1", 
    api_key="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"
)

# Title and description
st.title("🎭 Sentiment Analyzer")
st.markdown("### Discover the emotional tone of your text!")

# Text input with helpful placeholder
input_text = st.text_area(
    "Enter your text here:", 
    placeholder="Type or paste the text you want to analyze...",
    height=200
)

# Sentiment analysis function
def analyze_sentiment(text):
    try:
        # Show loading spinner
        with st.spinner('Analyzing sentiment... 🔍'):
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[
                    {
                        "role": "user", 
                        "content": f"Please analyze the sentiment of the following text and respond with only one word: 'Positive', 'Negative', or 'Neutral'. Text: '{text}'"
                    }
                ],
                temperature=0.5,
                top_p=1,
                max_tokens=10
            )
            
            sentiment = completion.choices[0].message.content.strip().capitalize()
            return sentiment
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Emoji mapping for sentiments
SENTIMENT_EMOJIS = {
    'Positive': '😄',
    'Neutral': '😐',
    'Negative': '😞'
}

# Sentiment color mapping
SENTIMENT_COLORS = {
    'Positive': 'green',
    'Neutral': 'gray',
    'Negative': 'red'
}

# Analyze button
if st.button("Analyze Sentiment 🚀"):
    if input_text:
        # Perform sentiment analysis
        sentiment = analyze_sentiment(input_text)
        
        if sentiment:
            # Display result with styling
            st.markdown(f"""
                <div style='background-color: {SENTIMENT_COLORS[sentiment]}; 
                            color: white; 
                            padding: 20px; 
                            border-radius: 10px; 
                            text-align: center;'>
                    <h2>Sentiment: {sentiment} {SENTIMENT_EMOJIS[sentiment]}</h2>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please enter some text to analyze! 📝")

# Footer
st.markdown("---")
st.markdown("*Powered by NVIDIA's Llama-3.1 Nemotron 70b Instruct* 🤖")
