import streamlit as st
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Set page configuration
st.set_page_config(page_title="Sentiment Analysis Magic ✨", page_icon="🔮", layout="centered")

# Custom CSS for enhanced design
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(120deg, #84fab0, #8fd3f4); /* Gradient background */
        animation: gradientBG 10s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .reportview-container {
        background: none;
    }
    .stTextArea textarea {
        border-radius: 15px;
        padding: 20px;
        font-size: 18px;
        border: 2px solid #ddd;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        animation: fadeIn 1s;
    }
    .stButton button {
        background-color: #4CAF50; /* Green button */
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 20px;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        animation: bounce 2s infinite;
    }
    .stButton button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    h1 {
        text-align: center;
        font-size: 3rem;
        color: #333;
        font-weight: bold;
        text-shadow: 2px 2px #ffffff;
        animation: textGlow 2s ease-in-out infinite alternate;
    }
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    @keyframes textGlow {
        from {
            text-shadow: 0 0 10px #3498db, 0 0 20px #3498db;
        }
        to {
            text-shadow: 0 0 20px #74b9ff, 0 0 30px #74b9ff;
        }
    }
    .emoji {
        font-size: 3rem;
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown("<h1>🔮 Sentiment Analysis Magic ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3>🌈 Unlock the power of AI and discover the sentiment of your text!</h3>", unsafe_allow_html=True)

# Input box with placeholder
input_text = st.text_area("👇 Type or paste your text below:", "", placeholder="e.g., This app is simply amazing! 💖")

# Button with sentiment analysis
if st.button("✨ Reveal Sentiment ✨"):
    if input_text:
        with st.spinner("Unveiling sentiment... ⏳"):
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
                    time.sleep(0.05)  # Simulate typing effect

        # Display sentiment with animations
        if sentiment.strip():
            if "positive" in sentiment.lower():
                st.success(f"**Sentiment:** Positive 😄🎉", icon="🎉")
                st.balloons()
            elif "negative" in sentiment.lower():
                st.error(f"**Sentiment:** Negative 😞💔", icon="💔")
            else:
                st.info(f"**Sentiment:** Neutral 😐💭", icon="💭")
        else:
            st.warning("Could not determine sentiment. Please try again. 😞", icon="⚠️")
    else:
        st.warning("Please enter some text to analyze. 📝", icon="✏️")
