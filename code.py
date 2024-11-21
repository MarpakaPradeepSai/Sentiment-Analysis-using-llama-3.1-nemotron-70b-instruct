import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Set page configuration
st.set_page_config(page_title="Sentiment Analysis 😊", page_icon="😊")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(135deg, #f0f8ff, #e6e6fa); /* Light blue gradient background */
    }
    .stTextArea textarea {
        border-radius: 10px;
        padding: 15px;
    }
    .stButton button {
        background-color: #4CAF50; /* Green button */
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 10px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI with emojis and better layout
st.title("Sentiment Analysis 😊 Using Llama-3.1 Nemotron 70b instruct")
st.write("Enter your text below to analyze its sentiment! 📝")

input_text = st.text_area("👇 Enter text here:", "")

if st.button("✨ Analyze Sentiment ✨"):
    if input_text:
        with st.spinner("Analyzing... 🔄"):
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
        
            if sentiment.strip():
                # Display sentiment with an appropriate emoji
                if "positive" in sentiment.lower():
                    st.write(f"Sentiment: **{sentiment.strip()}** 😀")
                elif "negative" in sentiment.lower():
                    st.write(f"Sentiment: **{sentiment.strip()}** 😞")
                else:
                    st.write(f"Sentiment: **{sentiment.strip()}** 😐")
            else:
                st.write("Could not determine sentiment. Please try again. 😞")
    else:
        st.write("Please enter some text to analyze. 📝")
