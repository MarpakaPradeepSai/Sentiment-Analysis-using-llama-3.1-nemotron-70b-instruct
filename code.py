import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(
    page_title="Sentiment Analyzer 🌈",
    page_icon="😊",
    layout="centered"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .main-container {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTextArea textarea {
        border: 2px solid #4a90e2;
        border-radius: 10px;
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #357abd;
        transform: scale(1.05);
    }
    .sentiment-result {
        font-size: 1.5em;
        text-align: center;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .positive {
        background-color: #dff0d8;
        color: #3c763d;
    }
    .negative {
        background-color: #f2dede;
        color: #a94442;
    }
    .neutral {
        background-color: #fcf8e3;
        color: #8a6d3b;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key 
)

# Main App Container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Title with Emojis
st.title("📊 Sentiment Analyzer 🔍")
st.markdown("*Understand the emotional tone of your text!* 💬")

# Informative Subheader
st.markdown("""
    ### How it works:
    - Enter any text in the box below
    - Click 'Analyze Sentiment'
    - Get instant sentiment classification 🚀
""")

# Text input box for the user to enter text
input_text = st.text_area(
    "Enter text for sentiment analysis:", 
    placeholder="Type your text here... 📝",
    height=200
)

# Sentiment Analysis Button
if st.button("Analyze Sentiment 🧐"):
    if input_text:
        # Loading Spinner
        with st.spinner('Analyzing sentiment...'):
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
                # Ensure that content exists in the chunk and accumulate
                if chunk.choices[0].delta.content:
                    sentiment += chunk.choices[0].delta.content.strip()
        
        # Sentiment Display with Conditional Styling
        sentiment = sentiment.strip().lower()
        if sentiment in ['positive', 'negative', 'neutral']:
            # Emoji mapping for sentiments
            sentiment_emojis = {
                'positive': '😄 Positive',
                'negative': '😞 Negative',
                'neutral': '😐 Neutral'
            }
            
            # Display sentiment with dynamic styling
            st.markdown(f"""
            <div class="sentiment-result {sentiment}">
                Sentiment: {sentiment_emojis.get(sentiment, sentiment.capitalize())}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Could not determine sentiment. Please try again. 🤔")
    else:
        st.error("Please enter some text to analyze! 📝")

# Closing the main container
st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
    ---
    *Powered by AI Technology* 🚀 | Created with ❤️ using Streamlit
""")
