import streamlit as st
from openai import OpenAI

# Streamlit UI - Enhanced Styling and Layout
st.set_page_config(
    page_title="🌍🌈Multilingual Sentiment Analyzer",
    page_icon="💬",
    layout="centered"
)

# Add custom CSS for advanced styling
st.markdown(
    """
    <style>
        body {
            background: linear-gradient(120deg, #a6c1ee, #fbc2eb);
            font-family: 'Arial', sans-serif;
        }
        .main {
            background-color: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(10px);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
        }
        h1 {
            color: #6a0572;
            text-align: center;
            font-size: 3em;
            margin-bottom: 15px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
        }
        p {
            color: #4a4e69;
            text-align: center;
            font-size: 1.1em;
        }
        .stButton>button {
            background: linear-gradient(90deg, #ff8a00, #e52e71);
            color: white;
            border: none;
            border-radius: 25px;
            padding: 10px 20px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .stButton>button:hover {
            transform: scale(1.05);
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            padding: 10px;
            font-size: 1em;
            font-weight: 400;
            width: 100%;
            margin-bottom: 20px;
            border: 2px solid #6a0572;
            transition: border-color 0.3s;
        }
        .stTextInput>div>div>input:focus {
            border-color: #ff8a00;
        }
        .sentiment-box {
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 1.8em;
        }
        .positive {
            background-color: #c8f7c5;
            color: #256029;
        }
        .negative {
            background-color: #f7c5c5;
            color: #601828;
        }
        .neutral {
            background-color: #c5eaf7;
            color: #185a60;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Header
st.markdown("# 🌍🌈Multilingual Sentiment Analyzer")
st.markdown(
    """
    Welcome to the **Sentiment Analyzer Pro**! 🎉  
    """
)

# API Key Input with Custom Styling
st.markdown("##### 🛠️ Enter Your NVIDIA API Key Below:")
api_key = st.text_input(
    "Enter API Key",
    type="password",  # Mask the input for security
    placeholder="🔑 Enter your NVIDIA API key here...",
    help="You can get your API key from your NVIDIA account dashboard."
)

# Add a helpful message with a link for users to create an API key
st.markdown(
    """
    Don't have an API key? Create one [here](https://build.nvidia.com/nvidia/llama-3_1-nemotron-70b-instruct).
    """,
    unsafe_allow_html=True
)

# Input Box for Text to Analyze
st.markdown("##### 🖋️ Enter Your Text Below To Analyze Its Sentiment:")
input_text = st.text_area(
    "",
    placeholder="✨ Type something amazing here... e.g., 'Streamlit makes data apps so easy!' ✨",
    height=150
)

# Animated Divider
st.markdown("---")
st.markdown("### 🚀 Analyze Sentiment:")

# Analyze Button with Interactive Result
if st.button("🔍 Analyze Sentiment"):
    if api_key.strip() and input_text.strip():
        # Initialize OpenAI client with user-provided API key
        client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key  # Use the API key provided by the user
        )

        # Modify the prompt to ensure the model responds with just 'positive', 'negative', or 'neutral'
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{
                "role": "user",
                "content": f"First, identify the language of this sentence, understand it, and then perform sentiment analysis to determine if the tone is Positive, Negative, or Neutral. After the analysis is complete, respond with only one word: (Positive, Negative, or Neutral). Do not provide any additional explanations or details, just the sentiment classification.'. Text: '{input_text}'"
            }],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )

        sentiment = ""  # Variable to accumulate the sentiment result
        for chunk in completion:
            if chunk.choices[0].delta.content:
                sentiment += chunk.choices[0].delta.content.strip()

        sentiment = sentiment.strip().lower()

        # Sentiment Box with Dynamic Styling
        if sentiment == "positive":
            st.markdown(
                f'<div class="sentiment-box positive">Sentiment: <strong>Positive</strong> 😊</div>',
                unsafe_allow_html=True,
            )
            st.balloons()
        elif sentiment == "negative":
            st.markdown(
                f'<div class="sentiment-box negative">Sentiment: <strong>Negative</strong> 😔</div>',
                unsafe_allow_html=True,
            )
        elif sentiment == "neutral":
            st.markdown(
                f'<div class="sentiment-box neutral">Sentiment: <strong>Neutral</strong> 😐</div>',
                unsafe_allow_html=True,
            )
            st.snow()
        else:
            st.warning("⚠️ Unable to determine sentiment. Please try again.")
    else:
        st.warning("⚠️ Please make sure to enter both an API key and text to analyze.")

# Footer
st.markdown("---")
st.markdown(
    """
    🛠️ Built with ❤️ using [Streamlit](https://streamlit.io) and [NVIDIA's Llama-3.1-Nemotron-70b-instruct](https://build.nvidia.com/nvidia/llama-3_1-nemotron-70b-instruct)
    """
)
