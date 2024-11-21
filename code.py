import streamlit as st
from openai import OpenAI
import time

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key="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"  # Replace with your actual API key
)

# Set page configuration
st.set_page_config(page_title="Sentiment Analysis Magic ✨", page_icon="🔮")

# Custom CSS for styling
st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(135deg, #f0f8ff, #e6e6fa); /* Light blue gradient background */
    }
    .stTextArea textarea {
        border-radius: 15px;
        padding: 20px;
        font-size: 16px;
        border: 2px solid #ddd;
    }
    .stButton button {
        background-color: #4CAF50; /* Green button */
        color: white;
        padding: 15px 30px;
        border: none;
        border-radius: 15px;
        font-size: 18px;
        cursor: pointer;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    .stMarkdown h1 {
        text-align: center;
        color: #333;
        font-weight: bold;
    }
    .stAlert {
        background-color: #f0f8ff;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #3498db;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit UI with animations and better layout
st.markdown("<h1>Sentiment Analysis Magic ✨ Using Llama-3.1 Nemotron 70b instruct</h1>", unsafe_allow_html=True)
st.write("Enter your text below to reveal its sentiment! 🌟")

input_text = st.text_area("👇 Enter text here:", "")

if st.button("✨ Reveal Sentiment ✨"):
    if input_text:
        with st.spinner("Unveiling sentiment... ⏳"):
            completion = client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[
                    {
                        "role": "user",
                        "content": f"Please analyze the sentiment of the following text carefully, determining whether the tone is positive, negative, or neutral. Once the analysis is complete, respond with only one word: 'Positive' if the sentiment conveys a favorable or optimistic tone, 'Negative' if the sentiment expresses dissatisfaction, sadness, or any form of negativity, or 'Neutral' if the sentiment does not lean towards either positive or negative but rather remains impartial or neutral. Do not provide any additional explanations or details, just the sentiment classification.'. Text: '{input_text}'"
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
        
            if sentiment.strip():
                # Display sentiment with an appropriate emoji and animation
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
        st.warning("Please enter some text to analyze. 📝")
