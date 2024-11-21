import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(
    page_title="Sentiment Analyzer 🧠💬", 
    page_icon="📊",
    layout="centered"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .big-font {
        font-size:20px !important;
        color: #333;
        font-weight: 600;
    }
    .stTextArea > div > div > textarea {
        border-radius: 10px;
        border: 2px solid #4A90E2;
        padding: 10px;
        background-color: #F0F4F8;
    }
    .stButton > button {
        background-color: #4A90E2;
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #357ABD;
        transform: scale(1.05);
    }
    .sentiment-result {
        background-color: #E6F2FF;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="API"  # Replace with your actual API key 
)

# Title with emojis and styling
st.markdown("<h1 style='text-align: center; color: #4A90E2;'>Sentiment Analyzer 🧠💬</h1>", unsafe_allow_html=True)

# Subtitle
st.markdown("<p class='big-font' style='text-align: center;'>Understand the Emotional Tone of Your Text 📝</p>", unsafe_allow_html=True)

# Explanation
with st.expander("How does this work? 🤔"):
    st.write("""
    - Enter any text in the box below
    - Click 'Analyze Sentiment'
    - We'll determine if the text is Positive 😊, Negative 😔, or Neutral 😐
    - Uses advanced AI to understand emotional context
    """)

# Text input box for the user to enter text
input_text = st.text_area(
    "Enter text for sentiment analysis:", 
    placeholder="Type or paste your text here...",
    height=200
)

# Sentiment Analysis Button
col1, col2, col3 = st.columns([1,2,1])
with col2:
    analyze_button = st.button("Analyze Sentiment 🔍")

# Sentiment Analysis Logic
if analyze_button:
    if input_text:
        # Disable button during processing
        st.session_state.disabled = True
        
        # Show loading spinner
        with st.spinner('Analyzing sentiment... 🤖'):
            # Sentiment analysis prompt
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
            
            sentiment = ""
            for chunk in completion:
                if chunk.choices[0].delta.content:
                    sentiment += chunk.choices[0].delta.content.strip()
            
            # Clean and normalize sentiment
            sentiment = sentiment.strip().lower()
            
            # Sentiment Display with Emojis
            if sentiment in ['positive', 'negative', 'neutral']:
                emoji_map = {
                    'positive': '😊 Positive 🌞',
                    'negative': '😔 Negative 🌧️',
                    'neutral': '😐 Neutral 🌤️'
                }
                
                # Display sentiment with custom styling
                st.markdown(f"""
                <div class='sentiment-result'>
                    <h2>{emoji_map.get(sentiment, 'Unknown')}</h2>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Could not determine sentiment. Please try again.")
    else:
        st.error("🚨 Please enter some text to analyze!")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Powered by NVIDIA Llama-3.1 Nemotron 70b Instruct 🚀</p>", unsafe_allow_html=True)
