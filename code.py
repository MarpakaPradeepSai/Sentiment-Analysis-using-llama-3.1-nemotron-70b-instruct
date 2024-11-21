import streamlit as st
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Set page configuration
st.set_page_config(page_title="Sentiment Analysis Spectacle ✨", page_icon="🎭")

# Custom CSS for advanced styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(135deg, #f5f7fa, #c3cfe2); /* Enhanced gradient background */
    }
    .stTextArea textarea {
        border-radius: 20px;
        padding: 25px;
        font-size: 18px;
        border: 3px solid #e0e0e0;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border: 3px solid #aed6f1;
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
    }
    .stButton button {
        background: linear-gradient(45deg, #4CAF50, #81C784); /* Gradient button */
        color: white;
        padding: 20px 40px;
        border: none;
        border-radius: 25px;
        font-size: 20px;
        font-weight: bold;
        cursor: pointer;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    .stMarkdown h1 {
        text-align: center;
        color: #2c3e50;
        font-weight: 900;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        margin-bottom: 40px;
    }
    .stAlert {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 15px;
        border-left: 6px solid #3498db;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .custom-container {
        border: 1px solid #d3d3d3;
        padding: 20px;
        border-radius: 15px;
        margin-top: 20px;
        background-color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI with enhanced styling and containers
st.markdown("<h1>Sentiment Analysis Spectacle ✨ Using Llama-3.1 Nemotron 70b</h1>", unsafe_allow_html=True)
st.write("Enter your text below to unveil its emotional essence! 💖")

with st.container(border=True):
    input_text = st.text_area("👇 Infuse your text here:", "")

if st.button("✨ Unveil the Sentiment ✨"):
    if input_text:
        with st.spinner("Conjuring sentiment analysis... ⏳"):
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": f"Please analyze the sentiment of the following text and no matter what just respond with only one word: 'Positive', 'Negative', or 'Neutral'. Text: '{input_text}'"
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
                    time.sleep(0.05)  # Typing effect
        
            with st.container(className="custom-container"):
                if sentiment.strip():
                    if "positive" in sentiment.lower():
                        st.success(f"Sentiment: **{sentiment.strip()}** 😄🎉")
                        st.balloons()
                    elif "negative" in sentiment.lower():
                        st.error(f"Sentiment: **{sentiment.strip()}** 😞💔")
                    else:
                        st.info(f"Sentiment: **{sentiment.strip()}** 😐💭")
                else:
                    st.warning("Could not determine sentiment. Please try again. 😞")
    else:
        st.warning("Please bestow some text to analyze. 📝")
