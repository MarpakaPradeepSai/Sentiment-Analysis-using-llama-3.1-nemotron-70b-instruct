import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Set page configuration
st.set_page_config(
    page_title="Sentiment Analysis with Llama-3",
    page_icon="😊",  # Add a friendly emoji to the page tab
    layout="centered"
)

# Custom CSS to style components
st.markdown("""
<style>
    .stTextArea textarea {
        border: 2px solid #4CAF50; /* Green border for text area */
        border-radius: 10px;
        padding: 15px;
    }
    .stButton button {
        background-color: #4CAF50; /* Green background for button */
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049; /* Darker green on hover */
    }
</style>
""", unsafe_allow_html=True)

# Title with an engaging emoji
st.title("😊 Sentiment Analysis Using Llama-3.1 Nemotron 70b instruct")

# Text input box for the user to enter text
input_text = st.text_area("✍️ Enter text for sentiment analysis:", "")

if st.button("🔍 Analyze Sentiment"):
    if input_text:
        # Add a spinner while processing
        with st.spinner('Analyzing... 🧠'):
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",  # Ensure this model supports sentiment analysis
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

            sentiment = ""  # Variable to accumulate the sentiment result
            for chunk in completion:
                # Ensure that content exists in the chunk and accumulate
                if chunk.choices[0].delta.content:
                    sentiment += chunk.choices[0].delta.content.strip()

        # Check the accumulated sentiment and display with emojis
        if sentiment.strip():
            sentiment = sentiment.strip()
            if sentiment.lower() == "positive":
                st.write(f"Sentiment: **{sentiment}** 😄")  # Happy emoji for positive
            elif sentiment.lower() == "negative":
                st.write(f"Sentiment: **{sentiment}** 😞")  # Sad emoji for negative
            else:
                st.write(f"Sentiment: **{sentiment}** 😐")  # Neutral emoji for neutral
        else:
            st.write("😞 Could not determine sentiment. Please try again.")
    else:
        st.write("📝 Please enter some text to analyze.")
