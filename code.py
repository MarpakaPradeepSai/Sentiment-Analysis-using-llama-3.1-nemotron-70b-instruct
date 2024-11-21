import streamlit as st

# Streamlit UI - Enhanced Styling and Layout
st.set_page_config(
    page_title="🌟 Sentiment Analyzer Pro",
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
        .sentiment-box {
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-weight: bold;
            font-size: 1.5em;
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
st.markdown("# 🌟 Sentiment Analyzer Pro")
st.markdown(
    """
    Welcome to the **Sentiment Analyzer Pro**! 🎉  
    Enter your text below, and we'll classify it as **Positive** 😊, **Negative** 😔, or **Neutral** 😐.  
    """
)

# Input Box with Placeholder
st.markdown("### 🖋️ Enter Your Text Below:")
st.text_area(
    "",
    placeholder="✨ Type something amazing here... e.g., 'Streamlit makes data apps so easy!' ✨",
    height=150
)

# Divider
st.markdown("---")
st.markdown("### 🚀 Analyze Sentiment:")

# Analyze Button
st.button("🔍 Analyze Sentiment")

# Footer
st.markdown("---")
st.markdown(
    """
    🛠️ Built with ❤️ using [Streamlit](https://streamlit.io) and NVIDIA's Llama-3.1 Model.  
    ✨ Analyze your text sentiment with ease!  
    """
)
