import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Streamlit page configuration
st.set_page_config(page_title="Sentiment Analyzer", page_icon="💡", layout="centered")

# Custom CSS styles for advanced UI
st.markdown(
    """
    <style>
        /* Background gradient and page styling */
        body {
            background: linear-gradient(135deg, #84fab0 10%, #8fd3f4 100%);
            color: #333333;
            font-family: 'Arial', sans-serif;
        }

        .stTextArea label {
            font-weight: bold;
            color: #333;
        }

        .title {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #1f3b4d;
            margin-top: 20px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
        }

        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #4f6277;
            margin-bottom: 20px;
        }

        .analyze-btn {
            background-color: #28a745;
            color: white;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 5px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease-in-out;
        }
        
        .analyze-btn:hover {
            background-color: #218838;
            box-shadow: 3px 3px 12px rgba(0, 0, 0, 0.4);
        }

        .result {
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
            color: #1f3b4d;
        }

        footer {
            text-align: center;
            margin-top: 30px;
            font-size: 14px;
            color: #555555;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Header section
st.markdown('<div class="title">💡 Sentiment Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Transform text into insights with cutting-edge AI 🧠</div>', unsafe_allow_html=True)

# Input section
input_text = st.text_area(
    "📝 Enter text for sentiment analysis:",
    "",
    height=150,
    help="Type or paste any text here for sentiment analysis."
)

# Sentiment analysis button
analyze_clicked = st.button("🔍 Analyze Sentiment", use_container_width=True, key="analyze", help="Click to analyze the sentiment!")

if analyze_clicked:
    if input_text.strip():
        with st.spinner("Analyzing sentiment... 🎉"):
            # Generate the sentiment analysis result
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Analyze the sentiment of the following text and reply "
                            f"only with 'Positive', 'Negative', or 'Neutral'.\n\nText: '{input_text}'"
                        )
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

        # Display sentiment result
        if sentiment.strip():
            sentiment_icon = {
                "Positive": "😊",
                "Negative": "😞",
                "Neutral": "😐"
            }.get(sentiment.strip(), "🤔")
            st.markdown(
                f'<div class="result">{sentiment_icon} Sentiment: <span style="color:#28a745;">{sentiment.strip()}</span></div>',
                unsafe_allow_html=True
            )
        else:
            st.error("❌ Unable to determine sentiment. Please try again!")
    else:
        st.warning("⚠️ Please enter some text to analyze!")

# Footer section
st.markdown(
    """
    <footer>
        Built with ❤️ using <b>NVIDIA's Llama-3.1 Nemotron 70b</b> and Streamlit 🚀
    </footer>
    """,
    unsafe_allow_html=True
)
