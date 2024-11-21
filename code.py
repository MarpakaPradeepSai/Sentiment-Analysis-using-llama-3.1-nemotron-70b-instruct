import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Streamlit UI
st.set_page_config(page_title="Sentiment Analyzer", page_icon="💬", layout="centered")

# Header Section
st.markdown(
    """
    <style>
        .title {
            text-align: center;
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 20px;
        }
        .subtitle {
            text-align: center;
            font-size: 20px;
            color: #6C757D;
        }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown('<div class="title">💬 Sentiment Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Analyze text sentiment with the power of AI 🤖</div>', unsafe_allow_html=True)

# Text Input Section
input_text = st.text_area(
    "📝 Enter text for sentiment analysis:", 
    "", 
    height=150, 
    help="Type or paste any text here for sentiment analysis."
)

# Sentiment Analysis Button
if st.button("🔍 Analyze Sentiment"):
    if input_text.strip():
        with st.spinner("Analyzing sentiment... ✨"):
            # Modify the prompt to ensure the model responds with just 'positive', 'negative', or 'neutral'
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",  # Ensure this model supports sentiment analysis
                messages=[
                    {
                        "role": "user",
                        "content": (
                            f"Please analyze the sentiment of the following text and respond with "
                            f"only one word: 'Positive', 'Negative', or 'Neutral'.\n\nText: '{input_text}'"
                        )
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

        # Display Result
        if sentiment.strip():
            sentiment_icon = {
                "Positive": "😊",
                "Negative": "😞",
                "Neutral": "😐"
            }.get(sentiment.strip(), "🤔")
            
            st.success(f"**Sentiment: {sentiment_icon} {sentiment.strip()}**")
        else:
            st.error("Could not determine sentiment. Please try again.")
    else:
        st.warning("⚠️ Please enter some text to analyze!")

# Footer
st.markdown(
    """
    <hr style="border-top: 2px solid #bbb;">
    <p style="text-align: center; font-size: 14px; color: #6C757D;">
        Built with ❤️ using NVIDIA's Llama-3.1 Nemotron 70b instruct model and Streamlit
    </p>
    """,
    unsafe_allow_html=True
)
