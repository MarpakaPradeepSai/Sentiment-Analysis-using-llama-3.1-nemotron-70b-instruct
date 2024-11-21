import streamlit as st
from openai import OpenAI
import time  # Import time for adding a delay effect

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Set page configuration
st.set_page_config(
    page_title="Sentiment Analyzer with Llama-3 🤖",
    page_icon="😊",
    layout="centered"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .stTextArea textarea {
        border: 3px solid #007BFF;  /* Blue border */
        border-radius: 15px;
        padding: 20px;
        font-size: 16px;
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1); /* Add shadow */
    }
    .stButton button {
        background-color: #28A745;  /* Success green */
        color: white;
        padding: 15px 25px;
        border: none;
        border-radius: 12px;
        font-size: 18px;
        box-shadow: 3px 3px 8px rgba(0, 0, 0, 0.2); /* Add shadow */
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;  /* Smooth transition */
    }
    .stButton button:hover {
        background-color: #218838; /* Darker green on hover */
        transform: translateY(-3px);  /* Slight lift effect on hover */
        box-shadow: 5px 5px 12px rgba(0, 0, 0, 0.3);
    }
    .result {
        padding: 20px;
        border-radius: 15px;
        background-color: #f0f8ff;  /* Light blue background */
        box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
        margin-top: 20px;
        font-size: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Title with animation and emojis
st.title("🤖 Sentiment Analyzer with Llama-3 😊")

# Subheader
st.subheader("Type your text below and let Llama-3 reveal its sentiment! 👇")

# Text input area
input_text = st.text_area("✍️ Enter your text here:")

if st.button("🔍 Analyze Sentiment"):
    if input_text:
        with st.spinner('Analyzing... 🧠'):
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
                    time.sleep(0.05)  # Add a slight delay for a typing effect

        if sentiment.strip():
            sentiment = sentiment.strip()
            if sentiment.lower() == "positive":
                result_display = f"😄 Sentiment: **{sentiment}** 🎉"
            elif sentiment.lower() == "negative":
                result_display = f"😞 Sentiment: **{sentiment}** 😔"
            else:
                result_display = f"😐 Sentiment: **{sentiment}** 🤔"

            # Display result in a styled container
            st.markdown(f'<div class="result">{result_display}</div>', unsafe_allow_html=True)
        else:
            st.write("😞 Could not determine sentiment. Please try again.")
    else:
        st.write("📝 Please enter some text to analyze.")

# Footer
st.markdown("---")  # Horizontal line separator
st.markdown("Powered by OpenAI's Llama-3 and Streamlit ✨")
